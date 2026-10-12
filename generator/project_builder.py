"""Generate a minimal Kotlin/Compose source file from a validated app specification.

This produces starter source files only; it does not compile or execute generated code.
"""
from __future__ import annotations

import re
from typing import Any

FEATURE_LABELS = {
    "search": "Pencarian",
    "login": "Login",
    "notes": "Catatan",
    "todo": "Daftar Tugas",
    "camera": "Kamera",
    "calculator": "Kalkulator",
    "offline": "Mode Offline",
    "notifications": "Notifikasi",
    "profile": "Profil",
    "database": "Penyimpanan Data",
    "home_screen": "Beranda",
}


def _kotlin_string(value: str) -> str:
    """Escape user-derived text for a Kotlin string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").replace("\n", " ").replace("\r", " ")


def build_android_sources(spec: dict[str, Any]) -> dict[str, str]:
    """Return a small Android source tree represented as relative-path -> content."""
    title = _kotlin_string(str(spec.get("project_name") or "Aplikasi Lara")[:80])
    raw_features = spec.get("features", [])
    features = [FEATURE_LABELS[f] for f in raw_features if f in FEATURE_LABELS]
    if not features:
        features = ["Beranda"]
    feature_items = ",\n        ".join(f'"{_kotlin_string(item)}"' for item in features)
    source = f'''package com.ailara.generated

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            MaterialTheme(colorScheme = lightColorScheme()) {{
                Surface(modifier = Modifier.fillMaxSize()) {{
                    GeneratedHome()
                }}
            }}
        }}
    }}
}}

@Composable
private fun GeneratedHome() {{
    val title = "{title}"
    val features = listOf(
        {feature_items}
    )
    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {{
        Text(title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        Text("Dibuat dengan AI Lara", style = MaterialTheme.typography.bodyLarge)
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {{
            items(features) {{ feature ->
                Card(modifier = Modifier.fillMaxWidth()) {{
                    Text(feature, modifier = Modifier.padding(16.dp))
                }}
            }}
        }}
    }}
}}
'''
    manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="false"
        android:label="AI Lara Generated"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.Light.NoActionBar">
        <activity
            android:name="com.ailara.generated.MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
'''
    return {
        "app/src/main/java/com/ailara/generated/MainActivity.kt": source,
        "app/src/main/AndroidManifest.xml": manifest,
    }
