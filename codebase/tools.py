"""Read-only, source-bounded tools for the B2 medication support prototype."""
import json
from itertools import combinations
from pathlib import Path

from tracing import tool, TOOLS  # noqa: F401


SEED_PATH = Path(__file__).resolve().parents[1] / "data" / "b2_seed.json"


def _load_seed():
    """Return seed records or a fail-closed error result."""
    try:
        with SEED_PATH.open(encoding="utf-8") as seed_file:
            seed = json.load(seed_file)
    except (OSError, json.JSONDecodeError):
        return None, {
            "status": "data_unavailable",
            "message": "Không đọc được dữ liệu đã kiểm chứng; không thể tra cứu an toàn. Hãy hỏi dược sĩ.",
        }

    if not isinstance(seed, dict) or not isinstance(seed.get("records"), list):
        return None, {
            "status": "data_unavailable",
            "message": "Cấu trúc dữ liệu tra cứu không hợp lệ; không thể đưa ra kết luận. Hãy hỏi dược sĩ.",
        }
    records = seed["records"]
    if any(not isinstance(record, dict) for record in records):
        return None, {
            "status": "data_unavailable",
            "message": "Dữ liệu tra cứu có bản ghi không hợp lệ; không thể đưa ra kết luận. Hãy hỏi dược sĩ.",
        }

    for record in records:
        if record.get("record_type") == "interaction":
            ingredients = record.get("ingredients")
            risk_tag = record.get("risk_tag")
            if (not isinstance(ingredients, list) or len(ingredients) < 2
                    or any(not isinstance(item, str) or not item.strip() for item in ingredients)
                    or (risk_tag is not None and (not isinstance(risk_tag, str) or not risk_tag.strip()))
                    or not isinstance(record.get("summary"), str) or not record["summary"].strip()
                    or not _valid_sources(record.get("source_urls"))):
                return None, {
                    "status": "data_unavailable",
                    "message": "Bản ghi tương tác thiếu trường hoặc nguồn hợp lệ; không thể đưa ra kết luận. Hãy hỏi dược sĩ.",
                }
    return records, None


def _valid_sources(sources):
    return isinstance(sources, list) and bool(sources) and all(
        isinstance(source, str) and source.strip() for source in sources
    )


def _reference_text(record):
    for field in ("summary", "schedule_hint"):
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _drug_record_is_valid(record):
    return (
        isinstance(record.get("name"), str) and bool(record["name"].strip())
        and isinstance(record.get("active_ingredient"), str) and bool(record["active_ingredient"].strip())
        and bool(_reference_text(record))
        and _valid_sources(record.get("source_urls"))
    )


def _drug_identity_is_valid(record):
    """Validate only identity/source fields needed to match an interaction pair."""
    return (
        isinstance(record.get("name"), str) and bool(record["name"].strip())
        and isinstance(record.get("active_ingredient"), str) and bool(record["active_ingredient"].strip())
        and _valid_sources(record.get("source_urls"))
    )


def _normalize_name(value):
    return " ".join(value.casefold().split())


# Explicit emergency wording used only as a conservative escalation trigger.
# This is not a complete clinical rule set and does not establish a diagnosis.
_EMERGENCY_PHRASES = (
    "khó thở", "khong tho duoc", "đau ngực dữ dội", "dau nguc du doi",
    "bất tỉnh", "bat tinh", "co giật", "co giat", "chảy máu nhiều", "chay mau nhieu",
    "chảy máu không cầm được", "chay mau khong cam duoc",
    "không cầm được máu", "khong cam duoc mau",
)


@tool
def check_red_flags(symptoms: str) -> dict:
    """Sàng lọc cụm từ nguy cấp được nêu rõ để hướng dẫn tìm trợ giúp.
    Input: mô tả triệu chứng (str). Output: mức khẩn cấp và hướng dẫn; không chẩn đoán, không tác động ra ngoài."""
    if not isinstance(symptoms, str) or not symptoms.strip():
        return {"status": "invalid_input", "urgency": "unknown", "message": "Vui lòng mô tả tình trạng; nếu đang nguy cấp, gọi 115 ngay."}

    text = symptoms.casefold()
    matched = [phrase for phrase in _EMERGENCY_PHRASES if phrase in text]
    if matched:
        return {
            "status": "possible_emergency",
            "urgency": "emergency",
            "matched_terms": matched,
            "message": "Có cụm từ có thể báo hiệu tình trạng khẩn cấp. Gọi 115 hoặc đến cơ sở cấp cứu ngay; không chờ tư vấn qua ứng dụng. Đây không phải chẩn đoán.",
        }
    return {
        "status": "not_assessed",
        "urgency": "unknown",
        "matched_terms": [],
        "message": "Không thể xác định mức độ an toàn từ kiểm tra từ khóa này. Nếu triệu chứng nặng, đột ngột hoặc xấu đi, gọi 115/đến cơ sở cấp cứu; nếu không, liên hệ nhân viên y tế để được đánh giá.",
    }


