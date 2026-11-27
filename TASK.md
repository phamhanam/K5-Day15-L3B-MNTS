# Kế hoạch phân công nhiệm vụ theo Checkpoint — Mini Hackathon AI K5 · Track B (B2) · Đội MNTS (L3B)

> **Repo nhóm:** `K5-Day15-L3B-MNTS` (Public, copy từ `starter-repo/`)
> **Hướng đề tài:** **Track B — B2 · Kiểm tra tương tác thuốc và lịch uống**
> **Tài liệu đối chiếu:** `tracks/track-b-healthcare.md`, `02-guide.md`, `03-rubric.md`, `AGENTS.md`
> **Mốc làm việc:**
> - **Thứ Sáu 27/11/2026:** `09:00` Zoom Kick-off · `16:00–19:30` Tại lớp (`H209 / H210 / C401`) · `CP1 (17:00)` · `CP2 (19:30)`
> - **Thứ Bảy 28/11/2026:** `10:00` CP3 (Online) · `14:00` Tập trung phòng thi L3B (`C401 / D303 / D304 / D305` — tra trên Cổng Tra Cứu) · `14:30` CP4 · `14:30–18:00` Vòng 1 & Vòng 2
> **Deadline nộp bài:**
> - **Form 1 (Đăng ký đội):** Trước `16:30` Thứ Sáu 27/11 (GMT+7) — Đội trưởng Phạm Hà Nam (`2A202604023`) nộp
> - **Form 2 (Checkpoint CP1–CP4):** `17:00 T6` (CP1) · `19:30 T6` (CP2) · `10:00 T7` (CP3) · `14:30 T7` (CP4)
> - **Khóa Repo cuối (không cần nộp thêm Form):** `23:59` Thứ Bảy 28/11 (GMT+7)

---

## 1. Bảng phân vai & định danh nhánh

| STT | Thành viên | MSSV | GitHub | Vai trò CP0–CP2 | Vai trò CP3–Khóa Repo | Tiền tố nhánh | File phụ trách / báo cáo |
| --: | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Phạm Hà Nam** *(Đội trưởng)* | `2A202604023` | `@phamhanam` | **Product, Spec, Form & Lát cắt B2** | **Slide, Video Demo, Pitch & Spec §10** | `nam/...` | `TEAMS.md`, `canvas.md`, `spec.md`, `AGENTS.md`, `slides/outline.md`, `demo-slides.pdf`, `reflection/nam.md` |
| 2 | **Nguyễn Đức Mạnh** | `2A202603731` | `@nguyenducmanh-itus` | **Giả thuyết Pain & Data thuốc/tương tác chuẩn nguồn** | **Evidence Discovery (Review/PV người thân/Survey) & Validation** | `manh/...` | `evidence/*`, `data/DATA_CARD.md`, `validation/log.md`, `reflection/manh.md` |
| 3 | **Vũ Trọng Thắng** | `2A202604022` | `@Thangvipsv4` | **Codebase Khung, Tools B2 & Mock Flow** | **Nối AI thật (`call_model`), Tối ưu L2 & AI Usage** | `thang/...` | `codebase/app.py`, `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`, `docs/ai-usage.md`, `reflection/thang.md` |
| 4 | **Đào Đức Sơn** | `2A202604105` | `@b1rdal` | **Benchmark B2 (tương tác nặng/nhẹ, sai tên, từ chối) & Metrics** | **Eval L1/L2, Cost Simulate & QA Repo** | `son/...` | `eval/*`, `cost/personas.yaml`, `cost/cost-estimate.md`, `reflection/son.md` |

> **Lưu ý chuyển giao:**
> - **Khóa chuẩn (`19:30` T6 – CP2):** **Nam** và **Sơn** chốt cứng chuẩn `"đạt"` bằng số trong `spec.md §7` và `eval/metric_spec.yaml`. Sau `19:30` T6 **cấm sửa 2 mục này**.
> - **Chuyển giao Eval L1 → Code L2 (sáng T7):** **Sơn** chạy `python run.py eval` ra `eval/run-1.csv`, gửi các ca trượt cho **Thắng** sửa `codebase/` trước `12:30` T7 để Sơn chạy lại Lượt 2 và `simulate` trước CP4 (`14:30`).

---

## 2. Quy ước Git Branch & Pull Request

### 2.1. Quy trình chuẩn cho mỗi task
```bash
git checkout main
git pull origin main
git checkout -b <tien-to>/<cp>-<mo-ta-ngan>
python run.py check
git status
git add <cac-file-da-sua>
git commit -m "<type>(<scope>): <mo-ta-ngan>"
git push -u origin <tien-to>/<cp>-<mo-ta-ngan>
```

### 2.2. Nguyên tắc chống xung đột (File Ownership)

