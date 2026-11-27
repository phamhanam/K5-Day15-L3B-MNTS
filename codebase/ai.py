"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả nguyên văn phần tổng hợp workflow đã truyền vào, model "fake", token 0.
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import os
import json
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_openrouter(system: str, user: str) -> dict:
    """Call OpenRouter's OpenAI-compatible endpoint and return measured usage."""
    if not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env; chưa gửi request nào đến OpenRouter.")
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env; chưa gửi request nào đến OpenRouter.")

    messages = ([{"role": "system", "content": system}] if system else [])
    messages.append({"role": "user", "content": user})
    body = json.dumps({"model": MODEL_NAME, "messages": messages}).encode("utf-8")
    request = urllib.request.Request(
        OPENROUTER_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")[:300]
        raise RuntimeError("OpenRouter HTTP %d: %s" % (error.code, detail)) from error

    try:
        usage = data["usage"]
        text = data["choices"][0]["message"]["content"]
        tokens_in = usage["prompt_tokens"]
        tokens_out = usage["completion_tokens"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Phản hồi OpenRouter thiếu text hoặc usage token cần thiết.") from error
    if not isinstance(text, str):
        raise RuntimeError("OpenRouter trả nội dung không phải chuỗi.")
    if not isinstance(tokens_in, int) or isinstance(tokens_in, bool) or tokens_in < 0:
        raise RuntimeError("OpenRouter trả prompt_tokens không hợp lệ.")
    if not isinstance(tokens_out, int) or isinstance(tokens_out, bool) or tokens_out < 0:
        raise RuntimeError("OpenRouter trả completion_tokens không hợp lệ.")
    return {"text": text, "model": data.get("model") or MODEL_NAME,
            "tokens_in": tokens_in, "tokens_out": tokens_out}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        # Deterministic pass-through: only the already-checked workflow result
        # is returned. The mock does not infer, rewrite, or add medical facts.
        return {"text": user, "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER == "openrouter":
        return call_openrouter(system, user)

    raise NotImplementedError(
        "chưa viết phần gọi model thật cho MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md"
        % MODEL_PROVIDER)
