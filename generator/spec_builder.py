"""Rule-based prototype: convert an app idea into a structured specification.

This is deliberately not presented as a trained AI model. It is a safe,
deterministic baseline that can later be compared with a model trained on data.
"""
from __future__ import annotations

import re
from typing import Any


FEATURE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("search", ("cari", "pencarian", "search")),
    ("login", ("login", "masuk akun", "autentikasi", "daftar akun")),
    ("notes", ("catatan", "note", "memo")),
    ("todo", ("tugas", "to-do", "todo", "daftar pekerjaan", "pengingat")),
    ("camera", ("kamera", "foto", "ambil gambar")),
    ("calculator", ("kalkulator", "hitung", "perhitungan")),
    ("offline", ("offline", "tanpa internet", "lokal")),
    ("notifications", ("notifikasi", "pemberitahuan", "alarm")),
    ("profile", ("profil", "profile")),
    ("database", ("database", "basis data", "simpan data", "menyimpan data")),
]


def build_spec(prompt: str) -> dict[str, Any]:
    """Build a conservative app specification from Indonesian/English text."""
    cleaned = re.sub(r"\s+", " ", (prompt or "")).strip()
    if not cleaned:
        raise ValueError("Deskripsi aplikasi tidak boleh kosong.")
    if len(cleaned) > 2000:
        raise ValueError("Deskripsi maksimal 2000 karakter.")

    lower = cleaned.lower()
    features = [
        feature for feature, keywords in FEATURE_RULES
        if any(keyword in lower for keyword in keywords)
    ]
    if not features:
        features = ["home_screen"]

    title = _guess_title(cleaned)
    return {
        "project_name": title,
        "package_name": "com.ailara.generated",
        "platform": "android",
        "language": "kotlin",
        "ui_framework": "jetpack_compose",
        "description": cleaned,
        "features": features,
        "screens": _screens_for(features),
        "build_status": "spec_only",
        "notice": (
            "Ini baru spesifikasi awal berbasis aturan. Belum ada kode aplikasi "
            "yang dihasilkan atau APK yang dibangun."
        ),
    }


def _guess_title(prompt: str) -> str:
    text = prompt.strip().rstrip(".!?")
    text = re.sub(
        r"^(tolong\s+)?(buatkan|buat|bikin|build|create)\s+(aplikasi|app)\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = text.split(" dengan ")[0].split(" yang ")[0].strip()
    words = re.findall(r"[A-Za-z0-9]+", text)[:4]
    if not words:
        return "Aplikasi Lara"
    return " ".join(word.capitalize() for word in words)


def _screens_for(features: list[str]) -> list[str]:
    screens = ["home"]
    if "login" in features:
        screens.append("login")
    if "notes" in features:
        screens.append("notes")
    if "todo" in features:
        screens.append("tasks")
    if "profile" in features:
        screens.append("profile")
    if "calculator" in features:
        screens.append("calculator")
    if "camera" in features:
        screens.append("camera")
    return list(dict.fromkeys(screens))
