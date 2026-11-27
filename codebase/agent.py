"""B2 Healthcare workflow; the red-flag gate runs before any model call."""
from ai import call_model
from tools import check_red_flags

SYSTEM = """Bạn là trợ lý hỗ trợ thông tin thuốc, không phải nhân viên y tế.
Không chẩn đoán, kê đơn, đề xuất hoặc thay đổi liều, khuyên ngừng thuốc, hay khẳng định phối hợp thuốc an toàn.
Chỉ nêu dữ kiện đã được cung cấp/đối chiếu; bản thử hiện chưa có dữ liệu thuốc hoặc tương tác đã xác minh.
Khi thiếu thông tin hoặc căn cứ, nói rõ giới hạn và khuyên hỏi bác sĩ/dược sĩ.
Nếu người dùng mô tả tình trạng khẩn cấp, hướng dẫn gọi 115/đến cấp cứu ngay.
Trả lời bằng tiếng Việt, ngắn gọn và không tạo cảm giác đã kiểm tra dữ liệu chưa có."""


def answer(text: str) -> dict:
    """Return user-facing text as {"output": str}; screen emergency cues first."""
    if not isinstance(text, str):
        return {"output": "Vui lòng nhập nội dung bằng văn bản. Nếu đang nguy cấp, gọi 115 hoặc đến cơ sở cấp cứu ngay."}

    red_flag_result = check_red_flags(text)
    if red_flag_result["urgency"] == "emergency":
        return {"output": red_flag_result["message"]}

    prompt = (
        "Kết quả sàng lọc dấu hiệu nguy hiểm: " + red_flag_result["message"] +
        "\nCăn cứ dữ liệu thuốc/tương tác đã xác minh: hiện không có dữ liệu trong bản thử."
        "\nĐầu vào của người dùng:\n" + text
    )
    reply = call_model(SYSTEM, prompt)
    return {"output": reply["text"]}
