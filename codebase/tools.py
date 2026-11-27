"""Read-only, source-bounded tools for the B2 medication support prototype.

The repository currently contains no reviewed medication or interaction dataset.
Accordingly lookup and interaction checks fail closed rather than invent facts.
These helpers do not diagnose, prescribe, or change a user's treatment.
"""
from tracing import tool, TOOLS  # noqa: F401


# Explicit emergency wording used only as a conservative escalation trigger.
# This is not a complete clinical rule set and does not establish a diagnosis.
_EMERGENCY_PHRASES = (
    "khó thở", "khong tho duoc", "đau ngực dữ dội", "dau nguc du doi",
    "bất tỉnh", "bat tinh", "co giật", "co giat", "chảy máu nhiều", "chay mau nhieu",
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
    return {
        "status": "no_verified_data",
        "drug_name": drug_name.strip(),
        "message": "Chưa có dữ liệu thuốc được đối chiếu nguồn trong bản thử này. Hãy hỏi dược sĩ; không suy diễn cách dùng hoặc liều.",
        "sources": [],
    }


@tool
def check_interactions(drug_names: list) -> dict:
    """Kiểm tra tương tác trong tập dữ liệu đã đối chiếu.
    Input: danh sách tên thuốc (list[str]). Output: trạng thái, kết quả và nguồn; không tác động ra ngoài."""
    if not isinstance(drug_names, (list, tuple)) or not drug_names or any(
        not isinstance(name, str) or not name.strip() for name in drug_names
    ):
        return {"status": "invalid_input", "message": "Cần danh sách gồm ít nhất một tên thuốc hợp lệ.", "results": []}
    names = [name.strip() for name in drug_names]
    return {
        "status": "no_verified_data",
        "drug_names": names,
        "message": "Chưa có dữ liệu tương tác được đối chiếu trong bản thử này. Kết quả không xác nhận an toàn; hỏi dược sĩ trước khi phối hợp thuốc.",
        "results": [],
        "sources": [],
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
