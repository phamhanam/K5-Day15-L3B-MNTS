"""Focused safety smoke tests for the B2 triage helper tools."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


CODEBASE = str(Path(__file__).resolve().parents[1] / "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

import tools  # noqa: E402


class RedFlagToolTests(unittest.TestCase):
    def test_explicit_emergency_phrase_escalates(self):
        result = tools.check_red_flags("Tôi đang khó thở")
        self.assertEqual(result["urgency"], "emergency")
        self.assertIn("115", result["message"])
        self.assertIn("khó thở", result["matched_terms"])

    def test_other_symptoms_are_not_declared_safe(self):
        result = tools.check_red_flags("Tôi thấy mệt")
        self.assertEqual(result["urgency"], "unknown")
        self.assertNotEqual(result["status"], "no_red_flags")

    def test_invalid_input(self):
        self.assertEqual(tools.check_red_flags(" ")["status"], "invalid_input")


class DoctorAdviceToolTests(unittest.TestCase):
    def test_recommends_clinician_without_diagnosis(self):
        result = tools.advise_see_doctor("Tôi bị đau đầu vài ngày")
        self.assertEqual(result["recommendation"], "seek_clinician")
        self.assertIn("không thể chẩn đoán", result["message"])

    def test_invalid_input_still_points_to_care(self):
        result = tools.advise_see_doctor("")
        self.assertEqual(result["status"], "invalid_input")
        self.assertEqual(result["recommendation"], "seek_clinician")


class SeedLookupTests(unittest.TestCase):
    def test_lookup_returns_only_seeded_drug_fields_and_sources(self):
        result = tools.lookup_drug("  IBUPROFEN ")
        self.assertEqual(result["status"], "found")
        self.assertEqual(result["active_ingredient"], "ibuprofen")
        self.assertIsNone(result["dose_or_schedule"])
        self.assertTrue(result["sources"])

    def test_unknown_drug_is_not_assumed_safe(self):
        result = tools.lookup_drug("unknown medicine")
        self.assertEqual(result["status"], "no_verified_data")
        self.assertTrue(result["sources"] == [])
        self.assertIn("không xác nhận thuốc an toàn", result["message"])

    def test_unreadable_seed_fails_closed(self):
        with patch.object(tools, "SEED_PATH", Path("missing-b2-seed.json")):
            self.assertEqual(tools.lookup_drug("ibuprofen")["status"], "data_unavailable")

    def test_interaction_check_fails_closed_when_seed_is_unavailable(self):
        with patch.object(tools, "SEED_PATH", Path("missing-b2-seed.json")):
            result = tools.check_interactions(["warfarin", "ibuprofen"])
        self.assertEqual(result["status"], "data_unavailable")

    def test_seeded_interaction_returns_risk_label_and_sources(self):
        result = tools.check_interactions(["Warfarin", "IBUPROFEN"])
        self.assertEqual(result["status"], "interaction_found")
        self.assertEqual(result["results"][0]["risk_tag"], "high_risk_refer_pharmacist")
        self.assertTrue(result["results"][0]["sources"])

    def test_unclassified_seed_interaction_is_retained_not_treated_as_missing_file(self):
        result = tools.check_interactions(["levothyroxine", "calcium carbonate"])
        self.assertEqual(result["status"], "partial_data")
        pair = next(item for item in result["results"] if item["status"] == "interaction_unclassified")
        self.assertIsNone(pair["risk_tag"])
        self.assertTrue(pair["summary"])
        self.assertTrue(pair["sources"])

    def test_unknown_drug_prevents_interaction_safety_conclusion(self):
        result = tools.check_interactions(["warfarin", "ibuprofen", "unknown medicine"])
        self.assertEqual(result["status"], "partial_data")
        self.assertEqual(len(result["results"]), 3)
        known_pair = next(item for item in result["results"] if item.get("risk_tag"))
        self.assertEqual(known_pair["risk_tag"], "high_risk_refer_pharmacist")
        unknown_pairs = [item for item in result["results"] if item["status"] == "no_verified_data"]
        self.assertEqual(len(unknown_pairs), 2)
        self.assertTrue(all("không thể kết luận" in item["message"] for item in unknown_pairs))

    def test_unlisted_pair_is_not_reported_as_safe(self):
        records, error = tools._load_seed()
        self.assertIsNone(error)
        records.append({
            "record_type": "drug_reference",
            "name": "test-only-compound",
            "active_ingredient": "test-only-compound",
            "summary": "Synthetic test fixture, not medical content.",
            "source_urls": ["https://example.test/fixture"],
        })
        with patch.object(tools, "_load_seed", return_value=(records, None)):
            result = tools.check_interactions(["ibuprofen", "test-only-compound"])
        self.assertEqual(result["results"][0]["status"], "no_verified_interaction_in_seed")
        self.assertIn("không phải xác nhận", result["results"][0]["message"])

    def test_handoff_only_returns_unsubmitted_draft(self):
        result = tools.handoff_to_pharmacist("Cần dược sĩ xem xét", user_approved=True)
        self.assertEqual(result["status"], "draft_pending_user_review")
        self.assertIs(result["sent"], False)


if __name__ == "__main__":
    unittest.main()
