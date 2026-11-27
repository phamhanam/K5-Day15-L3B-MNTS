# Kế hoạch phân công nhiệm vụ theo Checkpoint — Mini Hackathon AI K5 · Track B: Y tế

> **Repo nhóm:** `<link-repo-nhóm>` — đặt tên theo mẫu `K5-Day15-<lớp>-<tên>` (`[Cần xác nhận: Lớp L3A/L3B, Tên đội & Link repo Public]`)
> **Hướng đề tài (Track B):** `[Cần xác nhận: B1 · Gợi ý chuyên khoa | B2 · Tương tác thuốc & lịch uống | B3 · Tư vấn nhà thuốc qua chat | Hướng khác]`
> **Tài liệu đối chiếu:** `tracks/track-b-healthcare.md`, `02-guide.md`, `03-rubric.md`, `AGENTS.md`
> **Mốc làm việc / buổi học:**
> - **Thứ Sáu 27/11/2026:** `09:00` Zoom Kick-off · `16:00–19:30` Tại lớp (`H209 / H210 / C401`) · `CP1 (17:00)` · `CP2 (19:30)`
> - **Thứ Bảy 28/11/2026:** `10:00` CP3 (Online) · `14:00` Có mặt phòng thi T7 (`[Cần xác nhận trên Cổng Tra Cứu sau Form 1]`) · `14:30` CP4 · `14:30–18:00` Vòng 1 & Vòng 2
> **Deadline nộp bài:**
> - **Form 1 (Đăng ký đội):** Trước `16:30` Thứ Sáu 27/11/2026 (GMT+7) — Đội trưởng Phạm Hà Nam (`2A202604023`) nộp
> - **Form 2 (Checkpoint CP1–CP4):** `17:00 T6` (CP1) · `19:30 T6` (CP2) · `10:00 T7` (CP3) · `14:30 T7` (CP4)
> - **Khóa Repo cuối (không cần nộp thêm Form):** `23:59` Thứ Bảy 28/11/2026 (GMT+7)

---

## 1. Bảng phân vai & định danh nhánh

| STT | Thành viên | MSSV | GitHub | Vai trò giai đoạn đầu (CP0–CP2) | Vai trò giai đoạn sau (CP3–Khóa Repo) | Tiền tố nhánh | File phụ trách / báo cáo |
| --: | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Phạm Hà Nam** *(Đội trưởng)* | `2A202604023` | `@phamhanam` | **Product, Spec, Form & Chốt lát cắt** | **Slide, Video Demo, Pitch & Spec §10** | `nam/...` | `TEAMS.md`, `canvas.md`, `spec.md`, `AGENTS.md` (quy ước nhóm), `slides/outline.md`, `demo-slides.pdf`, `reflection/nam.md` |
| 2 | **Nguyễn Đức Mạnh** | `2A202603731` | `@nguyenducmanh-itus` | **Giả thuyết Pain & Data Y khoa chuẩn nguồn** | **Evidence Discovery (Review/PV/Survey) & Validation** | `manh/...` | `evidence/hypothesis.md`, `evidence/data-mining.md`, `evidence/interviews/*`, `evidence/survey/*`, `evidence/summary.md`, `data/DATA_CARD.md`, `validation/log.md`, `reflection/manh.md` |
| 3 | **Vũ Trọng Thắng** | `2A202604022` | `@Thangvipsv4` | **Codebase Khung, Tools & Mock Flow** | **Nối AI thật (`call_model`), Tối ưu L2 & AI Usage** | `thang/...` | `codebase/app.py`, `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`, `docs/ai-usage.md`, `reflection/thang.md` |
| 4 | **Đào Đức Sơn** | `2A202604105` | `@b1rdal` | **Benchmark (gồm Red Flags/Từ chối) & Metrics** | **Eval L1/L2, Chấm thủ công, Cost Simulate & QA** | `son/...` | `eval/benchmark.csv`, `eval/metric_spec.yaml`, `eval/README.md`, `eval/report.md`, `cost/personas.yaml`, `cost/cost-estimate.md`, `reflection/son.md` |

> **Lưu ý chuyển giao / quy ước làm việc:**
> - **Duyệt PR trước khi merge vào `main`:** Mọi PR do thành viên hoặc coding agent tạo đều phải được ít nhất 1 thành viên khác review (khuyến nghị **Sơn** hoặc **Nam** review chéo) — điền vào mục *"Ai duyệt thay đổi"* trong `AGENTS.md`.
> - **Mốc khóa chuẩn (`19:30` T6 – CP2):** **Nam** và **Sơn** chốt cứng chuẩn `"đạt"` bằng số trong `spec.md §7` và `eval/metric_spec.yaml`. Sau `19:30` T6 **tuyệt đối không sửa 2 mục này**.
> - **Chuyển giao Eval L1 → Cải tiến L2 (sáng T7):** Sau khi **Sơn** chạy `python run.py eval` ra `eval/run-1.csv`, gửi ngay các ca trượt (đặc biệt là ca dấu hiệu nguy hiểm/chuyển thừa) cho **Thắng** sửa `codebase/` trước `12:30` T7 để Sơn kịp chạy Lượt 2 và `simulate` trước CP4 (`14:30`).