@tool
def advise_see_doctor(information: str) -> dict:
    """Đưa hướng tìm trợ giúp y tế dựa trên thông tin người dùng nêu.
    Input: thông tin/tình trạng do người dùng cung cấp (str). Output: khuyến nghị thận trọng; không chẩn đoán, kê đơn hay tác động ra ngoài."""
    if not isinstance(information, str) or not information.strip():
        return {"status": "invalid_input", "recommendation": "seek_clinician", "message": "Chưa có thông tin để đánh giá; hãy liên hệ nhân viên y tế nếu cần trợ giúp."}
    return {
        "status": "limited_information",
        "recommendation": "seek_clinician",
        "message": "Công cụ này không thể chẩn đoán hoặc xác định mức độ an toàn. Hãy liên hệ bác sĩ/dược sĩ để được đánh giá; nếu tình trạng nghiêm trọng, đột ngột hoặc xấu đi, gọi 115 hoặc đến cấp cứu ngay.",
    }


@tool
def lookup_drug(drug_name: str) -> dict:
    """Tra cứu thuốc trong dữ liệu đã đối chiếu.
    Input: tên thuốc (str). Output: dict trạng thái và thông tin có nguồn; không tác động ra ngoài."""
    if not isinstance(drug_name, str) or not drug_name.strip():
        return {"status": "invalid_input", "drug_name": "", "message": "Vui lòng cung cấp tên thuốc để tra cứu."}
    records, error = _load_seed()
    if error:
        return {**error, "drug_name": drug_name.strip(), "sources": []}

    query = _normalize_name(drug_name)
    matches = [
        record for record in records
        if record.get("record_type") == "drug_reference"
        and any(_normalize_name(record.get(field, "")) == query
                for field in ("name", "active_ingredient")
                if isinstance(record.get(field), str))
    ]
    if not matches:
        return {
            "status": "no_verified_data",
            "drug_name": drug_name.strip(),
            "message": "Không tìm thấy tên thuốc trong dữ liệu đã kiểm chứng. Điều này không xác nhận thuốc an toàn; hãy kiểm tra tên/hoạt chất trên nhãn và hỏi dược sĩ.",
            "sources": [],
        }

    record = matches[0]
    if not _drug_record_is_valid(record):
        return {
            "status": "data_unavailable",
            "drug_name": drug_name.strip(),
            "message": "Bản ghi thuốc thiếu thông tin hoặc nguồn hợp lệ; không thể dùng để tư vấn. Hãy hỏi dược sĩ.",
            "sources": [],
        }
    return {
        "status": "found",
        "drug_name": record["name"],
        "active_ingredient": record["active_ingredient"],
        "dose_or_schedule": record.get("dose_or_schedule"),
        "summary": _reference_text(record),
        "sources": record["source_urls"],
        "limits": record.get("limits", ""),
        "message": "Thông tin chỉ là tóm lược nguồn, không phải hướng dẫn liều dùng cá nhân.",
    }


