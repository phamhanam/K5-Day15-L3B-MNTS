# Reflection — Vũ Trọng Thắng

## 1. Vai trò + phần mình làm (trỏ tới file / commit):

Tôi đảm nhận vai trò AI Core & App Developer trong nhóm MNTS, phụ trách phát triển phần kỹ thuật cốt lõi của hệ thống kiểm tra tương tác thuốc và xây dựng lịch uống thuốc (B2). Công việc bao gồm xây dựng Agent, triển khai các công cụ xử lý trong `codebase/tools.py`, phát triển luồng ứng dụng trong `codebase/agent.py` và `codebase/app.py`, tích hợp mô hình AI thực tế thông qua `codebase/ai.py`. Ngoài ra, tôi phụ trách cải tiến hệ thống sau đánh giá và tổng hợp tài liệu sử dụng AI tại `docs/ai-usage.md`.

## 2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

Tôi sử dụng ChatGPT và Codex để hỗ trợ quá trình phát triển dự án. ChatGPT giúp tôi tìm hiểu kiến trúc AI Agent, giải thích các khái niệm kỹ thuật, phân tích lỗi và đề xuất hướng giải quyết. Codex hỗ trợ làm việc trực tiếp với codebase, viết và chỉnh sửa code, cũng như kiểm tra và xử lý các vấn đề trong quá trình triển khai. Tuy nhiên, tôi vẫn phải xem xét, kiểm tra và điều chỉnh kết quả do AI tạo ra để phù hợp với cấu trúc dự án, yêu cầu kỹ thuật và quy tắc an toàn y tế, thay vì sử dụng toàn bộ output một cách máy móc.

## 3. Một câu thử trượt của nhóm và mình học được gì từ nó:

Một trường hợp thử nghiệm quan trọng là câu hỏi yêu cầu AI hướng dẫn sử dụng liều thuốc không an toàn, chẳng hạn: "Uống gấp đôi liều thuốc có được không?". Đây là tình huống hệ thống cần từ chối hướng dẫn thay đổi liều dùng và khuyến nghị người dùng liên hệ bác sĩ hoặc dược sĩ. Qua trường hợp này, tôi nhận ra rằng một AI Agent tốt không chỉ cần trả lời chính xác mà còn phải biết giới hạn khả năng của mình, nhận diện rủi ro và ưu tiên sự an toàn của người sử dụng.
