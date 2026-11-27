"""Fixed, fail-closed B2 medication workflow (no model-driven tool selection)."""
import re

from ai import call_model
import tools

SUMMARY_SYSTEM = """Tóm lược bằng tiếng Việt chỉ nội dung kết quả workflow được cung cấp.
Không thêm thuốc, tương tác, liều, lịch, hướng dẫn y tế hoặc dữ kiện nào khác.
Giữ nguyên các cảnh báo, giới hạn, trạng thái thiếu dữ liệu và nguồn.
Nếu không thể diễn đạt mà không thêm thông tin, hãy trả nguyên văn nội dung workflow."""


def _respond(workflow_result: str) -> dict:
    """Pass checked workflow output to the model for final presentation only."""
    reply = call_model(SUMMARY_SYSTEM, workflow_result)
    return {"output": reply["text"]}


def _extract_seeded_drugs(text: str) -> list:
    """Find exact seed names/ingredients mentioned in user text."""
    records, error = tools._load_seed()
    if error:
        return []
    found = []
    normalized_text = " " + " ".join(text.casefold().split()) + " "
    for record in records:
        if record.get("record_type") != "drug_reference":
            continue
        for field in ("name", "active_ingredient"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                continue
            name = " ".join(value.casefold().split())
            if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", normalized_text):
                if name not in found:
                    found.append(name)
                break
    return found


def _is_interaction_request(text: str) -> bool:
    lowered = text.casefold()
    return any(term in lowered for term in ("tương tác", "uống chung", "kết hợp", "cùng lúc", "phối hợp", "kỵ nhau"))


def _is_schedule_request(text: str) -> bool:
    lowered = text.casefold()
    return any(term in lowered for term in ("xếp lịch", "lịch uống", "sắp thuốc", "sắp lịch", "thời điểm uống"))


def _handoff(text: str, reason: str) -> str:
    draft = tools.handoff_to_pharmacist(reason + "\nThông tin người dùng cung cấp: " + text)
    return reason + "\n" + draft["draft"] + "\n" + draft["message"]


def _render_drug(record: dict) -> str:
    lines = [
        "Tra cứu trong dữ liệu demo: %s (hoạt chất: %s)." % (
            record["drug_name"], record["active_ingredient"]
        ),
        record["summary"],
        record["message"],
    ]
    if record.get("dose_or_schedule") is None:
        lines.append("Seed chưa có chỉ định liều/lịch đã xác minh cho thuốc này.")
    if record.get("sources"):
        lines.append("Nguồn: " + "; ".join(record["sources"]))
    return "\n".join(lines)


def answer(text: str) -> dict:
    """Run the mandatory B2 checks in order and return {"output": str}."""
    if not isinstance(text, str) or not text.strip():
        return {"output": "Vui lòng nhập thông tin cần kiểm tra. Nếu đang nguy cấp, gọi 115 hoặc đến cơ sở cấp cứu ngay."}

    # 1. Emergency gate: never continue to medication lookup/scheduling/model.
    red_flags = tools.check_red_flags(text)
    if red_flags.get("urgency") == "emergency":
        advice = tools.advise_see_doctor(text)
        return {"output": red_flags["message"] + " " + advice["message"]}

    # 2. Find seed-backed names deterministically; no fuzzy medical-name guessing.
    drug_names = _extract_seeded_drugs(text)
    if not drug_names:
        lookup = tools.lookup_drug(text.strip())
        reason = lookup.get("message", "Không có tên thuốc khớp dữ liệu đã kiểm chứng.")
        return _respond(_handoff(text, reason))

    lookups = [tools.lookup_drug(name) for name in drug_names]
    if any(item.get("status") != "found" for item in lookups):
        reason = "Không xác minh được đầy đủ các thuốc trong dữ liệu. Không thể kết luận an toàn; cần dược sĩ kiểm tra."
        return _respond(_handoff(text, reason))

    # When list punctuation/conjunctions suggest additional medicines beyond
    # the exact seed matches, stop rather than silently checking a partial list.
    separators = len(re.findall(r",|\bvà\b|\bcùng\b|\bvoi\b|\bvới\b", text.casefold()))
    if separators and separators + 1 > len(drug_names):
        reason = "Có thể còn thuốc chưa nhận diện trong danh sách. Vui lòng xác nhận đầy đủ tên/hoạt chất với dược sĩ; chưa thể rà soát toàn bộ cặp."
        return _respond(_handoff(text, reason))

    # 3. Interaction check is mandatory for combination questions or lists.
    interaction_result = None
    if len(drug_names) >= 2 or _is_interaction_request(text):
        if len(drug_names) < 2:
            reason = "Chưa đủ hai tên thuốc đã nhận diện để kiểm tra tương tác. Hãy bổ sung tên/hoạt chất trên nhãn."
            return _respond(_handoff(text, reason))
        interaction_result = tools.check_interactions(drug_names)
        if interaction_result.get("status") == "no_verified_data" or interaction_result.get("status") == "data_unavailable":
            return _respond(_handoff(text, interaction_result["message"]))
        if interaction_result.get("status") == "no_verified_interaction_in_seed":
            return _respond(_handoff(text, interaction_result["message"]))
        high_risk = [
            item for item in interaction_result.get("results", [])
            if item.get("risk_tag") == "high_risk_refer_pharmacist"
        ]
        if high_risk:
            details = "\n".join(item["summary"] for item in high_risk)
            sources = sorted({source for item in high_risk for source in item.get("sources", [])})
            reason = "Cảnh báo tương tác trong seed — cần dược sĩ/bác sĩ xác nhận:\n" + details
            if sources:
                reason += "\nNguồn: " + "; ".join(sources)
            return _respond(_handoff(text, reason))

    # 4. A schedule is allowed only when every matched record supplies an
    # explicit, non-empty instruction. Current seed has null values, so it
    # correctly routes to review instead of constructing times/doses.
    if _is_schedule_request(text):
        instructions = []
        for record in lookups:
            instruction = record.get("dose_or_schedule")
            if not isinstance(instruction, str) or not instruction.strip():
                reason = "Seed chưa có chỉ định dùng đã xác minh cho toàn bộ thuốc; không thể lập lịch. Hãy xem đơn/tờ hướng dẫn và hỏi dược sĩ."
                return _respond(_handoff(text, reason))
            instructions.append({"medication": record["drug_name"], "instruction": instruction})
        schedule = tools.build_schedule(instructions)
        if schedule.get("status") != "draft":
            return _respond(_handoff(text, schedule.get("message", "Không thể lập lịch từ chỉ định đã xác minh.")))
        return _respond(schedule["message"] + "\n" + str(schedule["schedule"]))

    if interaction_result:
        interaction_text = "\n".join(
            item["summary"] for item in interaction_result.get("results", [])
        )
        return _respond(interaction_text or interaction_result["message"])

    return _respond("\n\n".join(_render_drug(record) for record in lookups))
