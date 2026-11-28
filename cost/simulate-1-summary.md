# Tóm tắt mô phỏng simulate-1@20261128-115532

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 15 | 1 | 84 | 225 | 0.3 | 3.3 |
| dung_vua | 14 | 2 | 208 | 811 | 1.2 | 5.9 |
| dung_nhieu | 21 | 2 | 153 | 569 | 0.8 | 5.4 |

Tỉ lệ đạt dùng để tính: 18/27 (67%) — lượt run-2@20261128-114752

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from). ⚠️ Lượt này chạy bằng liquid/lfm-3-1.7b:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, nvidia/nemotron-3-ultra-550b-a55b:free, nvidia/nemotron-3.5-lightning:free, recursive/flint-v1.0:free, mô phỏng đo trên baidu/ernie-5.5-flash-preview:free, liquid/lfm-3-1.7b:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, nvidia/nemotron-3-ultra-550b-a55b:free, nvidia/nemotron-3.5-lightning:free, nvidia/nemotron-3.5-super-vl:free, particle-ai/particle-1:free, recursive/flint-v1.0:free — khác model.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (500 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Thực đo — mỗi model giá riêng** | chưa tính: thiếu giá của baidu/ernie-5.5-flash-preview:free, liquid/lfm-3-1.7b:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, nvidia/nemotron-3-ultra-550b-a55b:free, nvidia/nemotron-3.5-lightning:free, nvidia/nemotron-3.5-super-vl:free, particle-ai/particle-1:free, recursive/flint-v1.0:free trong `prices` | — | — | — | — | — |  — |
| gemini-3.5-flash-lite (vào 0.3 · ra 2.5 $/1M) — nếu MỌI token tính giá model này | $0.0014 (≈ 36 ₫) | $0.0021 (≈ 54 ₫) | $0.0012 (≈ 32 ₫) | $0.4551 (≈ 11.832 ₫) | $2.28 (≈ 59.160 ₫) | $4.55 (≈ 118.321 ₫) | $0.0046 (≈ 118 ₫) |
| gemini-3.1-pro-preview (vào 2.0 · ra 12.0 $/1M) — nếu MỌI token tính giá model này | $0.0067 (≈ 174 ₫) | $0.0100 (≈ 261 ₫) | $0.0059 (≈ 154 ₫) | $2.21 (≈ 57.485 ₫) | $11.05 (≈ 287.423 ₫) | $22.11 (≈ 574.846 ₫) | $0.0221 (≈ 575 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: baidu/ernie-5.5-flash-preview:free, liquid/lfm-3-1.7b:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, nvidia/nemotron-3-ultra-550b-a55b:free, nvidia/nemotron-3.5-lightning:free, nvidia/nemotron-3.5-super-vl:free, particle-ai/particle-1:free, recursive/flint-v1.0:free. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 26.000 ₫ ((tự ước tính) tỷ giá dùng cho kịch bản lập kế hoạch, không phải tỷ giá giao dịch).
