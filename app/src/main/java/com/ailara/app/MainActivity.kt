package com.ailara.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = lightColorScheme()) {
                Surface(modifier = Modifier.fillMaxSize()) { LaraHome() }
            }
        }
    }
}

@Composable
private fun LaraHome() {
    var request by rememberSaveable { mutableStateOf("") }
    var status by rememberSaveable {
        mutableStateOf("Tulis ide aplikasi. Generator AI akan ditambahkan pada tahap berikutnya.")
    }

    Column(
        modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("AI LARA", fontSize = 30.sp, fontWeight = FontWeight.Bold)
        Text("Dari ide menjadi aplikasi Android", fontSize = 18.sp)
        Text("Ceritakan aplikasi yang ingin kamu buat. Tujuan proyek ini adalah mengubah instruksi menjadi proyek Android dan membangun APK.")

        OutlinedTextField(
            value = request,
            onValueChange = { request = it },
            modifier = Modifier.fillMaxWidth(),
            label = { Text("Ide aplikasi") },
            placeholder = { Text("Contoh: aplikasi catatan dengan judul dan pencarian") },
            minLines = 4
        )

        Button(
            onClick = {
                status = if (request.isBlank()) {
                    "Masukkan deskripsi aplikasi terlebih dahulu."
                } else {
                    "Ide diterima di layar ini. Mesin AI dan pembuat APK otomatis belum terhubung; fitur itu akan dibangun berikutnya."
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) { Text("Siapkan ide aplikasi") }

        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Status proyek", fontWeight = FontWeight.SemiBold)
                Spacer(modifier = Modifier.height(8.dp))
                Text(status)
            }
        }

        Text("Tahap 1 dari 4 • Fondasi aplikasi", style = MaterialTheme.typography.labelMedium)
    }
}
