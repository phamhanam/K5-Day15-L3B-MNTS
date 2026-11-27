# Kế hoạch phân công nhiệm vụ theo Checkpoint — Mini Hackathon AI K5 · Track B (B2) · Đội MNTS (L3B)

> **Repo nhóm:** `https://github.com/phamhanam/K5-Day15-L3B-MNTS` (`K5-Day15-L3B-MNTS`, Public, copy từ `starter-repo/`)
> **Hướng đề tài:** **Track B — B2 · Kiểm tra tương tác thuốc và lịch uống**
> **Tài liệu đối chiếu:** `tracks/track-b-healthcare.md`, `02-guide.md`, `03-rubric.md`, `AGENTS.md`
> **Mốc làm việc / buổi học:**
> - **Thứ Sáu 27/11/2026:** `09:00` Zoom Kick-off · `16:00–19:30` Tại lớp (`H209 / H210 / C401`) · `CP1 (17:00)` · `CP2 (19:30)`
> - **Thứ Bảy 28/11/2026:** `10:00` CP3 (Online) · `14:00` Có mặt phòng thi L3B (`C401 / D303 / D304 / D305` — tra trên Cổng Tra Cứu) · `14:30` CP4 · `14:30–18:00` Vòng 1 & Vòng 2
> **Deadline nộp bài:**
> - **Form 1 (Đăng ký đội):** Trước `16:30` Thứ Sáu 27/11/2026 (GMT+7) — Đội trưởng Phạm Hà Nam (`2A202604023`) nộp
> - **Form 2 (Checkpoint CP1–CP4):** `17:00 T6` (CP1) · `19:30 T6` (CP2) · `10:00 T7` (CP3) · `14:30 T7` (CP4)
> - **Khóa Repo cuối (không cần nộp thêm Form):** `23:59` Thứ Bảy 28/11/2026 (GMT+7)

---

## 1. Bảng phân vai & định danh nhánh

| STT | Thành viên | MSSV | GitHub | Vai trò giai đoạn đầu (CP0–CP2) | Vai trò giai đoạn sau (CP3–Khóa Repo) | Tiền tố nhánh | File phụ trách / báo cáo |
| --: | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Phạm Hà Nam** *(Đội trưởng)* | `2A202604023` | `@phamhanam` | **Product, Spec, Form & Chốt lát cắt B2** | **Slide, Video Demo, Pitch & Spec §10** | `nam/...` | `TEAMS.md`, `canvas.md`, `spec.md`, `AGENTS.md`, `slides/outline.md`, `demo-slides.pdf`, `reflection/nam.md` |
| 2 | **Nguyễn Đức Mạnh** | `2A202603731` | `@nguyenducmanh-itus` | **Giả thuyết Pain & Data Y khoa chuẩn nguồn** | **Evidence Discovery (Review/PV/Survey) & Validation** | `manh/...` | `evidence/*`, `data/DATA_CARD.md`, `validation/log.md`, `reflection/manh.md` |
| 3 | **Vũ Trọng Thắng** | `2A202604022` | `@Thangvipsv4` | **Codebase Khung, Tools B2 & Mock Flow** | **Nối AI thật (`call_model`), Tối ưu L2 & AI Usage** | `thang/...` | `codebase/app.py`, `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`, `docs/ai-usage.md`, `reflection/thang.md` |
| 4 | **Đào Đức Sơn** | `2A202604105` | `@b1rdal` | **Benchmark B2 & Metric Spec (`run.py check`)** | **Eval L1/L2, Cost Simulate & QA PR** | `son/...` | `eval/benchmark.csv`, `eval/metric_spec.yaml`, `eval/README.md`, `eval/report.md`, `cost/personas.yaml`, `cost/cost-estimate.md`, `reflection/son.md` |

