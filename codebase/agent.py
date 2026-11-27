"""Fixed, fail-closed B2 medication workflow (no model-driven tool selection)."""
import re

from ai import call_model
import tools

SUMMARY_SYSTEM = """Tóm lược bằng tiếng Việt chỉ nội dung kết quả workflow được cung cấp.
Không thêm thuốc, tương tác, liều, lịch, hướng dẫn y tế hoặc dữ kiện nào khác.
Giữ nguyên các cảnh báo, giới hạn, trạng thái thiếu dữ liệu và nguồn.
Nếu không thể diễn đạt mà không thêm thông tin, hãy trả nguyên văn nội dung workflow."""


def _respond(workflow_result: str) -> dict:
    """Accept model output only if it is byte-for-byte the checked workflow."""
    try:
        reply = call_model(SUMMARY_SYSTEM, workflow_result)
    except Exception:
        return {"output": workflow_result}
    candidate = reply.get("text") if isinstance(reply, dict) else None
    if candidate != workflow_result:
        candidate = workflow_result
    return {"output": candidate}


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


def _is_out_of_scope_request(text: str) -> bool:
    lowered = text.casefold()
    return any(term in lowered for term in (
        "chẩn đoán", "kê đơn", "gấp đôi", "tăng liều", "giảm liều", "đổi liều",
        "ngừng thuốc", "bỏ thuốc", "uống bù",
    ))


def _parse_confirmed_instructions(text: str, drug_names: list):
    """Read exact per-drug instructions only from an explicitly confirmed format."""
    lowered = text.casefold()
    confirmation_terms = ("theo đơn", "theo nhãn", "đã xác nhận", "tôi xác nhận", "chỉ định đã xác nhận")
    if not any(term in lowered for term in confirmation_terms) or any(
        term in lowered for term in ("chưa xác nhận", "không xác nhận")
    ):
        return None, "Cần xác nhận rằng các chỉ dẫn bên dưới được chép theo đơn hoặc nhãn thuốc."

    expected = {" ".join(name.casefold().split()) for name in drug_names}
    instructions = {}
    conflicts = []
    ambiguous_terms = ("hoặc", "không chắc", "chưa rõ", "mâu thuẫn", "không nhớ")
    for line in text.splitlines():
        candidate, separator, instruction = line.strip().lstrip("-*• ").partition(":")
        if not separator:
            continue
        normalized_name = " ".join(candidate.casefold().split())
        if normalized_name not in expected:
            if instruction.strip() and not any(
                candidate.casefold().startswith(prefix)
                for prefix in ("xếp lịch", "lập lịch", "chỉ định", "danh sách", "theo đơn")
            ):
                conflicts.append(candidate.strip())
            continue
        instruction = instruction.strip()
        if not instruction or any(term in instruction.casefold() for term in ambiguous_terms):
            conflicts.append(candidate.strip())
            continue
        if normalized_name in instructions:
            conflicts.append(candidate.strip())
            continue
        instructions[normalized_name] = {"medication": candidate.strip(), "instruction": instruction}

    if conflicts:
        return None, "Có chỉ dẫn thiếu hoặc mâu thuẫn cho: %s. Vui lòng đối chiếu lại đơn/nhãn với dược sĩ." % ", ".join(conflicts)
    if set(instructions) != expected:
        missing = sorted(expected - set(instructions))
        return None, "Thiếu dòng chỉ dẫn đã xác nhận cho: %s. Vui lòng bổ sung đúng nội dung trên đơn/nhãn." % ", ".join(missing)
    return list(instructions.values()), None


def _handoff(text: str, reason: str) -> str:
    draft = tools.handoff_to_pharmacist(reason + "\nThông tin người dùng cung cấp: " + text)
    return draft["draft"] + "\n" + draft["message"]


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


