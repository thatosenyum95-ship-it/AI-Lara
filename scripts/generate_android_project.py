"""Generate starter Android files from the AI Lara workflow prompt."""
from __future__ import annotations

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.project_builder import build_android_sources
from generator.spec_builder import build_spec


def main() -> None:
    prompt = os.environ.get(
        "AI_LARA_PROMPT",
        "Buat aplikasi catatan dengan daftar catatan dan penyimpanan lokal",
    ).strip()
    if not prompt:
        raise SystemExit("Deskripsi aplikasi kosong. Isi input prompt pada GitHub Actions.")

    spec = build_spec(prompt)
    files = build_android_sources(spec)
    for relative_path, content in files.items():
        target = ROOT / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    print("Nama proyek:", spec["project_name"])
    print("Fitur terdeteksi:", ", ".join(spec["features"]))
    print("File yang dibuat:")
    for relative_path in files:
        print(" -", relative_path)
    print(
        "Catatan: generator saat ini berbasis aturan kata kunci. "
        "APK akan dibangun pada langkah Gradle berikutnya."
    )


if __name__ == "__main__":
    main()