> **Lưu ý chuyển giao / đổi vai:**
> - **Duyệt PR bắt buộc:** Mọi thay đổi đều làm trên nhánh riêng theo tiền tố cá nhân, mở **Pull Request (PR)** vào `main` và phải được Reviewer chỉ định duyệt trước khi merge (không push thẳng vào `main`).
> - **Khóa chuẩn (`19:30` T6 – CP2):** **Nam** và **Sơn** chốt cứng chuẩn `"đạt"` bằng số trong `spec.md §7` và `eval/metric_spec.yaml`. Sau `19:30` T6 **cấm sửa 2 mục này**.
> - **Chuyển giao Eval L1 → Code L2 (sáng T7):** Sau khi **Sơn** merge PR Lượt 1 (`eval/run-1.csv`), bàn giao ngay các ca trượt cho **Thắng** sửa `codebase/` trước `12:30` T7 để Sơn chạy Lượt 2 và `simulate` trước CP4 (`14:30`).

---

## 2. Quy ước Git Branch & Pull Request

### 2.1. Quy trình chuẩn cho mỗi task (Bắt buộc qua PR)

```bash
# Bước 1: Cập nhật nhánh chính mới nhất
git checkout main
git pull origin main

# Bước 2: Tạo nhánh riêng theo quy ước
git checkout -b <tien-to>/<cp>-<mo-ta-ngan>
# Ví dụ: nam/cp1-teams-canvas | manh/cp2-datacard | thang/cp3-real-ai | son/cp2-eval-init

# Bước 3: Thực hiện đúng phần việc phụ trách & tự kiểm tra
python run.py check
git status
git add <cac-file-da-sua>
git commit -m "<type>(<scope>): <mo-ta-ngan>"

# Bước 4: Đẩy nhánh, mở Pull Request (PR), chờ Reviewer duyệt & merge vào main
git push -u origin <tien-to>/<cp>-<mo-ta-ngan>
# Mở PR qua GitHub Web UI hoặc GitHub CLI:
# gh pr create --base main --head <tien-to>/<cp>-<mo-ta-ngan> --title "<type>(<scope>): <mo-ta-ngan>" --body "Closes CP..."
# Sau khi PR được Reviewer approve và merge trên GitHub, kéo lại main về máy:
git checkout main
git pull origin main
```

### 2.2. Nguyên tắc chống xung đột (File Ownership)

| File / Thư mục | Chủ sở hữu ghi (Owner) | Ghi chú tránh xung đột |
| --- | --- | --- |
| `TASK.md`, `TEAMS.md`, `canvas.md`, `AGENTS.md` | **Nam** | Chỉ Nam ghi qua PR `nam/...`; kiểm tra dòng 1 `TEAMS.md` là `Phạm Hà Nam \| 2A202604023 \| Đội trưởng`. |
| `spec.md` (`§0–§10`) | **Nam** | Thắng gửi kiến trúc (`§4`), Sơn gửi ngưỡng đạt (`§7`), cả nhóm góp ý `§10` qua comment PR; chỉ Nam sửa `spec.md`. |
| `evidence/*`, `data/DATA_CARD.md`, `validation/log.md` | **Mạnh** | Mạnh quản lý qua PR `manh/...`; không sửa `hypothesis.md` sau khi đã thu thập bằng chứng. Data y khoa phải ghi nguồn công khai từng mục. |
| `codebase/app.py`, `agent.py`, `tools.py`, `ai.py` | **Thắng** | Thắng quản lý qua PR `thang/...`; tuân thủ `answer(text) -> {"output": str}`, `call_model()` giữ `@model_call` lấy token từ `usage` API, `tools.py` dùng `@tool`. |
| `eval/benchmark.csv`, `metric_spec.yaml`, `README.md`, `report.md` | **Sơn** | Sơn quản lý qua PR `son/...`; không ai sửa `expected` cho khớp output; xóa 3 dòng mẫu `B01, B02, B03` trước khi nộp. |
| `eval/run-*.csv`, `traces/run-*.jsonl`, `cost/simulate-*.csv` | **Sơn** *(tự động)* | File sinh bởi `run.py`; không sửa nội dung đã chạy (chỉ điền cột `pass`, `ghi_chu` ở `run-*.csv` nếu chấm tay). |
| `cost/personas.yaml`, `cost/cost-estimate.md` | **Sơn** | Mạnh gửi số liệu tần suất thật từ bằng chứng để Sơn điền `personas.yaml`. |
| `slides/outline.md`, `demo-slides.pdf` | **Nam** | `demo-slides.pdf` bắt buộc nằm ở **thư mục gốc repo** trước CP4 (`14:30` T7). |
| `docs/ai-usage.md` | **Thắng** | Nam, Mạnh, Sơn gửi prompt/công cụ AI đã dùng cho Thắng tổng hợp qua PR trước `23:00` T7. |
| `reflection/*.md` | **Mỗi người 1 file riêng** | `nam.md`, `manh.md`, `thang.md`, `son.md` (chép từ `reflection/TEMPLATE.md`, mỗi người tự mở PR riêng). |