@tool
def check_interactions(drug_names: list) -> dict:
    """Kiểm tra tương tác trong tập dữ liệu đã đối chiếu.
    Input: danh sách tên thuốc (list[str]). Output: trạng thái, kết quả và nguồn; không tác động ra ngoài."""
    if not isinstance(drug_names, (list, tuple)) or len(drug_names) < 2 or any(
        not isinstance(name, str) or not name.strip() for name in drug_names
    ):
        return {"status": "invalid_input", "message": "Cần ít nhất hai tên thuốc hợp lệ để kiểm tra cặp tương tác.", "results": []}
    names = [name.strip() for name in drug_names]
    records, error = _load_seed()
    if error:
        return {**error, "drug_names": names, "results": [], "sources": []}

    normalized_to_name = {}
    for name in names:
        normalized_to_name.setdefault(_normalize_name(name), name)
    normalized_names = list(normalized_to_name)
    if len(normalized_names) < 2:
        return {"status": "invalid_input", "drug_names": names, "results": [],
                "message": "Cần ít nhất hai thuốc khác nhau để kiểm tra các cặp."}
    drug_records = [record for record in records if record.get("record_type") == "drug_reference"]
    drug_by_name = {}
    for record in drug_records:
        if isinstance(record.get("name"), str):
            drug_by_name[_normalize_name(record["name"])] = record
        if isinstance(record.get("active_ingredient"), str):
            drug_by_name[_normalize_name(record["active_ingredient"])] = record

    interaction_records = [record for record in records if record.get("record_type") == "interaction"]
    results = []
    for first, second in combinations(normalized_names, 2):
        pair_names = [normalized_to_name[first], normalized_to_name[second]]
        first_record = drug_by_name.get(first)
        second_record = drug_by_name.get(second)
        if first_record is None or second_record is None:
            results.append({
                "pair": pair_names,
                "status": "no_verified_data",
                "message": "Chưa đủ căn cứ nhận diện cả hai thuốc trong cặp; không thể kết luận có hay không có tương tác.",
                "sources": [],
            })
            continue
        if not _drug_identity_is_valid(first_record) or not _drug_identity_is_valid(second_record):
            results.append({
                "pair": pair_names,
                "status": "data_unavailable",
                "message": "Bản ghi thuốc trong cặp thiếu thông tin hoặc nguồn hợp lệ; chưa đủ căn cứ kiểm tra.",
                "sources": [],
            })
            continue

        pair = {first, second}
        matched = [record for record in interaction_records
                   if {_normalize_name(item) for item in record["ingredients"]} == pair]
        if matched:
            for record in matched:
                risk_tag = record.get("risk_tag")
                results.append({
                    "pair": pair_names,
                    "interaction_id": record.get("id", ""),
                    "status": "interaction_found" if risk_tag else "interaction_unclassified",
                    "ingredients": record["ingredients"],
                    "risk_tag": risk_tag,
                    "summary": record["summary"],
                    "sources": record["source_urls"],
                    "limits": record.get("limits", ""),
                    "message": "Tương tác có nguồn nhưng chưa được phân loại mức rủi ro; cần dược sĩ đánh giá." if not risk_tag else "",
                })
        else:
            results.append({
                "pair": pair_names,
                "status": "no_verified_interaction_in_seed",
                "message": "Seed không có bản ghi cho cặp này; đây không phải xác nhận không có tương tác hoặc thuốc an toàn.",
                "sources": [],
            })

    missing = any(item["status"] in {"no_verified_data", "data_unavailable", "no_verified_interaction_in_seed", "interaction_unclassified"}
                  for item in results)
    has_interaction = any(item["status"] in {"interaction_found", "interaction_unclassified"} for item in results)
    return {
        "status": "partial_data" if missing else ("interaction_found" if has_interaction else "no_verified_interaction_in_seed"),
        "drug_names": names,
        "results": results,
        "message": "Đã kiểm tra từng cặp; xem trạng thái riêng của mỗi cặp. Cặp thiếu dữ liệu chưa đủ căn cứ và không được xem là an toàn.",
    }


@tool
def build_schedule(instructions: list) -> dict:
    """Sắp xếp các chỉ định đã được người có thẩm quyền cung cấp.
    Input: list[dict] với medication và instruction nguyên văn. Output: bản lịch theo thứ tự nhập, giữ nguyên chỉ định; không tác động ra ngoài."""
    if not isinstance(instructions, (list, tuple)) or not instructions:
        return {"status": "invalid_input", "schedule": [], "message": "Cung cấp danh sách chỉ định đã có để lập lịch."}
    schedule = []
    for item in instructions:
        if not isinstance(item, dict):
            return {"status": "invalid_input", "schedule": [], "message": "Mỗi chỉ định phải có dạng đối tượng."}
        medication = item.get("medication")
        instruction = item.get("instruction")
        if not isinstance(medication, str) or not medication.strip() or not isinstance(instruction, str) or not instruction.strip():
            return {"status": "missing_instruction", "schedule": [], "message": "Mỗi thuốc cần tên và chỉ định nguyên văn; không tự điền liều hoặc thời điểm còn thiếu."}
        schedule.append({"medication": medication.strip(), "instruction": instruction.strip()})
    return {
        "status": "draft",
        "schedule": schedule,
        "message": "Bản sắp xếp giữ nguyên chỉ định được cung cấp, không xác minh tính phù hợp. Xác nhận với dược sĩ nếu có điểm chưa rõ; không tự đổi liều hay thời điểm.",
    }


@tool
def handoff_to_pharmacist(summary: str, user_approved: bool = False) -> dict:
    """Tạo bản nháp tóm tắt để người dùng đưa cho dược sĩ.
    Input: summary (str), user_approved (bool). Output: bản nháp cục bộ; không gửi tin hay dữ liệu ra ngoài."""
    if not isinstance(summary, str) or not summary.strip():
        return {"status": "invalid_input", "draft": "", "sent": False, "message": "Cần nội dung tóm tắt để tạo bản nháp."}
    if not isinstance(user_approved, bool):
        return {"status": "invalid_input", "draft": "", "sent": False, "message": "user_approved phải là giá trị boolean."}
    draft = "BẢN NHÁP — người dùng tự xem và quyết định có chia sẻ với dược sĩ:\n" + summary.strip()
    return {
        "status": "draft_pending_user_review",
        "draft": draft,
        "user_approved": user_approved,
        "sent": False,
        "message": "Bản nháp chỉ lưu trong kết quả công cụ; không có thông tin nào được gửi ra ngoài.",
    }