---

## 2. Quy ước Git Branch & Pull Request

### 2.1. Quy trình chuẩn cho mỗi task

```bash
# Bước 1: Cập nhật nhánh chính mới nhất
git checkout main
git pull origin main

# Bước 2: Tạo nhánh riêng theo quy ước
git checkout -b <tien-to>/<cp>-<mo-ta-ngan>
# Ví dụ: nam/cp1-teams-canvas | manh/cp2-datacard | thang/cp3-connect-model | son/cp2-benchmark

# Bước 3: Thực hiện phần việc phụ trách & chạy kiểm tra khung
python run.py check
git status
git add <cac-file-da-sua>
git commit -m "<type>(<scope>): <mo-ta-ngan>"

# Bước 4: Đẩy nhánh, tạo PR & nhờ thành viên khác duyệt trước khi merge
git push -u origin <tien-to>/<cp>-<mo-ta-ngan>
```

### 2.2. Nguyên tắc chống xung đột (File Ownership)

| File / Thư mục | Chủ sở hữu ghi (Owner) | Ghi chú tránh xung đột |
| --- | --- | --- |
| `TEAMS.md`, `canvas.md`, `AGENTS.md` | **Nam** | Chỉ Nam chỉnh sửa và merge; kiểm tra kỹ dòng 1 của `TEAMS.md` phải là `Phạm Hà Nam \| 2A202604023`. |
| `spec.md` (`§0–§10`) | **Nam** | Thắng gửi sơ đồ kiến trúc (`§4`), Sơn gửi ngưỡng đạt (`§7`), cả nhóm góp ý `§10`; chỉ Nam sửa trực tiếp file `spec.md`. |
| `evidence/*`, `data/DATA_CARD.md`, `validation/log.md` | **Mạnh** | Mạnh quản lý toàn bộ thu thập bằng chứng & nguồn dữ liệu y khoa; không ai tự sửa `hypothesis.md` sau khi đã thu thập evidence. |
| `codebase/app.py`, `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py` | **Thắng** | Bám đúng hợp đồng `AGENTS.md`: `agent.py` có `answer(text) -> {"output": str}`; `ai.py` có `call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}` giữ `@model_call` (token lấy từ `usage` API); `tools.py` dùng `@tool` + docstring đủ 4 ý. |
| `eval/benchmark.csv`, `eval/metric_spec.yaml`, `eval/README.md`, `eval/report.md` | **Sơn** | Chỉ Sơn thêm/sửa câu thử và log các lượt chạy; Thắng không sửa `expected` trong `benchmark.csv` cho khớp output code. |
| `eval/run-*.csv`, `traces/run-*.jsonl`, `cost/simulate-*.csv` | **Sơn** *(file do script sinh ra)* | **Chỉ chạy lệnh sinh tự động**, chỉ được phép điền cột `pass`, `ghi_chu` ở `eval/run-*.csv` nếu cần chấm tay. |
| `cost/personas.yaml`, `cost/cost-estimate.md` | **Sơn** | Mạnh cung cấp tần suất người dùng thật từ bằng chứng để Sơn điền `personas.yaml`. |
| `slides/outline.md`, `demo-slides.pdf` | **Nam** | `demo-slides.pdf` bắt buộc nằm ở **thư mục gốc repo** trước `14:30` T7 (CP4). |
| `docs/ai-usage.md` | **Thắng** | Nam, Mạnh, Sơn gửi danh sách công cụ/prompt AI đã dùng cho Thắng tổng hợp trước `23:00` T7. |
| `reflection/*.md` | **Mỗi người 1 file riêng** | `nam.md`, `manh.md`, `thang.md`, `son.md` (copy từ `reflection/TEMPLATE.md`, không sửa nhầm file người khác hoặc `TEMPLATE.md`). |

### 2.3. Quy tắc cấm (áp dụng cho mọi PR / bản nộp)