### 2.3. Quy tắc cấm (áp dụng cho mọi PR / bản nộp)

- **KHÔNG** sửa 4 file khung BTC: `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py`, `run.py`.
- **KHÔNG** commit `.env`, API key, bệnh án, đơn thuốc, ảnh hộp thuốc thật hay PII lên GitHub (**TRỪ 10 ĐIỂM**).
- **KHÔNG** sửa `spec.md §7`, `eval/metric_spec.yaml` sau CP2 (`19:30` T6), không xóa câu trượt, không sửa `expected` (**0 ĐIỂM** khối đánh giá).
- **KHÔNG** viết prompt "giấu" nguyên văn câu thử từ `benchmark.csv` vào code (`AGENTS.md`).
- **KHÔNG** dùng AI tự sinh dữ liệu thuốc/tương tác rồi dùng luôn mà không đối chiếu tờ HDSD thuốc, Dược thư Quốc gia VN hoặc hướng dẫn Bộ Y tế trong `data/DATA_CARD.md`.
- **KHÔNG** để AI chẩn đoán bệnh, kê đơn, tư vấn liều, khuyên đổi/bỏ thuốc; **100% ca dấu hiệu nguy hiểm** phải báo đi khám/gọi 115 ngay.

---

## 3. Tổng quan tiến độ & lịch trình

| Giai đoạn / CP | Khung giờ / Mốc | Nhánh / PR / Đầu ra | Điều kiện qua cổng ("Xong khi") |
| --- | --- | --- | --- |
| **CP0 · Khởi động & Form 1** | `09:00` – trước `16:30` T6 | PR `nam/cp0-task` (`TASK.md`), Repo Public, Form 1 | Cả 4 người clone repo, cài `requirements.txt`; PR `TASK.md` được merge; Nam nộp Form 1 trước `16:30` T6. |
| **CP1 · Chốt đội & Canvas (3đ)** | `16:00 – 17:00` T6 | PR `nam/cp1-teams-canvas`, PR `manh/cp1-hypothesis` | `TEAMS.md` không còn warning ở `python run.py check`; `canvas.md` 7 dòng (B2, không chữ AI); `hypothesis.md` có trước bằng chứng; Form 2 (CP1) trước `17:00`. |
| **CP2 · Spec, Data & Mock (4đ)** | `17:00 – 19:30` T6 | PR `nam/cp2-spec`, `manh/cp2-datacard`, `thang/cp2-mock-flow`, `son/cp2-eval-init` | `spec.md §4` & `§7` (khóa cứng chuẩn đạt); `DATA_CARD.md` có nguồn từng mục; `benchmark.csv` ≥10 câu + `metric_spec.yaml` ≥3 metric đủ 4 trường; `python run.py` thông luồng; Form 2 (CP2) trước `19:30`. |
| **CP3 · Pain, AI thật & Eval L1 (4đ)** | `19:30` T6 – `10:00` T7 | PR `manh/cp3-evidence`, `thang/cp3-real-ai`, `son/cp3-eval-run1`, Video 30s | `evidence/summary.md` ≥1 nguồn + ≥5 trích dẫn ẩn tên; `benchmark.csv` 20–30 câu (≥5 `kho`, ≥2 `tu_choi`, xóa `B01–B03`); `ai.py` gọi AI thật + Video 30s mở ẩn danh; `eval/run-1.csv`; Form 2 (CP3) trước `10:00`. |
| **CP4 · L2, Cost & Slide (4đ)** | `10:00 – 14:30` T7 | PR `thang/cp4-improve`, `son/cp4-eval2-cost`, `manh/cp4-validation`, `nam/cp4-slides` | Có mặt phòng L3B lúc `14:00`; `report.md` (L1→L2); `simulate` ≥50 phiên + `cost-estimate.md`; `demo-slides.pdf` ở gốc repo + Video dự phòng; Form 2 (CP4) trước `14:30`. |
| **Vòng 1 & Vòng 2 · Thi đấu** | `14:30 – 18:00` T7 | Pitch live, Form 3 (`15:47`), Form 4 (`17:34`) | Bám giờ cứng (V1: 9p/đội, V2: 12p/đội); mạng/API lỗi >30s bật ngay Video dự phòng. |
| **Khóa Repo Cuối** | `18:00 – 23:59` T7 | PR `nam/final-spec10`, `thang/final-ai-usage`, 4 PR `*/final-reflection` | `spec.md §10`, `docs/ai-usage.md`, đủ 4 file `reflection/*.md` merge vào `main` trước `23:59` T7. |

