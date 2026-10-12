import unittest

from generator.project_builder import build_android_sources
from generator.spec_builder import build_spec


class ProjectBuilderTests(unittest.TestCase):
    def test_generates_compose_activity_and_manifest(self):
        spec = build_spec("Buat aplikasi catatan dengan pencarian")
        files = build_android_sources(spec)
        self.assertIn("app/src/main/java/com/ailara/generated/MainActivity.kt", files)
        source = files["app/src/main/java/com/ailara/generated/MainActivity.kt"]
        self.assertIn("class MainActivity : ComponentActivity()", source)
        self.assertIn("Catatan", source)
        self.assertIn("Pencarian", source)
        self.assertIn("app/src/main/AndroidManifest.xml", files)
        self.assertIn("android.intent.action.MAIN", files["app/src/main/AndroidManifest.xml"])

    def test_escapes_user_title_for_kotlin(self):
        spec = {"project_name": 'Aplikasi "Lara" $demo', "features": []}
        source = build_android_sources(spec)["app/src/main/java/com/ailara/generated/MainActivity.kt"]
        self.assertIn(r'Aplikasi \"Lara\" \$demo', source)

    def test_unknown_features_fall_back_to_home(self):
        files = build_android_sources({"project_name": "Contoh", "features": ["unknown"]})
        self.assertIn('"Beranda"', files["app/src/main/java/com/ailara/generated/MainActivity.kt"])


if __name__ == "__main__":
    unittest.main()