def _render_interactions(result: dict) -> str:
    """Render every pair result, retaining status, risk label, and sources."""
    lines = []
    for item in result.get("results", []):
        pair = item.get("pair", item.get("ingredients", []))
        pair_label = " + ".join(pair) if pair else "cặp chưa nhận diện đầy đủ"
        if item.get("status") in {"interaction_found", "interaction_unclassified"} or item.get("risk_tag"):
            risk = item.get("risk_tag") or "chưa phân loại"
            lines.append("Cảnh báo tương tác%s — %s: %s" % (
                (" [%s]" % risk), pair_label, item.get("summary", "")
            ))
            if item.get("message"):
                lines.append(item["message"])
        else:
            lines.append("%s — %s" % (pair_label, item.get("message", "Chưa đủ căn cứ; không kết luận an toàn.")))
        if item.get("sources"):
            lines.append("Nguồn: " + "; ".join(item["sources"]))
        if item.get("limits"):
            lines.append("Giới hạn/cảnh báo an toàn: " + item["limits"])
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

    # 3. Interaction check is mandatory for combination questions or lists.
    interaction_result = None
    interaction_text = ""
    if len(drug_names) >= 2 or _is_interaction_request(text):
        check_names = list(drug_names)
        separators = len(re.findall(r",|\bvà\b|\bcùng\b|\bvới\b|\bvoi\b|\+", text.casefold()))
        if _is_interaction_request(text) and separators + 1 > len(check_names):
            check_names.append("[thuốc chưa nhận diện]")
        if len(check_names) < 2:
            if not _is_schedule_request(text):
                reason = "Chưa đủ hai tên thuốc đã nhận diện để kiểm tra tương tác. Hãy bổ sung tên/hoạt chất trên nhãn."
                return _respond(_handoff(text, reason))
        else:
            interaction_result = tools.check_interactions(check_names)

            pair_results = interaction_result.get("results", [])
            interaction_text = _render_interactions(interaction_result)
            high_risk = [item for item in pair_results
                         if item.get("risk_tag") == "high_risk_refer_pharmacist"]
            incomplete = [item for item in pair_results if item.get("status") in {
                "no_verified_data", "data_unavailable", "no_verified_interaction_in_seed", "interaction_unclassified"
            }]
            if interaction_result.get("status") in {"no_verified_data", "data_unavailable"} and not pair_results:
                incomplete.append({"message": interaction_result.get("message", "Chưa đủ căn cứ kiểm tra tương tác."), "pair": []})

            if high_risk or incomplete:
                details = interaction_text or interaction_result.get("message", "Chưa đủ căn cứ kiểm tra tương tác.")
                reason = details + "\nCần dược sĩ rà soát toàn bộ danh sách trước khi quyết định."
                return _respond(_handoff(text, reason))

    if any(item.get("status") != "found" for item in lookups):
        reason = "Không xác minh được đầy đủ các thuốc trong dữ liệu. Không thể kết luận an toàn; cần dược sĩ kiểm tra."
        if interaction_text:
            reason = interaction_text + "\n" + reason
        return _respond(_handoff(text, reason))

    # 4. Refuse diagnosis, prescribing, and user-requested dose changes.
    if _is_out_of_scope_request(text):
        refusal = (
            "Không thể chẩn đoán, kê đơn hoặc hướng dẫn tăng/giảm, bù, ngừng hay đổi liều. "
            "Không tự thay đổi cách dùng; hãy xác nhận với bác sĩ hoặc dược sĩ."
        )
        if interaction_text:
            refusal = interaction_text + "\n" + refusal
        return _respond(refusal)

    # 5. Schedule entries are copied from explicitly confirmed user input.
    # No dose/time/interval is inferred from the seed or generated here.
    if _is_schedule_request(text):
        instructions, issue = _parse_confirmed_instructions(text, drug_names)
        if issue:
            return _respond(_handoff(text, issue))
        schedule = tools.build_schedule(instructions)
        if schedule.get("status") != "draft":
            return _respond(_handoff(text, schedule.get("message", "Không thể lập lịch từ chỉ định đã xác minh.")))
        output = schedule["message"] + "\n" + str(schedule["schedule"])
        if interaction_result and interaction_text:
            output += "\n" + interaction_text
        return _respond(output)

    if interaction_result:
        return _respond(interaction_text or interaction_result["message"])

    return _respond("\n\n".join(_render_drug(record) for record in lookups))