---

## 4. Phân công chi tiết từng Checkpoint / Giai đoạn

### CP0 · Khởi động, Đăng ký đội & PR `TASK.md` (`09:00` – trước `16:30` Thứ Sáu 27/11)

**Tài liệu / Mục đối chiếu:** `tracks/track-b-healthcare.md`, `AGENTS.md`, `02-guide.md`, `03-rubric.md`.

- [ ] **Phạm Hà Nam** (`@phamhanam`): Mở PR `nam/cp0-task` cập nhật `TASK.md`; nộp **Form 1** (Lớp `L3B`, Đội `MNTS`, đủ 4 MSSV) trước `16:30` T6 *(điền sai báo Lab Coach sửa, không tự nộp lại)*; kiểm tra tên đội trên Dropdown Form 2 & Cổng Tra Cứu.
- [ ] **Nguyễn Đức Mạnh** (`@nguyenducmanh-itus`): Clone repo, cài `requirements.txt`, đọc `tracks/track-b-healthcare.md` & `further-reading/mom-test-summary.md`; nhắn hẹn gọi điện người thân hay sắp thuốc hộ (`10–15p` tối T6) và dược sĩ (nếu có) ngay từ sáng T6.
- [ ] **Vũ Trọng Thắng** (`@Thangvipsv4`): Clone repo, cài `requirements.txt`, đọc `AGENTS.md` & `docs/connect-model.md`, tạo `.env` local từ `.env.example`.
- [ ] **Đào Đức Sơn** (`@b1rdal`): Clone repo, review & merge PR `nam/cp0-task`, đọc `03-rubric.md` và chạy thử `python run.py check`.

---

### CP1 · Chốt Đội, Hướng B2, Canvas & Giả thuyết (`16:00 – 17:00` Thứ Sáu 27/11 · 3 điểm)

**Tài liệu / Mục đối chiếu:** `TEAMS.md`, `canvas.md`, `AGENTS.md`, `evidence/hypothesis.md`, Form 2 nhánh CP1.

#### 1. Phạm Hà Nam (`@phamhanam`) — Đội trưởng / Product & Spec
- **Nhánh / File:** `nam/cp1-teams-canvas` | `TEAMS.md`, `canvas.md`, `AGENTS.md`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Điền `TEAMS.md` đúng format (Tên nhóm `MNTS`, Lớp `L3B`, Track `B`, Link repo Public, 4 thành viên với Nam ở dòng 1 `Đội trưởng`).
  - [ ] Điền `canvas.md` đủ 7 dòng cho hướng **B2** (bài toán 1–2 câu **không dùng chữ "AI"** + lát cắt 1 câu).
  - [ ] Cập nhật 3 dòng *"Quy ước của nhóm"* ở `AGENTS.md`.
  - [ ] Chạy `python run.py check` xác nhận phần `Kiểm TEAMS.md` **không còn cảnh báo**, mở PR và merge vào `main`; kiểm link Repo ở **Tab Ẩn Danh** → Nộp **Form 2 → Nhánh CP1** trước `17:00`.

#### 2. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Discovery & Data
- **Nhánh / File:** `manh/cp1-hypothesis` | `evidence/hypothesis.md`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Viết `evidence/hypothesis.md` **TRƯỚC** khi thu thập bằng chứng (giả thuyết pain của người sắp thuốc hộ cho cha mẹ uống nhiều thuốc và khách hỏi thuốc tối muộn).
  - [ ] Mở PR và merge `manh/cp1-hypothesis` vào `main` trước `17:00`.

