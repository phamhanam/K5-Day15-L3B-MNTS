# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Coding agent (Codex) | Gợi ý khung hàm `@tool` (`tools.py`), tích hợp `call_openrouter` (`ai.py`), luồng `answer(text)` (`agent.py`) và unit test (`tests/`) | Thắng rà soát hợp đồng `@tool`/`@model_call`, sửa nhận diện danh sách thuốc (`PR #14`), tách bỏ `dotenv`/lộ key và chạy `unittest` đạt | Vũ Trọng Thắng |
| Prompt / thiết kế lời gọi mô hình | Trợ lý AI / Coding agent | Gợi ý system prompt an toàn y tế (cấm chẩn đoán, kê đơn, tự đoán liều) và cấu trúc `tool_context` JSON | Thắng & Nam kiểm tra ràng buộc fail-closed (`no_verified_data`), bỏ qua lời tự xưng bác sĩ, thêm kiểm tra thiếu chỉ dẫn lịch | Vũ Trọng Thắng, Phạm Hà Nam |
| Đào data (viết script đếm, gợi ý nhãn) | Trợ lý AI | Hỗ trợ mã hóa, phân loại nhận xét review công khai trên App Store / Google Play (`Long Châu`, `Medisafe`) | Mạnh tự kiểm tay toàn bộ `17` review (`10` Long Châu + `7` Medisafe trong `evidence/data-mining.md`), khớp `17/17`, xóa thông tin nhận diện và ghi rõ giới hạn mẫu | Nguyễn Đức Mạnh |
| Rà câu hỏi phỏng vấn / khảo sát | Trợ lý AI | Chỉ rà câu dẫn dắt khảo sát hành vi, tránh hỏi bệnh lý cá nhân | Mạnh kiểm tra không thu PII/đơn thuốc thật; giữ nguyên dữ liệu trả lời thật `n=20` không sửa | Nguyễn Đức Mạnh |
| Viết câu thử (benchmark) | Trợ lý AI (hỗ trợ diễn đạt một số tình huống) | Gợi ý biến thể câu hỏi khó, viết sai chính tả và câu tấn công giả danh bác sĩ (`tu_choi`) | Sơn tự xây dựng và kiểm tay đủ `27` câu trong `eval/benchmark.csv`: `13` câu dựa nguồn tài liệu thật (`data_that`), `14` câu `tu_viet` (gắn rõ `source`), khóa ngưỡng với `spec.md §7` | Đào Đức Sơn |
| Sinh data `synthetic` (nếu có) | Trợ lý AI (hỗ trợ format JSON) | Định dạng cấu trúc JSON cho `data/b2_seed.json` và khung lời thoại ca demo giả lập | Seed `MNTS-B2-CP2-v1` · Mạnh kiểm tay `2` dòng `synthetic` (`CASE-SYN-001`, `CASE-SYN-002`) và đối chiếu thủ công toàn bộ `8` thuốc + `3` cặp tương tác với link MedlinePlus/DailyMed/Bộ Y tế | Nguyễn Đức Mạnh |
| Chấm cột `pass` bằng LLM (nếu có) | Coding agent | Đối chiếu nháp `27` output với `pass_criterion` ở giai đoạn CP3 | Kiểm tra thủ công `5` câu thử đại diện trong nhóm, khớp `4/5` (ghi tại `eval/README.md`); Sơn rà soát lại và chạy `python run.py score` cho cả `run-1.csv` và `run-2.csv` | Đào Đức Sơn |
| Slide, văn bản | ChatGPT / Gemini | Gợi ý cấu trúc `TASK.md`, dàn ý `spec.md`, mã HTML/CSS cho `slides/demo-slides.html` và kịch bản thuyết trình | Nam tự sửa lỗi cú pháp Mermaid, đồng bộ quy tắc chỉ xếp lịch khi có chỉ dẫn xác minh, đối chiếu từng số liệu trong `demo-slides.pdf` với `evidence/summary.md`, `eval/report.md`, `cost/cost-estimate.md` | Phạm Hà Nam |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
