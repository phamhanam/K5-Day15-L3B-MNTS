"""Offline tests for fake mode and the existing OpenRouter adapter."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


CODEBASE = str(Path(__file__).resolve().parents[1] / "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

import ai  # noqa: E402
import agent  # noqa: E402


class FakeModelTests(unittest.TestCase):
    def test_fake_returns_workflow_summary_unchanged_without_network(self):
        workflow_summary = "Tra cứu seed: warfarin.\nCảnh báo: hỏi dược sĩ.\nNguồn: seed-url"
        with patch.object(ai, "MODEL_PROVIDER", "fake"), \
                patch.object(ai.urllib.request, "urlopen", side_effect=AssertionError("network must not be used")) as urlopen:
            result = ai.call_model("system", workflow_summary)
        self.assertEqual(result, {
            "text": workflow_summary,
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        })
        urlopen.assert_not_called()

    def test_run_py_end_to_end_with_fake_provider(self):
        repo = Path(__file__).resolve().parents[1]
        environment = os.environ.copy()
        environment["MODEL_PROVIDER"] = "fake"
        environment["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, "run.py"],
            cwd=repo,
            input="Thông tin về warfarin\n\n\n",
            text=True,
            encoding="utf-8",
            capture_output=True,
            env=environment,
            timeout=15,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Tra cứu trong dữ liệu demo: warfarin", result.stdout)
        self.assertIn("(model: fake", result.stdout)
        self.assertIn("gọi model 1 lần", result.stdout)

    def test_agent_fake_flow_summarizes_checked_seed_output_offline(self):
        with patch.object(ai, "MODEL_PROVIDER", "fake"), \
                patch.object(ai.urllib.request, "urlopen", side_effect=AssertionError("network must not be used")) as urlopen:
            result = agent.answer("Thông tin về warfarin")
        self.assertIn("Tra cứu trong dữ liệu demo: warfarin", result["output"])
        self.assertIn("Seed chưa có chỉ định liều/lịch đã xác minh", result["output"])
        self.assertIn("medlineplus.gov/druginfo/meds/a682277.html", result["output"])
        urlopen.assert_not_called()

    def test_example_env_selects_fake_without_key_or_model(self):
        example = Path(__file__).resolve().parents[1] / ".env.example"
        values = {}
        for line in example.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.lstrip().startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
        self.assertEqual(values["MODEL_PROVIDER"], "fake")
        self.assertEqual(values["MODEL_NAME"], "")
        self.assertEqual(values["API_KEY"], "")


class OpenRouterCompatibilityTests(unittest.TestCase):
    def test_openrouter_contract_still_uses_response_usage(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps({
                    "model": "provider/model:free",
                    "choices": [{"message": {"content": "mocked response"}}],
                    "usage": {"prompt_tokens": 7, "completion_tokens": 3},
                }).encode("utf-8")

        with patch.object(ai, "MODEL_PROVIDER", "openrouter"), \
                patch.object(ai, "MODEL_NAME", "openrouter/free"), \
                patch.object(ai, "API_KEY", "unit-test-placeholder"), \
                patch.object(ai.urllib.request, "urlopen", return_value=Response()) as urlopen:
            result = ai.call_model("system", "user")
        self.assertEqual(result, {
            "text": "mocked response",
            "model": "provider/model:free",
            "tokens_in": 7,
            "tokens_out": 3,
        })
        urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main()