#### 3. Vũ Trọng Thắng (`@Thangvipsv4`) — AI Core & App Developer
- **Nhánh / File:** `thang/cp1-env-check` | `.env` (local), `codebase/` (thiết kế nháp)
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Chốt danh sách tool B2 theo `track-b-healthcare.md`: `check_red_flags`, `lookup_drug`, `check_interactions`, `build_schedule`, `handoff_to_pharmacist`, `advise_see_doctor`.
  - [ ] Kiểm tra API key & kết nối thử ở máy local (trong `.env`) theo `docs/connect-model.md`.

#### 4. Đào Đức Sơn (`@b1rdal`) — Eval, Cost & QA
- **Nhánh / File:** Review PR `nam/cp1-teams-canvas`
- **Reviewer:** — (đóng vai Reviewer)
- **Đầu việc:**
  - [ ] Review PR `nam/cp1-teams-canvas` (khớp 4 MSSV, không chữ AI ở Pain trong `canvas.md`), approve/merge và chạy `python run.py check` trên `main` trước `17:00`.

---

### CP2 · Kiến trúc, Data Y khoa, Bộ câu thử đầu & Khóa chuẩn "Đạt" (`17:00 – 19:30` Thứ Sáu 27/11 · 4 điểm)

**Tài liệu / Mục đối chiếu:** `spec.md` (`§4`, `§7`), `data/DATA_CARD.md`, `eval/benchmark.csv`, `eval/metric_spec.yaml`, `codebase/*`, Form 2 nhánh CP2.

#### 1. Phạm Hà Nam (`@phamhanam`) — Product & Spec
- **Nhánh / File:** `nam/cp2-spec` | `spec.md`, `canvas.md` (cập nhật mục `Đã đổi gì so với CP1`)
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Viết `spec.md §4` (sơ đồ: Input → `check_red_flags` → `lookup_drug` & `check_interactions` → Cảnh báo mức độ / `handoff_to_pharmacist` / `build_schedule`).
  - [ ] Cùng Sơn chốt **chuẩn "đạt" bằng số ở `spec.md §7`** (100% ca red flags báo đi khám/115 ngay; 100% tương tác mức "nặng" trong data được báo; 100% câu dụ chẩn đoán/hỏi liều/kê đơn bị từ chối; thêm metric kiểm soát chuyển dược sĩ thừa). **Khóa cứng `§7` trước `19:30` T6**.
  - [ ] Mở PR, merge vào `main` và nộp **Form 2 → Nhánh CP2** trước `19:30`.

#### 2. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Data Y khoa chuẩn nguồn
- **Nhánh / File:** `manh/cp2-datacard` | `data/DATA_CARD.md` (+ file dữ liệu seed giả lập trong `data/` nếu cần)
- **Reviewer:** `@Thangvipsv4`
- **Đầu việc:**
  - [ ] Dựng bộ dữ liệu seed B2 (thuốc phổ biến, hoạt chất, cách uống, cặp tương tác nhẹ/vừa/nặng, thuốc uống cách giờ, dấu hiệu nguy hiểm; tên nhà thuốc dựng).
  - [ ] Điền `data/DATA_CARD.md` **ghi rõ nguồn công khai từng mục** (tờ HDSD thuốc, Dược thư Quốc gia VN, hướng dẫn Bộ Y tế) và mở PR merge trước `19:00`.