| File / Thư mục | Owner | Ghi chú tránh xung đột |
| --- | --- | --- |
| `TEAMS.md`, `canvas.md`, `AGENTS.md`, `spec.md` | **Nam** | Chỉ Nam ghi; thành viên gửi góp ý qua chat/PR comment. Dòng 1 `TEAMS.md` phải là `Phạm Hà Nam \| 2A202604023`. |
| `evidence/*`, `data/DATA_CARD.md`, `validation/log.md` | **Mạnh** | Không sửa `hypothesis.md` sau khi đã thu thập bằng chứng. Data thuốc/tương tác phải ghi nguồn công khai từng mục trong `DATA_CARD.md`. |
| `codebase/app.py`, `agent.py`, `tools.py`, `ai.py` | **Thắng** | `ai.py` (`call_model`) là chỗ duy nhất gọi model; `tools.py` dùng `@tool`; `agent.py` xuất `answer(text) -> {"output": str}`. |
| `eval/benchmark.csv`, `metric_spec.yaml`, `README.md`, `report.md`, `cost/*` | **Sơn** | Không ai sửa `expected` trong `benchmark.csv` cho khớp output code. |
| `eval/run-*.csv`, `traces/run-*.jsonl`, `cost/simulate-*.csv` | **Sơn** *(tự động)* | Không sửa tay file kết quả đã chạy (trừ điền cột `pass`, `ghi_chu`). |
| `slides/outline.md`, `demo-slides.pdf` | **Nam** | `demo-slides.pdf` đặt ở **thư mục gốc repo** trước `14:30` T7. |
| `docs/ai-usage.md` | **Thắng** | Cả nhóm gửi thông tin dùng AI cho Thắng tổng hợp trước `23:00` T7. |
| `reflection/*.md` | **Mỗi người 1 file** | `nam.md`, `manh.md`, `thang.md`, `son.md` (copy từ `reflection/TEMPLATE.md`). |

### 2.3. Quy tắc cấm
- **KHÔNG** sửa 4 file khung BTC: `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py`, `run.py`.
- **KHÔNG** commit `.env`, API key, bệnh án/đơn thuốc/ảnh hộp thuốc thật hay PII lên GitHub (**TRỪ 10 ĐIỂM**).
- **KHÔNG** sửa `spec.md §7`, `eval/metric_spec.yaml` sau CP2 (`19:30` T6) hoặc xóa câu trượt (**0 ĐIỂM** khối đánh giá).
- **KHÔNG** tự sinh dữ liệu thuốc/tương tác bằng AI rồi dùng luôn mà không đối chiếu tờ HDSD thuốc / Dược thư Quốc gia VN / hướng dẫn Bộ Y tế.
- **KHÔNG** để AI chẩn đoán bệnh, kê đơn, tư vấn liều, khuyên đổi/bỏ thuốc; **100% ca dấu hiệu nguy hiểm** phải báo đi khám/gọi 115 ngay.

---

## 3. Tổng quan tiến độ & lịch trình

| Giai đoạn / CP | Khung giờ / Mốc | Đầu ra chính | Điều kiện qua cổng |
| --- | --- | --- | --- |
| **CP0 · Khởi động** | `09:00` – trước `16:30` T6 | Repo Public, Form 1, lịch PV người thân/dược sĩ | Cài xong môi trường; Nam nộp Form 1 trước `16:30`; Mạnh hẹn gọi người thân uống nhiều thuốc (tối T6). |
| **CP1 · Đội & Canvas (3đ)** | `16:00 – 17:00` T6 | `TEAMS.md`, `canvas.md`, `hypothesis.md` | `python run.py check` **OK**; `canvas.md` không chữ AI, chốt lát cắt B2; Form 2 (CP1) trước `17:00`. |
| **CP2 · Spec, Data & Mock (4đ)** | `17:00 – 19:30` T6 | `spec.md` (`§4`, `§7`), `DATA_CARD.md`, `benchmark.csv` (≥10), `codebase/` mock | Khóa chuẩn đạt B2 trong `spec.md §7`; data thuốc/tương tác có nguồn công khai; `python run.py` chạy thông; Form 2 (CP2) trước `19:30`. |
| **CP3 · Pain, AI thật & L1 (4đ)** | `19:30` T6 – `10:00` T7 | `evidence/summary.md`, `ai.py` thật, `benchmark.csv` (20–30), `run-1.csv`, Video 30s | ≥1 nguồn pain + ≥5 trích dẫn ẩn tên; bộ 20–30 câu (≥5 `kho`, ≥2 `tu_choi`); gọi AI thật + Video 30s mở ẩn danh; Form 2 (CP3) trước `10:00`. |
| **CP4 · L2, Cost & Slide (4đ)** | `10:00 – 14:30` T7 | `report.md` (L1→L2), `simulate`, `cost-estimate.md`, `demo-slides.pdf`, Video dự phòng | Có mặt phòng L3B lúc `14:00`; chạy `simulate` ≥50 phiên; `demo-slides.pdf` ở gốc repo; Form 2 (CP4) trước `14:30`. |
| **Vòng 1 & Vòng 2** | `14:30 – 18:00` T7 | Pitch live, Form 3 (`15:47`), Form 4 (`17:34`) | Bám giờ cứng (V1: 9p, V2: 12p); mạng/API lỗi >30s bật ngay Video dự phòng. |
| **Khóa Repo Cuối** | `18:00 – 23:59` T7 | `spec.md §10`, `docs/ai-usage.md`, 4 file `reflection/*.md` | Push sạch trước `23:59` T7. |

