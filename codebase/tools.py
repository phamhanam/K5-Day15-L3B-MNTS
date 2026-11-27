"""Read-only, source-bounded tools for the B2 medication support prototype.

The repository currently contains no reviewed medication or interaction dataset.
Accordingly lookup and interaction checks fail closed rather than invent facts.
These helpers do not diagnose, prescribe, or change a user's treatment.
"""
from tracing import tool, TOOLS  # noqa: F401


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