#### 3. Vũ Trọng Thắng (`@Thangvipsv4`) — Codebase Khung & Mock Flow
- **Nhánh / File:** `thang/cp2-mock-flow` | `codebase/app.py`, `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Cài đặt các `@tool` trong `codebase/tools.py` (đủ docstring 4 ý) và `answer(text) -> {"output": str}` trong `codebase/agent.py` bám `spec.md §4`.
  - [ ] Chạy `python run.py` thông luồng từ đầu đến cuối (dùng mock trong `call_model()` ở CP2), mở PR và merge vào `main`.

#### 4. Đào Đức Sơn (`@b1rdal`) — Benchmark & Metric Spec
- **Nhánh / File:** `son/cp2-eval-init` | `eval/benchmark.csv`, `eval/metric_spec.yaml`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Điền `eval/benchmark.csv` đủ **≥10 câu** đầu (đúng 6 cột `id,input,expected,pass_criterion,type,source`; xóa 3 dòng ví dụ `B01, B02, B03`).
  - [ ] Điền `eval/metric_spec.yaml` đủ **≥3 metric** (đủ 4 trường `name`, `definition`, `grader`, `threshold`) khớp `spec.md §7`.
  - [ ] Chạy `python run.py check` & `python run.py eval --try`, mở PR và merge trước `19:30`.

---

### CP3 · Bằng chứng Pain, Nối AI Thật, Bộ 20–30 câu & Eval Lượt 1 (`19:30` T6 – `10:00` Thứ Bảy 28/11 · 4 điểm · Online)

**Tài liệu / Mục đối chiếu:** `evidence/*`, `codebase/ai.py`, `eval/benchmark.csv`, `eval/README.md`, Video 30s, Form 2 nhánh CP3.

#### 1. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Bằng chứng Pain (Track B tự tìm)
- **Nhánh / File:** `manh/cp3-evidence` | `evidence/data-mining.md`, `evidence/interviews/P*.md`, `evidence/survey/*`, `evidence/summary.md`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Thu thập ≥1 nguồn đạt ngưỡng theo `02-guide.md §1.2`: đào review app nhà thuốc (Google Play/App Store/Google Maps) vào `data-mining.md`, **hoặc** ≥3 phỏng vấn (`interviews/P1.md`...), **hoặc** ≥20 khảo sát (`survey/`). Không hỏi bệnh cụ thể, không xin ảnh đơn thuốc; ghi giới hạn mẫu nếu phỏng vấn bạn cùng lớp.
  - [ ] Tổng hợp `evidence/summary.md` kèm số đếm và **≥5 trích dẫn nguyên văn đã ẩn tên/bệnh**, mở PR và merge trước `09:30` T7.

#### 2. Vũ Trọng Thắng (`@Thangvipsv4`) — Nối Model AI Thật
- **Nhánh / File:** `thang/cp3-real-ai` | `codebase/ai.py`, `codebase/agent.py`, `codebase/tools.py`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Nối model **AI thật** tại `call_model(system, user)` trong `codebase/ai.py` (giữ `@model_call`, trả `{"text", "model", "tokens_in", "tokens_out"}` từ `usage` API; API key để trong `.env`).
  - [ ] Mở PR và merge vào `main` trước `08:30` T7 để Sơn chạy Eval Lượt 1 và Nam quay Video 30s.

#### 3. Đào Đức Sơn (`@b1rdal`) — Bộ 20–30 câu & Eval Lượt 1
- **Nhánh / File:** `son/cp3-eval-run1` | `eval/benchmark.csv`, `eval/README.md`, `eval/run-1.csv`, `traces/run-1.jsonl`
- **Reviewer:** `@Thangvipsv4`
- **Đầu việc:**
  - [ ] Mở rộng `eval/benchmark.csv` lên **20–30 câu** (≥5 câu `kho`: tương tác nặng trong đơn 5–7 thuốc, tương tác nhẹ, uống cách giờ, sai tên/biệt dược, thuốc ngoài data, red flags ẩn; ≥2 câu `tu_choi`: dụ chẩn đoán, hỏi liều "uống gấp đôi được không", đòi kháng sinh không đơn, giả làm bác sĩ).
  - [ ] Chạy `python run.py check`, `python run.py eval` (Lượt 1 trên AI thật) và `python run.py score eval/run-1.csv`; ghi `x/N` + Run ID vào `eval/README.md`; mở PR merge và gửi danh sách câu trượt cho Thắng.

#### 4. Phạm Hà Nam (`@phamhanam`) — Video 30s & Nộp Form 2 (CP3)
- **Nhánh / File:** Video 30s (link ngoài repo)
- **Đầu việc:**
  - [ ] Quay **Video 30 giây** bản chạy thử gọi **AI thật** (YouTube Unlisted / Drive công khai), kiểm tra mở cả Video và Repo ở **Tab Ẩn Danh** → Nộp **Form 2 → Nhánh CP3** trước `10:00` T7.

---

### CP4 · Cải tiến Lượt 2, Mô phỏng Chi phí & Chốt Slide Demo (`10:00 – 14:30` Thứ Bảy 28/11 · 4 điểm)

**Tài liệu / Mục đối chiếu:** `codebase/*`, `eval/report.md`, `cost/*`, `slides/outline.md`, `demo-slides.pdf`, Form 2 nhánh CP4.
> **Mốc di chuyển:** Cả 4 thành viên có mặt tại đúng **Phòng thi L3B** (tra trên Cổng Tra Cứu) lúc **`14:00`**.

#### 1. Vũ Trọng Thắng (`@Thangvipsv4`) — Cải tiến Lượt 2
- **Nhánh / File:** `thang/cp4-improve` | `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Sửa đúng **1 cải tiến rõ ràng** từ các ca trượt ở `eval/run-1.csv` (ví dụ: chuẩn hóa tra biệt dược/sai chính tả, siết chặn red flags, giảm chuyển dược sĩ thừa ở tương tác nhẹ).
  - [ ] Chạy `python run.py eval --try`, mở PR và merge vào `main` trước `12:30` T7.

#### 2. Đào Đức Sơn (`@b1rdal`) — Eval Lượt 2, Report & Mô phỏng Chi phí
- **Nhánh / File:** `son/cp4-eval2-cost` | `eval/README.md`, `eval/report.md`, `eval/run-2.csv`, `cost/personas.yaml`, `cost/cost-estimate.md`, `cost/simulate-*.csv`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Chạy `python run.py eval` lấy **Lượt 2** (`eval/run-2.csv`) + `python run.py score eval/run-2.csv`; viết `eval/report.md` so sánh trung thực **L1 → L2**.
  - [ ] Điền `cost/personas.yaml` (ít: người trẻ khỏe; vừa: phụ huynh có con nhỏ; nhiều: người con sắp thuốc cho cha mẹ bệnh mạn tính; cộng chi phí giờ công dược sĩ ca chuyển) → chạy `python run.py simulate --rate-from eval/run-2.csv` (hoặc `python run.py simulate`, ≥50 phiên thật) → viết `cost/cost-estimate.md`.
  - [ ] Mở PR và merge vào `main` trước `13:30` T7.

#### 3. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Hỗ trợ Slide & Thử nghiệm thực tế (Bonus)
- **Nhánh / File:** `manh/cp4-validation` | `validation/log.md`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Gửi 2–3 trích dẫn pain đắt giá nhất từ `evidence/summary.md` cho Nam đưa lên slide.
  - [ ] *(Bonus nếu kịp trước `13:30`)* Cho 1–2 người ngoài nhóm thử với đơn thuốc giả định (không dùng bệnh án thật), ghi vào `validation/log.md`, mở PR và merge.

#### 4. Phạm Hà Nam (`@phamhanam`) — Slide Demo, Video Dự phòng & Nộp Form 2 (CP4)
- **Nhánh / File:** `nam/cp4-slides` | `slides/outline.md`, `demo-slides.pdf` (tại **thư mục gốc repo**)
- **Reviewer:** `@nguyenducmanh-itus`
- **Đầu việc:**
  - [ ] Hoàn thiện `slides/outline.md` và xuất **`demo-slides.pdf`** đặt ở **thư mục gốc repo** (gồm: Pain có trích dẫn, Lát cắt 1 câu B2, Demo AI thật + cổng an toàn, Bảng Eval L1→L2, Chi phí/task thành công).
  - [ ] Quay **Video Demo dự phòng** (kiểm Tab Ẩn Danh), mở PR merge `nam/cp4-slides` vào `main`.
  - [ ] Kiểm tra đủ **4 điều kiện cứng xét giải** → Nộp **Form 2 → Nhánh CP4** trước `14:30`.

---

### Vòng 1 & Vòng 2 · Thi đấu tại phòng (`14:30 – 18:00` Thứ Bảy 28/11)

- [ ] **Phạm Hà Nam** (`@phamhanam`): Thuyết trình chính (V1: `5p` pitch + demo; V2: `6p`); điền **Form 3** (`15:47–15:55`, đội mình = `0đ`) và **Form 4** (`17:34–17:44` nếu vào V2).
- [ ] **Vũ Trọng Thắng** (`@Thangvipsv4`): Điều khiển máy demo AI thật; lỗi mạng/API >`30 giây` bật ngay **Video Demo dự phòng**.
- [ ] **Đào Đức Sơn** (`@b1rdal`) & **Nguyễn Đức Mạnh** (`@nguyenducmanh-itus`): Trả lời phần **Thử ca khó & Q&A** (`3p` V1 / `5p` V2) dựa trên `eval/report.md`, `cost/cost-estimate.md`, `data/DATA_CARD.md` và `evidence/summary.md`.

---

### Đóng gói & Khóa Repo Cuối (`18:00 – 23:59` Thứ Bảy 28/11)

**Tài liệu / Mục đối chiếu:** `spec.md §10`, `docs/ai-usage.md`, `reflection/TEMPLATE.md`.

- [ ] **Phạm Hà Nam** (`@phamhanam`): Mở PR `nam/final-spec10` cập nhật `spec.md §10` (tổng kết & hướng cải tiến); Reviewer: `@b1rdal`.
- [ ] **Vũ Trọng Thắng** (`@Thangvipsv4`): Mở PR `thang/final-ai-usage` tổng hợp khai báo dùng AI của 4 người vào `docs/ai-usage.md`; Reviewer: `@phamhanam`.
- [ ] **Mỗi thành viên tự mở PR riêng cho file reflection cá nhân** (chép từ `reflection/TEMPLATE.md`):
  - [ ] **Phạm Hà Nam**: `nam/final-reflection` → `reflection/nam.md` (Reviewer: `@b1rdal`)
  - [ ] **Nguyễn Đức Mạnh**: `manh/final-reflection` → `reflection/manh.md` (Reviewer: `@phamhanam`)
  - [ ] **Vũ Trọng Thắng**: `thang/final-reflection` → `reflection/thang.md` (Reviewer: `@b1rdal`)
  - [ ] **Đào Đức Sơn**: `son/final-reflection` → `reflection/son.md` (Reviewer: `@phamhanam`)
- [ ] **Đào Đức Sơn** (`@b1rdal`): Chạy QA cuối lúc `23:30` T7 trên `main` trước khi khóa repo `23:59`.

---

## 5. Checklist QA cuối cùng trước khi nộp bài

```bash
# 1. Kiểm tra TEAMS.md, eval/benchmark.csv và eval/metric_spec.yaml
python run.py check

# 2. Chạy đánh giá Lượt 2 & tính điểm
python run.py eval
python run.py score eval/run-2.csv

# 3. Chạy mô phỏng chi phí (>= 50 phiên thật)
python run.py simulate --rate-from eval/run-2.csv

# 4. Kiểm tra git sạch và không lộ .env / API key
git status
git ls-files | grep -E '\.env$|key|secret'
```

**Checklist bắt buộc:**
- [ ] **AI thật & Hợp đồng code:** `codebase/ai.py` gọi model thật lấy token từ `usage`; `agent.py` trả `{"output": str}`; không sửa `tracing.py`, `run_eval.py`, `simulate.py`, `run.py`.
- [ ] **An toàn B2 & Eval trung thực:** 100% ca dấu hiệu nguy hiểm báo đi khám/115 ngay; 100% tương tác nặng trong data được báo; 100% ca dụ chẩn đoán/hỏi liều/kê đơn bị từ chối; đủ 20–30 câu (≥5 `kho`, ≥2 `tu_choi`, đã xóa `B01–B03`); không sửa `spec.md §7` hay `metric_spec.yaml` sau `19:30` T6.
- [ ] **Bằng chứng & Nguồn Y khoa:** `evidence/hypothesis.md` viết trước bằng chứng; `evidence/summary.md` đủ ≥1 nguồn + ≥5 trích dẫn ẩn tên; `data/DATA_CARD.md` ghi rõ nguồn công khai từng mục.
- [ ] **Slide, Video & Khóa Repo:** `demo-slides.pdf` nằm ở thư mục gốc repo; Video 30s & Video dự phòng mở được ẩn danh; không lộ `.env`/PII trong lịch sử Git; đủ `spec.md §10`, `docs/ai-usage.md` và 4 file `reflection/*.md`.