---

## 4. Phân công chi tiết từng Checkpoint (Hướng B2)

### CP0 (`09:00` – trước `16:30` Thứ Sáu 27/11)
- [ ] **Phạm Hà Nam** (`@phamhanam`): Nộp **Form 1** (Lớp `L3B`, Đội `MNTS`, đủ 4 MSSV). Kiểm tra tên đội `MNTS` hiện trên Dropdown Form 2 & Cổng Tra Cứu.
- [ ] **Nguyễn Đức Mạnh** (`@nguyenducmanh-itus`): Nhắn hẹn người thân đang uống nhiều thuốc/người sắp thuốc hộ để gọi `10–15p` tối T6; hẹn dược sĩ (nếu có); lên danh sách app nhà thuốc để đào review công khai.
- [ ] **Vũ Trọng Thắng** (`@Thangvipsv4`): Cài `requirements.txt`, đọc `AGENTS.md` & `docs/connect-model.md`, tạo `.env` local.
- [ ] **Đào Đức Sơn** (`@b1rdal`): Đọc `03-rubric.md`, chạy thử `python run.py check`.

### CP1 (`16:00 – 17:00` Thứ Sáu 27/11 · 3đ)
- [ ] **Nam** (`nam/cp1-teams-canvas`): Điền `TEAMS.md` (Nam dòng 1), `canvas.md` (bài toán người con/người bệnh uống nhiều thuốc dễ nhầm lịch và quên kiểm tương tác — **không dùng chữ AI**, lát cắt B2 1 câu), cập nhật quy ước `AGENTS.md`. Chạy `python run.py check` → **OK**, kiểm Repo ở Tab Ẩn Danh → Nộp **Form 2 (CP1)** trước `17:00`.
- [ ] **Mạnh** (`manh/cp1-hypothesis`): Viết `evidence/hypothesis.md` **TRƯỚC** khi thu thập bằng chứng.
- [ ] **Thắng** (`thang/cp1-tools-plan`): Chốt 4 tool B2 trong `codebase/tools.py`: `lookup_drug`, `check_interactions`, `build_schedule`, `handoff_to_pharmacist` (+ `check_red_flags` / `advise_see_doctor`).
- [ ] **Sơn** (`son/cp1-qa`): Review PR `nam/cp1-teams-canvas` và chạy `python run.py check` xác nhận **OK**.

### CP2 (`17:00 – 19:30` Thứ Sáu 27/11 · 4đ)
- [ ] **Nam** (`nam/cp2-spec`): Viết `spec.md §4` (Input → Kiểm dấu hiệu nguy hiểm → `lookup_drug` & `check_interactions` → Cảnh báo/Chuyển dược sĩ/Xếp lịch) và **khóa cứng `spec.md §7`** (100% ca dấu hiệu nguy hiểm bảo đi khám/115 ngay; 100% tương tác nặng trong data được báo; 100% ca dụ chẩn đoán/hỏi liều/đòi thuốc kê đơn bị từ chối; đo thêm tỷ lệ chuyển dược sĩ thừa). Nộp **Form 2 (CP2)** trước `19:30`.
- [ ] **Mạnh** (`manh/cp2-datacard`): Dựng dữ liệu giả có seed cho B2 (thuốc, hoạt chất, cách uống, cặp tương tác nhẹ/vừa/nặng, thuốc cần cách giờ, dấu hiệu nguy hiểm) và ghi **nguồn công khai từng mục** (tờ HDSD, Dược thư Quốc gia VN, Bộ Y tế) vào `data/DATA_CARD.md`.
- [ ] **Thắng** (`thang/cp2-mock-flow`): Cài đặt các `@tool` ở `tools.py` + `answer(text)` ở `agent.py`, đảm bảo `python run.py` chạy hết luồng (mock OK).
- [ ] **Sơn** (`son/cp2-eval-init`): Viết `eval/benchmark.csv` (≥10 câu đầu) và `eval/metric_spec.yaml` (≥3 metric khớp `spec.md §7`), chạy `python run.py check` và `python run.py eval --try`.

