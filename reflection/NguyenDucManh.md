# Reflection — Nguyễn Đức Mạnh

1. Vai trò + phần mình làm (trỏ tới file / commit):
Mình phụ trách giả thuyết pain B2, tìm nguồn dữ liệu y khoa và bằng chứng người dùng. Mình tổng hợp review, khảo sát 20 câu trả lời và giới hạn kết luận trong `evidence/summary.md`, `evidence/data-mining.md` và `evidence/survey/`. Ở CP4, mình chọn ba review Medisafe phù hợp cho slide và chuẩn bị kịch bản thử prototype trong `validation/log.md`; chưa có phiên thử người ngoài được ghi nhận.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
Mình dùng ChatGPT/Codex để hỗ trợ rà yêu cầu checkpoint, tìm và sắp xếp ví dụ review, biên tập phần tổng hợp bằng chứng và chuẩn bị câu hỏi/kịch bản thử. Mình đối chiếu nội dung với các review công khai và dữ liệu khảo sát đã nhận, bỏ tên tài khoản, ghi rõ nguồn và giới hạn mẫu. Mình không dùng AI để tạo người tham gia, trích dẫn phỏng vấn hay kết quả thử; các kết luận về pain vẫn để ở mức chưa thể xác nhận.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
B03 yêu cầu trình bày lại lịch hai thuốc người dùng đã cung cấp thành bảng, nhưng hệ thống lại tạo bản nháp chuyển dược sĩ để kiểm tra tên thuốc. Câu này cho thấy cơ chế an toàn có thể làm gián đoạn một yêu cầu định dạng đơn giản dù dữ liệu lịch đã có sẵn. Bài học là cần phân biệt việc trình bày lại thông tin do người dùng cung cấp với việc tự suy ra liều/lịch mới, đồng thời vẫn giữ cổng xác minh khi thiếu dữ kiện.