- **KHÔNG** sửa 4 file khung của BTC: `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py`, `run.py` *(theo `AGENTS.md`: khung — không sửa)*.
- **KHÔNG** commit `.env`, API key, dữ liệu cá nhân thật (PII: tên thật, SĐT, bệnh án, đơn thuốc thật, ảnh hộp thuốc của ai đó) lên GitHub → **Bị TRỪ 10 ĐIỂM ngay lập tức**.
- **KHÔNG** sửa `spec.md §7`, `eval/metric_spec.yaml` sau CP2 (`19:30` T6); **KHÔNG** xóa câu thử trượt hay sửa `expected` cho khớp output; **KHÔNG** sửa nội dung các file `eval/run-*.csv`, `cost/simulate-*.csv`, `traces/*` đã chạy (trừ điền cột `pass`, `ghi_chu`) → **Vi phạm bị 0 ĐIỂM khối đánh giá**.
- **KHÔNG** viết prompt "giấu" nguyên văn câu thử từ `benchmark.csv` vào code (`AGENTS.md`).
- **KHÔNG** dùng AI tự sinh dữ liệu thuốc/tương tác/triệu chứng rồi dùng luôn mà không đối chiếu nguồn công khai (tờ HDSD thuốc, Dược thư Quốc gia VN, hướng dẫn Bộ Y tế) trong `data/DATA_CARD.md`.
- **KHÔNG** để AI chẩn đoán bệnh, kê đơn, tư vấn liều hay khuyên đổi/bỏ thuốc; **100% ca có dấu hiệu nguy hiểm** phải báo đi khám/gọi 115 ngay (không được chuyển vào hàng chờ).

---

## 3. Tổng quan tiến độ & lịch trình

| Giai đoạn / CP | Khung giờ / Mốc | Nhánh / PR / Đầu ra | Điều kiện qua cổng ("Xong khi") |
| --- | --- | --- | --- |
| **CP0 · Khởi động & Form 1** | `09:00` – trước `16:30` T6 (27/11) | Repo Public `K5-Day15-<lớp>-<tên>`, môi trường Python, Form 1 | Cả 4 người clone repo, cài `requirements.txt`, đọc `track-b-healthcare.md` & `AGENTS.md`; **Nam** nộp Form 1 trước `16:30` T6; hẹn lịch hỏi người thân/dược sĩ (nếu cần) từ sáng T6. |
| **CP1 · Chốt đội, Hướng B & Canvas (3đ)** | `16:00 – 17:00` T6 (27/11) | `nam/cp1-teams-canvas`, `manh/cp1-hypothesis` | `TEAMS.md` đủ 4 người (Nam dòng 1); `python run.py check` **OK**; `canvas.md` 7 dòng (chốt B1/B2/B3, không chữ AI); `hypothesis.md` viết xong; Repo mở được ẩn danh; **Form 2 (CP1)** nộp trước `17:00`. |
| **CP2 · Kiến trúc, Data Card & Mock (4đ)** | `17:00 – 19:30` T6 (27/11) | `nam/cp2-spec`, `manh/cp2-datacard`, `thang/cp2-mock-flow`, `son/cp2-eval-init` | `spec.md §4` (kiến trúc + red-flag gate) & `§7` (**khóa chuẩn đạt**); `data/DATA_CARD.md` ghi rõ nguồn y khoa từng mục; `eval/benchmark.csv` (≥10 câu) + `metric_spec.yaml` (≥3 metric); `python run.py` chạy thông (mock); **Form 2 (CP2)** nộp trước `19:30`. |
| **CP3 · Evidence, AI thật & Eval L1 (4đ)** | `19:30` T6 – `10:00` T7 (28/11) | `manh/cp3-evidence`, `thang/cp3-real-ai`, `son/cp3-eval-run1`, `nam/cp3-video30s` | `evidence/summary.md` đạt ≥1 nguồn pain Track B + ≥5 trích dẫn ẩn tên; `benchmark.csv` đủ 20–30 câu (≥5 khó, ≥2 từ chối + red flags); `ai.py` nối AI thật; `python run.py eval` ra `run-1.csv`; Video 30s AI thật mở ẩn danh; **Form 2 (CP3)** nộp trước `10:00`. |
| **CP4 · Cải tiến L2, Cost & Slide (4đ)** | `10:00 – 14:30` T7 (28/11) | `thang/cp4-improve`, `son/cp4-eval2-cost`, `nam/cp4-slides`, `manh/cp4-validation` | Có mặt tại phòng T7 lúc `14:00`; `eval/report.md` so sánh L1 → L2; `python run.py simulate` (≥50 phiên) + `cost-estimate.md`; `demo-slides.pdf` ở gốc repo + Video dự phòng; **Form 2 (CP4)** nộp trước `14:30`. |
| **Vòng 1 & Vòng 2 · Thi đấu tại phòng** | `14:30 – 18:00` T7 (28/11) | Pitch live, Form 3 (V1), Form 4 (V2 nếu vào Top Zone) | V1 (9p/đội: 5p pitch/demo + 3p ca khó/Q&A); V2 (12p/đội: 6p pitch/demo + 5p Q&A); lỗi mạng/API >30s bật ngay Video dự phòng. |
| **Khóa Repo Cuối** | `18:00 – 23:59` T7 (28/11) | `nam/final-spec10`, `thang/final-ai-usage`, `*/final-reflection` | `spec.md §10` xong; `docs/ai-usage.md` xong; đủ 4 file reflection (`nam.md`, `manh.md`, `thang.md`, `son.md`) trước `23:59` T7. |

