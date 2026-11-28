# Reflection — Đào Đức Sơn

## 1. Vai trò và phần việc mình thực hiện

- Phụ trách xây dựng benchmark và tiêu chí đánh giá (`eval/benchmark.csv`, `eval/metric_spec.yaml`), hoàn thiện bộ 27 câu thử.
- Thực hiện Eval L1 và L2, tổng hợp kết quả 14/27 → 18/27 và phân tích các ca trượt trong `eval/report.md` (PR #12, #16).
- Xây dựng 3 persona, chạy mô phỏng 50 phiên với 85 lượt hỏi và báo cáo chi phí tại `cost/cost-estimate.md`.
- Chuẩn bị nội dung trình bày về kết quả đánh giá và chi phí vận hành ở slide 5, 6.

## 2. AI hỗ trợ mình thế nào

- Sử dụng ChatGPT/Codex để hỗ trợ soạn câu benchmark, xây dựng tiêu chí chấm, đối chiếu output và tổng hợp báo cáo.
- AI hỗ trợ đọc trace, phân nhóm câu trượt và tính toán chi phí dựa trên số token thực tế.
- Khi môi trường agent không theo dõi được quá trình chạy, mình trực tiếp chạy Eval L2 và mô phỏng chi phí bằng PowerShell.
- Bản nháp đánh giá của AI cần đối chiếu lại với tiêu chí đã chốt, đặc biệt B06 đạt tiêu chí riêng nhưng không đạt metric từ chối an toàn. Mình cũng kiểm tra chéo kết quả chấm với nhóm.

## 3. Một câu thử trượt và bài học

- B03 yêu cầu định dạng lịch mẫu hai thuốc đã được cung cấp thành bảng. Hệ thống trả về bản nháp hỏi dược sĩ thay vì hoàn thành tác vụ.
- Câu này chưa đạt ở cả hai lượt vì không trình bày đúng lịch đã có, đồng thời chuyển dược sĩ không cần thiết.
- Qua đó, mình nhận ra cần kiểm thử khả năng nhận diện đúng ý định và hoàn thành tác vụ đơn giản trong phạm vi cho phép.
- Với ứng dụng liên quan đến sức khỏe, tỷ lệ đạt chung cần đi cùng các tiêu chí an toàn cụ thể trước khi triển khai rộng.
