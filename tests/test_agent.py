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

    def test_unclassified_seed_interaction_hands_off_with_source(self):
        with patch.object(agent.tools, "check_red_flags", return_value={"urgency": "unknown", "message": ""}):
            result = agent.answer("Levothyroxine và calcium carbonate có tương tác không?")
        self.assertIn("chưa phân loại", result["output"])
        self.assertIn("Cần dược sĩ rà soát", result["output"])
        self.assertIn("dailymed.nlm.nih.gov", result["output"])

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

    def test_verified_warning_before_clarification_and_handoff(self):
        check_interactions = agent.tools.check_interactions
        handoff_to_pharmacist = agent.tools.handoff_to_pharmacist
        drafts = []

        def capture_draft(summary):
            draft = handoff_to_pharmacist(summary)
            drafts.append(draft)
            return draft

        inputs = (
            ("warfarin, ibuprofen và Xarelto có tương tác không?", ("Xarelto",)),
            ("Mẹ uống vitamin C, ibuprofen, warfarin, thuốc dạ dày và thuốc huyết áp "
             "chưa rõ tên. Kiểm tra giúp mình.", ("vitamin C", "thuốc dạ dày", "thuốc huyết áp")),
        )
        for text, unverified in inputs:
            with self.subTest(text=text), \
                    patch.object(agent.tools, "check_interactions", wraps=check_interactions) as check, \
                    patch.object(agent.tools, "handoff_to_pharmacist", side_effect=capture_draft), \
                    patch.object(agent.tools, "build_schedule") as schedule:
                output = agent.answer(text)["output"]
                check.assert_called_once()
                self.assertCountEqual(check.call_args.args[0], ["warfarin", "ibuprofen"])
                schedule.assert_not_called()
                self.assertIn("high_risk_refer_pharmacist", output)
                self.assertIn("chảy máu", output)
                self.assertIn("https://www.medlineplus.gov/druginfo/meds/a682277.html", output)
                self.assertIn("Cần dược sĩ rà soát", output)
                self.assertLess(output.index("Cảnh báo tương tác"), output.index("hoạt chất trên nhãn"))
                unverified_line = next(line for line in output.splitlines() if "Chưa có dữ liệu kiểm chứng" in line)
                for label in unverified:
                    self.assertIn(label, unverified_line)
                self.assertIs(drafts[-1]["sent"], False)
        self.mock_model.assert_not_called()

    def test_named_unverified_drug_is_preserved_in_interaction_requests(self):
        inputs = (
            ("Tôi đang sử dụng warfarin và aspirin. Hai thuốc này có tương tác với nhau không?",
             "warfarin", "aspirin"),
            ("Warfarin và Aspirin có dùng chung được không?", "warfarin", "Aspirin"),
            ("Warfarin có tương tác với Aspirin không?", "warfarin", "Aspirin"),
            ("Thuốc warfarin, Aspirin", "warfarin", "Aspirin"),
            ("Tôi uống warfarin, Aspirin và không nhớ tên thuốc thứ ba.", "warfarin", "Aspirin"),
            ("Kiểm tra tương tác giữa ibuprofen + XYZ-123 giúp tôi.", "ibuprofen", "XYZ-123"),
            ("Danh sách thuốc:warfarin; Foo Bar. Hai thuốc có tương tác không?", "warfarin", "Foo Bar"),
        )
        for text, known, unknown in inputs:
            with self.subTest(text=text), patch.object(agent.tools, "check_interactions") as check:
                output = agent.answer(text)["output"]
                self.assertIn(f"Thuốc đã nhận diện: {known}", output)
                self.assertIn(f"Chưa có dữ liệu kiểm chứng tương ứng cho: “{unknown}”.", output)
                self.assertIn("Chưa đủ căn cứ kết luận tương tác", output)
                self.assertIn("hoạt chất trên nhãn", output)
                self.assertNotIn("[thuốc chưa nhận diện]", output)
                check.assert_not_called()
        self.mock_model.assert_not_called()

    def test_incomplete_list_asks_for_all_names_without_adding_a_fake_drug(self):
        text = "Mẹ đang uống warfarin, ibuprofen và còn một thuốc chưa rõ tên. Nhờ kiểm tra."
        output = agent.answer(text)["output"]
        self.assertIn("Thuốc đã nhận diện", output)
        self.assertIn("chảy máu", output)
        self.assertIn("còn thiếu tên", output)
        self.assertIn("bổ sung danh sách đầy đủ", output)
        self.assertNotIn("[thuốc chưa nhận diện]", output)
        self.mock_model.assert_not_called()

    def test_single_named_drug_with_another_unnamed_drug_asks_for_label(self):
        output = agent.answer("Tôi đang dùng warfarin. Còn một thuốc chưa rõ tên.")["output"]
        self.assertIn("Thuốc đã nhận diện: warfarin", output)
        self.assertIn("còn thiếu tên", output)
        self.assertIn("hoạt chất trên nhãn", output)
        self.assertNotIn("Chưa có dữ liệu kiểm chứng tương ứng cho:", output)
        self.mock_model.assert_not_called()

    def test_request_words_do_not_become_a_third_drug(self):
        output = agent.answer(
            "Tôi đang dùng warfarin và muốn kiểm tra tương tác với ibuprofen."
        )["output"]
        self.assertIn("high_risk_refer_pharmacist", output)
        self.assertNotIn("Chưa có dữ liệu kiểm chứng tương ứng cho:", output)
        self.assertNotIn("bổ sung danh sách đầy đủ", output)

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