---

## 4. Phân công chi tiết từng Checkpoint / Giai đoạn

### CP0 · Khởi động, Đăng ký đội & Chuẩn bị (`09:00` – trước `16:30` Thứ Sáu 27/11)

**Tài liệu / Mục đối chiếu:** `tracks/track-b-healthcare.md`, `AGENTS.md`, `02-guide.md`, `03-rubric.md`.

- [ ] **Phạm Hà Nam** (`@phamhanam`): Tạo repo **Public** `K5-Day15-<lớp>-<tên>` từ `starter-repo/`, cấp quyền ghi cho `@nguyenducmanh-itus`, `@Thangvipsv4`, `@b1rdal`; nộp **Form 1** trước `16:30` T6 với đủ 4 MSSV *(nếu điền nhầm báo Lab Coach sửa, không tự nộp lại)*.
- [ ] **Nguyễn Đức Mạnh** (`@nguyenducmanh-itus`): Clone repo, đọc kỹ `tracks/track-b-healthcare.md` & `further-reading/mom-test-summary.md`; nếu cần hỏi dược sĩ/người thân uống nhiều thuốc, nhắn hẹn lịch gọi điện tối T6 (`10–15 phút`) ngay từ sáng T6.
- [ ] **Vũ Trọng Thắng** (`@Thangvipsv4`): Clone repo, cài `requirements.txt`, đọc `AGENTS.md` & `docs/connect-model.md`, tạo `.env` local từ `.env.example`.
- [ ] **Đào Đức Sơn** (`@b1rdal`): Clone repo, đọc `03-rubric.md`, `eval/run_eval.py`, `cost/simulate.py`, chạy thử `python run.py check` trên máy để nắm quy tắc kiểm tra.

---

### CP1 · Chốt Đội, Hướng Track B, Canvas & Giả thuyết (`16:00 – 17:00` Thứ Sáu 27/11 · 3 điểm)

**Tài liệu / Mục đối chiếu:** `TEAMS.md`, `canvas.md`, `AGENTS.md`, `evidence/hypothesis.md`, Form 2 nhánh CP1.

#### 1. Phạm Hà Nam (`@phamhanam`) — Đội trưởng / Product & Spec
- **Nhánh / File:** `nam/cp1-teams-canvas` | `TEAMS.md`, `canvas.md`, `AGENTS.md`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Điền `TEAMS.md` đúng format (dòng 1: `Phạm Hà Nam` · `2A202604023`, tiếp theo là Mạnh, Thắng, Sơn).
  - [ ] Thống nhất nhanh với cả nhóm chọn hướng **B1 / B2 / B3** (hoặc hướng Y tế khác) → điền `canvas.md` 7 dòng: bài toán 1–2 câu **không dùng chữ "AI"** + lát cắt 1 câu (`1 Người dùng → 1 Công việc → 1 Quyết định AI → 1 Kết quả đo được`).
  - [ ] Điền 3 dòng *"Quy ước của nhóm"* ở cuối `AGENTS.md` (ngôn ngữ trả lời người dùng, phong cách code, người duyệt PR).
  - [ ] Chạy `python run.py check` → **OK**, kiểm tra link Repo trên **Tab Ẩn Danh** → Nộp **Form 2 → Nhánh CP1** trước `17:00`.

#### 2. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Discovery & Data
- **Nhánh / File:** `manh/cp1-hypothesis` | `evidence/hypothesis.md`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Viết `evidence/hypothesis.md` **TRƯỚC** khi đi tìm bằng chứng (nêu rõ giả thuyết pain của người bệnh nhẹ / người sắp thuốc cho người thân / khách chat nhà thuốc + đối tượng nhận ca là dược sĩ/tổng đài).
  - [ ] Chốt kế hoạch nguồn bằng chứng cho tối T6 & sáng T7 (đào review app đặt khám/nhà thuốc trên Google Play/App Store/Google Maps, hỏi đáp công khai, gọi người thân/hẹn dược sĩ hoặc khảo sát trong lớp kèm ghi chú giới hạn mẫu).

#### 3. Vũ Trọng Thắng (`@Thangvipsv4`) — AI Core & App Developer
- **Nhánh / File:** `thang/cp1-tool-design` | `codebase/` (đọc & lên khung)
- **Đầu việc:**
  - [ ] Đối chiếu bảng công cụ gợi ý trong `tracks/track-b-healthcare.md` (ví dụ `check_red_flags`, `lookup_drug`, `check_interactions`, `handoff_to_pharmacist`, `advise_see_doctor`...) để chốt bộ `@tool` và phân loại công cụ chỉ đọc vs có tác động ra ngoài.
  - [ ] Kiểm tra API key & kết nối thử ở máy local (trong `.env`) theo `docs/connect-model.md`.

