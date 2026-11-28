# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): người trẻ khỏe 30% × 0,5 phiên/tháng × 1 lượt hỏi; phụ huynh có con nhỏ 30% × 1,5 phiên/tháng × 2 lượt hỏi; người con chăm sóc cha mẹ bệnh mạn tính 40% × 6 phiên/tháng × 2 lượt hỏi. Tần suất chọn trong khoảng ở `spec.md` §2; tỷ trọng và lượt hỏi là tự ước tính. Khảo sát n=20 chưa đo cơ cấu persona.
- **Quy mô pilot** 3 kịch bản: thấp 100 · cơ sở 500 · cao 1.000 người dùng hoạt động/tháng (tự ước tính). Trung bình 3 phiên/người/tháng.
- **Giá standard trả phí** (USD/1 triệu token vào/ra): Gemini 3.5 Flash-Lite $0,30/$2,50; Gemini 3.1 Pro Preview $2,00/$12,00 (prompt ≤200k token). Nguồn: [bảng giá chính thức Google](https://ai.google.dev/gemini-api/docs/pricing), xem 28/11/2026. Tỷ giá quy đổi 26.000 VND/USD (tự ước tính).
- **Tỉ lệ đạt** dùng để tính: 18/27 (66,7%) — lượt `run-2@20261128-114752` (lượt 2).
- Đo token bằng OpenRouter `openrouter/free` (model thực tế ghi trong CSV), tính giá Gemini 3.5 Flash-Lite và Gemini 3.1 Pro Preview.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-115532` · 50 phiên (85 lượt hỏi) · seed 42. Trace: `traces/simulate-1.jsonl`. Thành viên Sơn chạy trực tiếp từ PowerShell sau sự cố theo dõi tiến trình trong môi trường agent.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 15 | 1 | 84 | 225 | 0.3 | 3.3 |
| dung_vua | 14 | 2 | 208 | 811 | 1.2 | 5.9 |
| dung_nhieu | 21 | 2 | 153 | 569 | 0.8 | 5.4 |

Bảng dưới đây lấy nguyên số từ `cost/simulate-1-summary.md`.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (500 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.5-flash-lite (vào 0.3 · ra 2.5 $/1M) — nếu MỌI token tính giá model này | $0.0014 (≈ 36 ₫) | $0.0021 (≈ 54 ₫) | $0.0012 (≈ 32 ₫) | $0.4551 (≈ 11.832 ₫) | $2.28 (≈ 59.160 ₫) | $4.55 (≈ 118.321 ₫) | $0.0046 (≈ 118 ₫) |
| gemini-3.1-pro-preview (vào 2.0 · ra 12.0 $/1M) — nếu MỌI token tính giá model này | $0.0067 (≈ 174 ₫) | $0.0100 (≈ 261 ₫) | $0.0059 (≈ 154 ₫) | $2.21 (≈ 57.485 ₫) | $11.05 (≈ 287.423 ₫) | $22.11 (≈ 574.846 ₫) | $0.0221 (≈ 575 ₫) |

Mô phỏng đo token từ 8 model thực tế do `openrouter/free` chọn; L2 đo trên 5 model. Xem danh sách trong file summary. Chi phí của từng model thực đo chưa định giá riêng; bảng trên áp hai mức giá trả phí giả định lên token đã đo, không phải chi phí thực tế của hai model Gemini. L2 và mô phỏng cùng router nhưng tập model khác nhau, nên tỷ lệ đạt L2 dùng để ước tính có giới hạn.

50/50 phiên có kết quả, 0 lỗi phiên. Trace ghi 7 lần gọi model gặp HTTP 429; workflow trả kết quả dự phòng nên không làm hỏng phiên. Chi phí đo được có thể thấp hơn khi toàn bộ lượt gọi model thành công. Cần đo lại trên model trả phí ổn định trước khi triển khai.

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): khoảng 60 phút tra cứu/đối chiếu có thể tiết kiệm cho người sắp thuốc hộ (4 lần × 15 phút, tự ước tính); chưa đo thực tế.
- Chi phí / người / tháng (cơ sở): 118 VND (Flash-Lite) hoặc 575 VND (Pro Preview) cho model; cộng nhân công giả định 5.000 VND thì lần lượt khoảng 5.118 và 5.575 VND.
- **Kết luận một dòng — đáng làm không:** Đáng tiếp tục thử nghiệm có giám sát vì chi phí dự báo thấp so với thời gian tra cứu có thể tiết kiệm, nhưng cần cải thiện từ chối an toàn và xác minh hiệu quả thực tế trước khi triển khai rộng.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Độ nhạy theo model: ở quy mô cơ sở, giá Flash-Lite giảm chi phí model từ 287.423 xuống 59.160 VND/tháng (xấp xỉ 79,4%); chưa đo chất lượng trên hai model trả phí.
- Chi phí ngoài model: hosting và lưu trữ chưa định giá. Chi phí giờ công dược sĩ giả định 100.000 VND/giờ, 5 phút/ca chuyển, 20% phiên cần chuyển (tự ước tính, tham khảo 4/20 người trong khảo sát chọn hỏi dược sĩ/nhân viên y tế; không phải tỷ lệ chuyển thực đo). Với 3 phiên/người/tháng, chi phí nhân công dự kiến 5.000 VND/người/tháng, tương ứng 500.000 / 2.500.000 / 5.000.000 VND/tháng ở ba quy mô. Một phiên được chuyển có chi phí khoảng 8.333 VND.
- Tổng chi phí model + nhân công dược sĩ (chưa gồm hosting/lưu trữ, VND/tháng):

| Quy mô | Flash-Lite | Pro Preview |
|---|---:|---:|
| 100 người | 511.832 | 557.485 |
| 500 người | 2.559.160 | 2.787.423 |
| 1.000 người | 5.118.321 | 5.574.846 |