### CP3 (`19:30` T6 – `10:00` Thứ Bảy 28/11 · 4đ)
- [ ] **Mạnh** (`manh/cp3-evidence`): Thu thập ≥1 nguồn pain (đào review app nhà thuốc/Google Maps vào `evidence/data-mining.md` hoặc ≥3 phỏng vấn người thân sắp thuốc hộ/dược sĩ vào `evidence/interviews/` hoặc ≥20 khảo sát vào `evidence/survey/`) → tổng hợp `evidence/summary.md` kèm **≥5 trích dẫn nguyên văn ẩn tên/bệnh**.
- [ ] **Thắng** (`thang/cp3-real-ai`): Nối model **AI thật** trong `codebase/ai.py` (`call_model()` giữ `@model_call`, token từ `usage` API, key trong `.env`).
- [ ] **Sơn** (`son/cp3-eval-run1`): Mở rộng `eval/benchmark.csv` lên **20–30 câu** gồm các tình huống khó B2 (tương tác nặng lẫn trong 5–7 thuốc, tương tác nhẹ không làm hoảng, 2 thuốc uống cách giờ, sai chính tả/biệt dược, thuốc ngoài data, "uống gấp đôi được không", red flags ẩn trong mô tả dài, dụ chẩn đoán/kê đơn). Chạy `python run.py eval` (Lượt 1) + `score`, ghi `eval/README.md`, gửi câu trượt cho Thắng.
- [ ] **Nam** (`nam/cp3-video`): Quay **Video 30s AI thật**, kiểm Tab Ẩn Danh → Nộp **Form 2 (CP3)** trước `10:00`.

### CP4 (`10:00 – 14:30` Thứ Bảy 28/11 · 4đ)
- [ ] **Thắng** (`thang/cp4-improve`): Sửa đúng 1 cải tiến rõ ràng từ các ca trượt Lượt 1 trong `codebase/` trước `12:30`.
- [ ] **Sơn** (`son/cp4-eval2-cost`): Chạy `python run.py eval` (Lượt 2) + viết `eval/report.md` (L1→L2). Cập nhật `cost/personas.yaml` (ít: người trẻ khỏe; vừa: phụ huynh có con nhỏ; nhiều: con sắp thuốc cho cha mẹ bệnh mạn tính + chi phí dược sĩ trực ca chuyển) → chạy `python run.py simulate` (≥50 phiên) → viết `cost/cost-estimate.md`.
- [ ] **Mạnh** (`manh/cp4-validation`): Gửi trích dẫn pain cho slide; *(bonus nếu kịp)* mời 1–2 người ngoài thử ca giả định và ghi `validation/log.md`.
- [ ] **Nam** (`nam/cp4-slides`): Làm `slides/outline.md` → xuất **`demo-slides.pdf` ở thư mục gốc repo**; quay **Video Demo dự phòng**; có mặt tại phòng L3B lúc `14:00`; nộp **Form 2 (CP4)** trước `14:30`.

### Vòng 1, Vòng 2 (`14:30 – 18:00` T7) & Khóa Repo (`23:59` T7)
- [ ] **Vòng 1 & 2:** Nam pitch & điền Form 3 (`15:47`), Form 4 (`17:34`); Thắng điều khiển demo (lỗi >30s bật Video dự phòng); Sơn & Mạnh trả lời ca khó/Q&A.
- [ ] **Khóa Repo (`23:59` T7):** Nam cập nhật `spec.md §10`; Thắng tổng hợp `docs/ai-usage.md`; cả 4 bạn viết riêng `reflection/nam.md`, `reflection/manh.md`, `reflection/thang.md`, `reflection/son.md`; Sơn QA cuối trước `23:45`.

---

## 5. Checklist QA cuối cùng

```bash
python run.py check
python run.py eval
python run.py score eval/run-2.csv
python run.py simulate
git status
```

- [ ] **AI thật:** `call_model()` gọi model thật, token lấy từ `usage` API; không hardcode.
- [ ] **An toàn B2:** 100% ca red flags báo đi khám/115 ngay; 100% tương tác nặng trong data được báo; 100% ca dụ chẩn đoán/hỏi liều/kê đơn bị từ chối.
- [ ] **Bằng chứng & Nguồn:** `evidence/summary.md` đủ ngưỡng + ≥5 trích dẫn ẩn tên; `data/DATA_CARD.md` có nguồn y khoa công khai từng mục.
- [ ] **Bảo mật & Khóa Repo:** Không lộ `.env`/API key/PII; `demo-slides.pdf` ở gốc repo; đủ `spec.md §10`, `docs/ai-usage.md`, 4 file `reflection/`.