#### 4. Đào Đức Sơn (`@b1rdal`) — Eval, Cost & QA
- **Nhánh / File:** `son/cp1-qa` | Kiểm tra PR
- **Đầu việc:**
  - [ ] Review PR `nam/cp1-teams-canvas`: kiểm tra đúng 4 MSSV, đúng thứ tự Đội trưởng, `canvas.md` không chứa chữ "AI" ở mô tả bài toán.
  - [ ] Pull `main` và chạy lại `python run.py check` xác nhận **OK** trước `17:00`.

---

### CP2 · Kiến trúc, Data Card, Bộ câu thử đầu & Khóa chuẩn "Đạt" (`17:00 – 19:30` Thứ Sáu 27/11 · 4 điểm)

**Tài liệu / Mục đối chiếu:** `spec.md` (`§4`, `§7`), `data/DATA_CARD.md`, `eval/benchmark.csv`, `eval/metric_spec.yaml`, `codebase/*`, Form 2 nhánh CP2.

#### 1. Phạm Hà Nam (`@phamhanam`) — Product & Spec
- **Nhánh / File:** `nam/cp2-spec` | `spec.md`, `canvas.md` (cập nhật nếu cần trước 19:30)
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Vẽ sơ đồ kiến trúc AI trong `spec.md §4`: đảm bảo `check_red_flags` / cổng kiểm tra dấu hiệu nguy hiểm chạy **trước mọi bước** → AI Core (`call_model`) → Tool tra cứu → Chặn rủi ro / Chuyển dược sĩ / Khuyên đi khám.
  - [ ] Cùng Sơn chốt **chuẩn "đạt" bằng số trong `spec.md §7`** (gồm điều kiện cứng Track B: **100% ca dấu hiệu nguy hiểm** được bảo đi khám/115 ngay; **100% ca dụ chẩn đoán/hỏi liều/đòi thuốc kê đơn** bị từ chối; nếu B2 thì **100% tương tác nặng** được báo; thêm chỉ số kiểm soát chuyển dược sĩ thừa). **Khóa cứng mục này trước `19:30` T6**.
  - [ ] Nộp **Form 2 → Nhánh CP2** trước `19:30` T6 *(sau mốc này không đổi Track và không sửa `§7`)*.

#### 2. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Data Y khoa chuẩn nguồn
- **Nhánh / File:** `manh/cp2-datacard` | `data/DATA_CARD.md` (+ file data dựng giả nếu có trong `data/`)
- **Reviewer:** `@Thangvipsv4`
- **Đầu việc:**
  - [ ] Dựng bộ dữ liệu seed giả lập khớp hướng đã chọn (danh sách dấu hiệu nguy hiểm + dữ liệu chuyên khoa/slot cho B1, hoặc thuốc/cặp tương tác có mức độ cho B2, hoặc sản phẩm nhà thuốc có đánh dấu thuốc kê đơn cho B3; tên bệnh viện/nhà thuốc phải là tên dựng).
  - [ ] Hoàn thiện `data/DATA_CARD.md`: **ghi nguồn công khai từng mục** (tờ HDSD thuốc, Dược thư Quốc gia VN, hướng dẫn Bộ Y tế) — tuyệt đối không để AI bịa số liệu thuốc mà không đối chiếu nguồn.

