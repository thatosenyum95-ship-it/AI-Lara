import unittest

from generator.spec_builder import build_spec


class SpecBuilderTests(unittest.TestCase):
    def test_notes_and_search_features(self):
        spec = build_spec("Buat aplikasi catatan dengan fitur pencarian")
        self.assertIn("notes", spec["features"])
        self.assertIn("search", spec["features"])
        self.assertIn("notes", spec["screens"])
        self.assertEqual(spec["platform"], "android")
        self.assertEqual(spec["build_status"], "spec_only")

    def test_empty_prompt_is_rejected(self):
        with self.assertRaises(ValueError):
            build_spec("   ")

    def test_too_long_prompt_is_rejected(self):
        with self.assertRaises(ValueError):
            build_spec("x" * 2001)

    def test_unknown_request_gets_home_screen(self):
        spec = build_spec("Aplikasi untuk sesuatu yang unik")
        self.assertEqual(spec["features"], ["home_screen"])
        self.assertEqual(spec["screens"], ["home"])


if __name__ == "__main__":
    unittest.main()
