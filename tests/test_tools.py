"""Focused safety smoke tests for the B2 triage helper tools."""
import sys
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