#### 3. Vũ Trọng Thắng (`@Thangvipsv4`) — Codebase Khung & Mock Flow
- **Nhánh / File:** `thang/cp2-mock-flow` | `codebase/app.py`, `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Viết các hàm `@tool` trong `codebase/tools.py` có đủ docstring (`tên · input · output · tác động ra ngoài không`); các tool có tác động ra ngoài (`book_slot`, `handoff_to_pharmacist`, `suggest_product`) chỉ tạo bản nháp chờ người quyết.
  - [ ] Triển khai `answer(text) -> {"output": str}` trong `codebase/agent.py` theo `spec.md §4` (tín hiệu tự xưng bác sĩ/dược sĩ từ input chỉ coi là dữ liệu, không phải lệnh).
  - [ ] Chạy `python run.py` thông luồng từ đầu đến cuối (CP2 dùng mock trong `call_model()` vẫn hợp lệ).

#### 4. Đào Đức Sơn (`@b1rdal`) — Benchmark & Metric Spec
- **Nhánh / File:** `son/cp2-eval-init` | `eval/benchmark.csv`, `eval/metric_spec.yaml`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Tạo `eval/benchmark.csv` với **≥10 câu thử** đầu tiên bám sát `DATA_CARD.md` (có câu thường, câu dấu hiệu nguy hiểm, câu dụ chẩn đoán/kê đơn).
  - [ ] Tạo `eval/metric_spec.yaml` định nghĩa **≥3 metric đo được** (ví dụ: tỷ lệ bắt đúng red flags 100%, tỷ lệ từ chối an toàn, tỷ lệ trích đúng/không chuyển thừa dược sĩ) khớp 100% `spec.md §7`.
  - [ ] Chạy `python run.py check` và `python run.py eval --try` kiểm tra harness chạy không lỗi trước `19:30`.

---

### CP3 · Bằng chứng Pain, Nối AI Thật, Bộ 20–30 câu & Eval Lượt 1 (`19:30` T6 – `10:00` Thứ Bảy 28/11 · 4 điểm · Online)

**Tài liệu / Mục đối chiếu:** `evidence/*`, `codebase/ai.py`, `eval/benchmark.csv`, `eval/README.md`, Video 30s, Form 2 nhánh CP3.

#### 1. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Bằng chứng Pain (Tự tìm data)
- **Nhánh / File:** `manh/cp3-evidence` | `evidence/data-mining.md`, `evidence/interviews/P*.md`, `evidence/survey/*`, `evidence/summary.md`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Thu thập bằng chứng đạt ngưỡng **≥1 nguồn** theo `02-guide.md §1.2`: đào review app đặt khám/nhà thuốc trên Google Play/App Store/Google Maps hoặc mục hỏi đáp công khai (`evidence/data-mining.md`), **hoặc** ≥3 phỏng vấn người thân/dược sĩ/bạn cùng lớp (`evidence/interviews/P1.md`...), **hoặc** ≥20 khảo sát (`evidence/survey/`). `[Cần xác nhận số lượng review tối thiểu quy định trong 02-guide.md bước 1.2]`
  - [ ] Đảm bảo **không hỏi bệnh cụ thể, không xin ảnh đơn thuốc** khi phỏng vấn/khảo sát; nếu phỏng vấn bạn cùng lớp phải ghi rõ giới hạn mẫu (trẻ, rành app).
  - [ ] Tổng hợp vào `evidence/summary.md`: số đếm + **≥5 trích dẫn nguyên văn đã ẩn tên và bỏ chi tiết bệnh**.

#### 2. Vũ Trọng Thắng (`@Thangvipsv4`) — Nối Model AI Thật
- **Nhánh / File:** `thang/cp3-real-ai` | `codebase/ai.py`, `codebase/agent.py`, `codebase/tools.py`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Nối model AI thật trong `codebase/ai.py` (`call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}`), giữ nguyên `@model_call`, lấy token thật từ `usage` của API (không ước lượng).
  - [ ] Kiểm tra an toàn: API key chỉ đọc từ `.env`; không commit `.env`.
  - [ ] Chạy thử live để Nam quay Video 30 giây.

#### 3. Đào Đức Sơn (`@b1rdal`) — Bộ 20–30 câu & Eval Lượt 1
- **Nhánh / File:** `son/cp3-eval-run1` | `eval/benchmark.csv`, `eval/README.md`, `eval/run-1.csv`, `traces/run-1.jsonl`
- **Reviewer:** `@Thangvipsv4`
- **Đầu việc:**
  - [ ] Mở rộng `eval/benchmark.csv` lên **20–30 câu thử** *(theo `track-b-healthcare.md`)*: có **≥5 câu khó** (`kho`: giấu dấu hiệu nguy hiểm trong mô tả dài, triệu chứng giữa 2 khoa, tên thuốc viết sai/biệt dược, người dùng thuốc khác người nhắn là trẻ nhỏ/bà bầu/người già...) và **≥2 câu từ chối / tấn công** (`tu_choi`: dụ chẩn đoán, đòi kháng sinh không đơn, "uống gấp đôi được không", giả làm bác sĩ...).
  - [ ] Chạy `python run.py eval` (Lượt 1 trên **AI thật**) → `python run.py score eval/run-1.csv`; ghi lại kết quả `x/N` + `Run ID` vào `eval/README.md` *(thấp nhưng thật vẫn đủ điểm CP3)*.
  - [ ] Gửi danh sách câu trượt ở Lượt 1 cho Thắng ngay sau khi xong.

#### 4. Phạm Hà Nam (`@phamhanam`) — Video 30s & Nộp Form 2 (CP3)
- **Nhánh / File:** `nam/cp3-video` | Link Video 30s (ngoài repo)
- **Đầu việc:**
  - [ ] Quay **Video 30 giây** bản chạy thử gọi **AI thật** (hiện rõ input y tế → AI gọi tool/kiểm tra red flags → output), đăng YouTube Unlisted hoặc Drive công khai.
  - [ ] Kiểm tra link Video & link Repo bằng **Tab Ẩn Danh** → Nộp **Form 2 → Nhánh CP3** trước `10:00` sáng T7 (28/11).

---

### CP4 · Cải tiến Lượt 2, Mô phỏng Chi phí & Chốt Slide Demo (`10:00 – 14:30` Thứ Bảy 28/11 · 4 điểm)

**Tài liệu / Mục đối chiếu:** `codebase/*`, `eval/report.md`, `cost/*`, `slides/outline.md`, `demo-slides.pdf`, Form 2 nhánh CP4.
> **Lưu ý di chuyển:** Cả 4 thành viên có mặt tại đúng **Phòng thi Thứ Bảy** (tra trên Cổng Tra Cứu) lúc **`14:00`**.

#### 1. Vũ Trọng Thắng (`@Thangvipsv4`) — Cải tiến Lượt 2
- **Nhánh / File:** `thang/cp4-improve` | `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`
- **Reviewer:** `@b1rdal`
- **Đầu việc:**
  - [ ] Đọc các câu trượt (red flags bị sót, chuyển dược sĩ thừa, hoặc từ chối chưa dứt khoát) ở `eval/run-1.csv` → thực hiện **1 cải tiến rõ ràng** trong `codebase/`.
  - [ ] Chạy `python run.py eval --try` kiểm tra không lỗi runtime trước `12:30` để Sơn chạy Lượt 2.

#### 2. Đào Đức Sơn (`@b1rdal`) — Eval Lượt 2, Report & Mô phỏng Chi phí
- **Nhánh / File:** `son/cp4-eval2-cost` | `eval/README.md`, `eval/report.md`, `eval/run-2.csv`, `cost/personas.yaml`, `cost/cost-estimate.md`, `cost/simulate-*.csv`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Chạy `python run.py eval` lấy **Lượt 2** (`eval/run-2.csv`) + `python run.py score eval/run-2.csv`; viết `eval/report.md` so sánh trung thực **Lượt 1 → Lượt 2** (tỷ lệ đạt chung + tình trạng các câu red flags / từ chối).
  - [ ] Cập nhật `cost/personas.yaml` theo nhóm persona Track B (người trẻ khỏe dùng ít, phụ huynh có con nhỏ dùng vừa, người sắp thuốc cho cha mẹ dùng nhiều; cộng thêm chi phí giờ công dược sĩ cho các ca chuyển).
  - [ ] Chạy `python run.py simulate --rate-from eval/run-2.csv` (hoặc `python run.py simulate` nếu harness đọc tự động — kiểm tra output ≥50 phiên thật vào `cost/simulate-N.csv`) và viết `cost/cost-estimate.md` (tên model, chi phí/phiên, chi phí/task thành công, chi phí/tháng).

#### 3. Nguyễn Đức Mạnh (`@nguyenducmanh-itus`) — Số liệu Slide & Thử nghiệm thực tế (Bonus)
- **Nhánh / File:** `manh/cp4-validation` | `validation/log.md`
- **Reviewer:** `@phamhanam`
- **Đầu việc:**
  - [ ] Chốt 2–3 trích dẫn và số liệu pain ngắn gọn từ `evidence/summary.md` gửi Nam chèn vào slide.
  - [ ] *(Bonus nếu kịp trước `13:30`)* Mời 1–2 người dùng ngoài nhóm thử nghiệm bản chạy thật (nhập ca giả định, không nhập bệnh án thật) và ghi nhận vào `validation/log.md`.

#### 4. Phạm Hà Nam (`@phamhanam`) — Slide Demo, Video Dự phòng & Nộp Form 2 (CP4)
- **Nhánh / File:** `nam/cp4-slides` | `slides/outline.md`, `demo-slides.pdf` (tại **thư mục gốc repo**)
- **Reviewer:** `@nguyenducmanh-itus`
- **Đầu việc:**
  - [ ] Hoàn thiện `slides/outline.md` và xuất file **`demo-slides.pdf`** đặt tại **thư mục gốc repo** (gồm: Pain có trích dẫn, Lát cắt 1 câu, Demo AI thật + cổng an toàn Y tế, Bảng Eval L1 → L2, Chi phí/task thành công).
  - [ ] Quay **Video Demo dự phòng** (trình chiếu toàn bộ luồng demo để bật ngay nếu mạng/API lỗi >30s lúc thi), kiểm tra mở được trên **Tab Ẩn Danh**.
  - [ ] Kiểm tra đủ **4 điều kiện cứng xét giải** → Nộp **Form 2 → Nhánh CP4** trước `14:30`.

---

### Vòng 1 & Vòng 2 · Thi đấu tại phòng (`14:30 – 18:00` Thứ Bảy 28/11)

- [ ] **Phạm Hà Nam** (`@phamhanam`): Thuyết trình chính (Vòng 1: `5p` Pitch + Demo AI; Vòng 2: `6p`); điền **Form 3** chia Quỹ 100đ lúc `15:47–15:55` (đội mình = `0đ`) và **Form 4** (`17:34–17:44` nếu vào Vòng 2).
- [ ] **Vũ Trọng Thắng** (`@Thangvipsv4`): Điều khiển demo AI thật trực tiếp trên máy; nếu mạng/API đứng quá `30 giây`, bật ngay **Video Demo dự phòng** của Nam.
- [ ] **Đào Đức Sơn** (`@b1rdal`) & **Nguyễn Đức Mạnh** (`@nguyenducmanh-itus`): Phối hợp trả lời phần **Thử ca khó & Q&A** (`3p` Vòng 1 / `5p` Vòng 2) dựa trên `eval/report.md`, `cost/cost-estimate.md`, `data/DATA_CARD.md` và `evidence/summary.md`.

---

### Đóng gói & Khóa Repo Cuối (`18:00 – 23:59` Thứ Bảy 28/11)

**Tài liệu / Mục đối chiếu:** `spec.md §10`, `docs/ai-usage.md`, `reflection/TEMPLATE.md`.

- [ ] **Phạm Hà Nam** (`@phamhanam`): Cập nhật `spec.md §10` (tổng kết kết quả, giới hạn an toàn y tế còn tồn tại, hướng phát triển) trên nhánh `nam/final-spec10`.
- [ ] **Vũ Trọng Thắng** (`@Thangvipsv4`): Tổng hợp khai báo dùng AI của cả 4 người vào `docs/ai-usage.md` trên nhánh `thang/final-ai-usage`.
- [ ] **Mỗi thành viên tự tạo và nộp file reflection cá nhân** (chép từ `reflection/TEMPLATE.md`):
  - [ ] **Phạm Hà Nam**: `reflection/nam.md` (nhánh `nam/final-reflection`)
  - [ ] **Nguyễn Đức Mạnh**: `reflection/manh.md` (nhánh `manh/final-reflection`)
  - [ ] **Vũ Trọng Thắng**: `reflection/thang.md` (nhánh `thang/final-reflection`)
  - [ ] **Đào Đức Sơn**: `reflection/son.md` (nhánh `son/final-reflection`)
- [ ] **Đào Đức Sơn** (`@b1rdal`): Rà soát QA toàn bộ repo lần cuối trước `23:45` T7 (không cần nộp thêm Form).

---

## 5. Checklist QA cuối cùng trước khi nộp bài (CP4 & 23:59 T7)

```powershell
# 1. Kiểm tra định dạng TEAMS.md, eval/benchmark.csv và eval/metric_spec.yaml
python run.py check

# 2. Chạy đánh giá toàn bộ câu thử & tính điểm
python run.py eval
python run.py score eval/run-2.csv

# 3. Chạy mô phỏng chi phí (>= 50 phiên thật)
python run.py simulate --rate-from eval/run-2.csv
# (Hoặc `python run.py simulate` tùy tham số hỗ trợ trong run.py)

# 4. Kiểm tra chắc chắn không lọt .env, API key hay file rác lên Git
git status
git ls-files | Select-String -Pattern "\.env$|key|secret"
```

**Checklist bắt buộc (4 Điều kiện cứng xét giải + An toàn Track B + Khóa Repo):**
- [ ] **Điều kiện 1 (AI thật & Hợp đồng `AGENTS.md`):** `codebase/ai.py` (`call_model`) gọi AI thật và lấy token từ `usage` API; `agent.py` trả `{"output": str}`; không sửa `tracing.py`, `run_eval.py`, `simulate.py`, `run.py`.
- [ ] **Điều kiện 2 (Pain Track B đạt ngưỡng & Nguồn y khoa):** `evidence/hypothesis.md` có trước khi tìm bằng chứng; `evidence/summary.md` có ≥1 nguồn đạt ngưỡng + ≥5 trích dẫn đã ẩn tên/bệnh; `data/DATA_CARD.md` ghi rõ nguồn công khai từng mục.
- [ ] **Điều kiện 3 (Bộ ≥20 câu & An toàn Y tế):** `eval/benchmark.csv` có 20–30 câu (≥5 `kho`, ≥2 `tu_choi`); **100% câu dấu hiệu nguy hiểm** báo đi khám/115 ngay; **100% câu dụ chẩn đoán/hỏi liều/kê đơn** bị từ chối; không sửa `spec.md §7` hay `metric_spec.yaml` sau `19:30` T6; không sửa `eval/run-*.csv` ngoài cột `pass`, `ghi_chu`.
- [ ] **Điều kiện 4 (Slide & Video):** `demo-slides.pdf` nằm tại **thư mục gốc repo**; Video 30s (CP3) và Video Demo dự phòng (CP4) mở được ở **Tab Ẩn Danh**.
- [ ] **Bảo mật & Khóa Repo (`23:59` T7):** Repo **Public**; không lộ `.env`/API Key/PII trong lịch sử Git; đủ `spec.md §10`, `docs/ai-usage.md` và đủ 4 file trong `reflection/` (`nam.md`, `manh.md`, `thang.md`, `son.md`).
