"""Workflow tests for the deterministic CP2 B2 agent."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


CODEBASE = str(Path(__file__).resolve().parents[1] / "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

import agent  # noqa: E402


def found_drug(name="warfarin", instruction=None):
    return {
        "status": "found",
        "drug_name": name,
        "active_ingredient": name,
        "dose_or_schedule": instruction,
        "summary": "Seed summary",
        "sources": ["https://example.test/source"],
        "message": "Seed-only information",
    }


class AgentWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.model_patch = patch.object(
            agent,
            "call_model",
            side_effect=lambda system, user: {
                "text": user,
                "model": "fake",
                "tokens_in": 0,
                "tokens_out": 0,
            },
        )
        self.mock_model = self.model_patch.start()
        self.addCleanup(self.model_patch.stop)

    def test_emergency_stops_before_lookup(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "emergency", "message": "Gọi 115"}), \
                patch.object(agent.tools, "advise_see_doctor", return_value={"message": "Đi cấp cứu"}) as advise, \
                patch.object(agent.tools, "lookup_drug") as lookup:
            result = agent.answer("Mô tả nguy cấp")
        self.assertEqual(result, {"output": "Gọi 115 Đi cấp cứu"})
        advise.assert_called_once()
        lookup.assert_not_called()
        self.mock_model.assert_not_called()

    def test_unknown_drug_creates_local_handoff(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=[]), \
                patch.object(agent.tools, "lookup_drug", return_value={"status": "no_verified_data", "message": "Chưa có căn cứ"}), \
                patch.object(agent.tools, "handoff_to_pharmacist", return_value={"draft": "DRAFT", "message": "not sent"}) as handoff:
            result = agent.answer("Kiểm tra thuốc không rõ")
        handoff.assert_called_once()
        self.assertIn("DRAFT", result["output"])

    def test_high_risk_interaction_hands_off_without_schedule(self):
        interaction = {"status": "interaction_found", "results": [{
            "risk_tag": "high_risk_refer_pharmacist", "summary": "Cảnh báo seed", "sources": ["source"]
        }]}
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin", "ibuprofen"]), \
                patch.object(agent.tools, "lookup_drug", side_effect=[found_drug(), found_drug("ibuprofen")]), \
                patch.object(agent.tools, "check_interactions", return_value=interaction) as check, \
                patch.object(agent.tools, "handoff_to_pharmacist", return_value={"draft": "DRAFT", "message": "not sent"}) as handoff, \
                patch.object(agent.tools, "build_schedule") as schedule:
            result = agent.answer("Warfarin và ibuprofen")
        check.assert_called_once()
        handoff.assert_called_once()
        schedule.assert_not_called()
        self.assertIn("Cảnh báo seed", result["output"])

    def test_unlisted_interaction_is_not_declared_safe(self):
        interaction = {"status": "no_verified_interaction_in_seed", "results": [], "message": "Chưa có dữ liệu"}
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin", "ibuprofen"]), \
                patch.object(agent.tools, "lookup_drug", side_effect=[found_drug(), found_drug("ibuprofen")]), \
                patch.object(agent.tools, "check_interactions", return_value=interaction), \
                patch.object(agent.tools, "handoff_to_pharmacist", return_value={"draft": "DRAFT", "message": "not sent"}) as handoff:
            result = agent.answer("Warfarin và ibuprofen")
        handoff.assert_called_once()
        self.assertIn("Chưa có dữ liệu", result["output"])

    def test_schedule_missing_verified_instruction_hands_off(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug(instruction=None)), \
                patch.object(agent.tools, "build_schedule") as schedule, \
                patch.object(agent.tools, "handoff_to_pharmacist", return_value={"draft": "DRAFT", "message": "not sent"}) as handoff:
            result = agent.answer("Xếp lịch warfarin")
        schedule.assert_not_called()
        handoff.assert_called_once()
        self.assertIn("chưa có chỉ định dùng đã xác minh", result["output"])

    def test_schedule_uses_only_verified_instruction(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug(instruction="Nguyên văn chỉ dẫn đã xác minh")), \
                patch.object(agent.tools, "build_schedule", return_value={"status": "draft", "schedule": ["draft"], "message": "Lịch nháp"}) as schedule:
            result = agent.answer("Xếp lịch warfarin")
        schedule.assert_called_once_with([{"medication": "warfarin", "instruction": "Nguyên văn chỉ dẫn đã xác minh"}])
        self.assertEqual(result, {"output": "Lịch nháp\n['draft']"})

    def test_single_drug_lookup_returns_seed_grounded_summary(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug()):
            result = agent.answer("Thông tin về warfarin")
        self.assertEqual(set(result), {"output"})
        self.assertIn("Seed summary", result["output"])
        self.mock_model.assert_called_once()


if __name__ == "__main__":
    unittest.main()
