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
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}) as handoff:
            result = agent.answer("Kiểm tra thuốc không rõ")
        handoff.assert_called_once()
        self.assertIn("Chưa có căn cứ", result["output"])

    def test_high_risk_interaction_hands_off_without_schedule(self):
        interaction = {"status": "interaction_found", "results": [{
            "risk_tag": "high_risk_refer_pharmacist", "summary": "Cảnh báo seed", "sources": ["source"]
        }]}
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin", "ibuprofen"]), \
                patch.object(agent.tools, "lookup_drug", side_effect=[found_drug(), found_drug("ibuprofen")]), \
                patch.object(agent.tools, "check_interactions", return_value=interaction) as check, \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}) as handoff, \
                patch.object(agent.tools, "build_schedule") as schedule:
            result = agent.answer("Warfarin và ibuprofen")
        check.assert_called_once()
        handoff.assert_called_once()
        schedule.assert_not_called()
        self.assertIn("Cảnh báo seed", result["output"])

    def test_unlisted_interaction_is_not_declared_safe(self):
        interaction = {"status": "no_verified_interaction_in_seed", "results": [{
            "pair": ["warfarin", "ibuprofen"],
            "status": "no_verified_interaction_in_seed",
            "message": "Chưa có dữ liệu; không thể xác nhận an toàn",
            "sources": [],
        }]}
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin", "ibuprofen"]), \
                patch.object(agent.tools, "lookup_drug", side_effect=[found_drug(), found_drug("ibuprofen")]), \
                patch.object(agent.tools, "check_interactions", return_value=interaction), \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}) as handoff:
            result = agent.answer("Warfarin và ibuprofen")
        handoff.assert_called_once()
        self.assertIn("Chưa có dữ liệu", result["output"])

    def test_all_pairs_are_reported_before_handoff(self):
        results = [
            {"pair": ["warfarin", "ibuprofen"], "status": "interaction_found",
             "risk_tag": "high_risk_refer_pharmacist", "summary": "Cảnh báo nguồn seed",
             "sources": ["https://source.test/warning"]},
            {"pair": ["warfarin", "[thuốc chưa nhận diện]"], "status": "no_verified_data",
             "message": "Chưa đủ căn cứ cho cặp này", "sources": []},
            {"pair": ["ibuprofen", "[thuốc chưa nhận diện]"], "status": "no_verified_data",
             "message": "Chưa đủ căn cứ cho cặp này", "sources": []},
        ]
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin", "ibuprofen"]), \
                patch.object(agent.tools, "lookup_drug", side_effect=[found_drug(), found_drug("ibuprofen")]), \
                patch.object(agent.tools, "check_interactions", return_value={"status": "partial_data", "results": results}) as check, \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}):
            result = agent.answer("warfarin, ibuprofen và Xarelto có tương tác không?")
        self.assertEqual(check.call_args.args[0], ["warfarin", "ibuprofen", "[thuốc chưa nhận diện]"])
        self.assertIn("Cảnh báo nguồn seed", result["output"])
        self.assertIn("Chưa đủ căn cứ cho cặp này", result["output"])
        self.assertIn("https://source.test/warning", result["output"])

    def test_interactions_run_before_handoff_when_drug_lookup_is_incomplete(self):
        interaction = {"status": "interaction_found", "results": [{
            "pair": ["warfarin", "ibuprofen"], "status": "interaction_found",
            "risk_tag": "review", "summary": "Pair result retained", "sources": ["source"],
        }]}
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin", "ibuprofen"]), \
                patch.object(agent.tools, "lookup_drug", side_effect=[found_drug(), {"status": "data_unavailable"}]), \
                patch.object(agent.tools, "check_interactions", return_value=interaction) as check, \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}):
            result = agent.answer("Warfarin và ibuprofen")
        check.assert_called_once()
        self.assertIn("Pair result retained", result["output"])
        self.assertIn("source", result["output"])

    def test_schedule_missing_verified_instruction_hands_off(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug(instruction=None)), \
                patch.object(agent.tools, "build_schedule") as schedule, \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}) as handoff:
            result = agent.answer("Xếp lịch warfarin")
        schedule.assert_not_called()
        handoff.assert_called_once()
        self.assertIn("Cần xác nhận", result["output"])

    def test_schedule_uses_only_verified_instruction(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug(instruction="Nguyên văn chỉ dẫn đã xác minh")), \
                patch.object(agent.tools, "build_schedule", return_value={"status": "draft", "schedule": ["draft"], "message": "Lịch nháp"}) as schedule:
            result = agent.answer("Xếp lịch theo đơn đã xác nhận:\nwarfarin: Nguyên văn chỉ dẫn đã xác minh")
        schedule.assert_called_once_with([{"medication": "warfarin", "instruction": "Nguyên văn chỉ dẫn đã xác minh"}])
        self.assertEqual(result, {"output": "Lịch nháp\n['draft']"})

    def test_schedule_conflict_hands_off_without_building(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug(instruction=None)), \
                patch.object(agent.tools, "build_schedule") as schedule, \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}) as handoff:
            result = agent.answer("Xếp lịch theo đơn đã xác nhận:\nwarfarin: sáng hoặc tối")
        schedule.assert_not_called()
        handoff.assert_called_once()
        self.assertIn("mâu thuẫn", result["output"])

    def test_schedule_unknown_or_unmatched_line_hands_off(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug(instruction=None)), \
                patch.object(agent.tools, "build_schedule") as schedule, \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}) as handoff:
            result = agent.answer("Xếp lịch theo đơn đã xác nhận:\nwarfarin: đúng chỉ dẫn trên nhãn\nthuốc lạ: theo toa")
        schedule.assert_not_called()
        handoff.assert_called_once()
        self.assertIn("thuốc lạ", result["output"])

    def test_single_drug_lookup_returns_seed_grounded_summary(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug()):
            result = agent.answer("Thông tin về warfarin")
        self.assertEqual(set(result), {"output"})
        self.assertIn("Seed summary", result["output"])
        self.mock_model.assert_called_once()

    def test_model_cannot_remove_or_change_warning_or_add_medical_claims(self):
        interaction = {"status": "interaction_found", "results": [{
            "pair": ["warfarin", "ibuprofen"], "status": "interaction_found",
            "risk_tag": "high_risk_refer_pharmacist", "summary": "Seed warning exact text",
            "sources": ["https://source.test/verified"],
            "limits": "Không kết luận an toàn cá nhân.",
        }]}
        self.mock_model.side_effect = None
        self.mock_model.return_value = {
            "text": "This combination is safe; increase dose.",
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin", "ibuprofen"]), \
                patch.object(agent.tools, "lookup_drug", side_effect=[found_drug(), found_drug("ibuprofen")]), \
                patch.object(agent.tools, "check_interactions", return_value=interaction), \
                patch.object(agent.tools, "handoff_to_pharmacist", side_effect=lambda summary: {"draft": summary, "message": "not sent"}):
            result = agent.answer("warfarin ibuprofen")
        self.assertIn("high_risk_refer_pharmacist", result["output"])
        self.assertIn("Seed warning exact text", result["output"])
        self.assertIn("https://source.test/verified", result["output"])
        self.assertIn("Không kết luận an toàn cá nhân", result["output"])
        self.assertNotIn("This combination is safe", result["output"])

    def test_model_cannot_remove_safe_refusal(self):
        self.mock_model.side_effect = None
        self.mock_model.return_value = {
            "text": "Sure, double your dose.",
            "model": "mock",
            "tokens_in": 1,
            "tokens_out": 1,
        }
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}), \
                patch.object(agent, "_extract_seeded_drugs", return_value=["warfarin"]), \
                patch.object(agent.tools, "lookup_drug", return_value=found_drug()):
            result = agent.answer("Tôi đang dùng warfarin, có nên uống gấp đôi liều không?")
        self.assertIn("Không thể chẩn đoán, kê đơn", result["output"])
        self.assertNotIn("Sure, double", result["output"])

    def test_model_error_falls_back_to_workflow_result(self):
        self.mock_model.side_effect = RuntimeError("model unavailable")
        result = agent._respond("Cảnh báo và nguồn đã kiểm tra")
        self.assertEqual(result, {"output": "Cảnh báo và nguồn đã kiểm tra"})


if __name__ == "__main__":
    unittest.main()
