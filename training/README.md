# Rencana pelatihan AI-Lara

Dokumen ini membedakan generator aturan yang sudah ada dari model yang benar-benar dilatih.

## Target pertama: model pembuat spesifikasi aplikasi

Jangan mulai dengan melatih model besar dari nol atau langsung menghasilkan seluruh kode Kotlin. Target versi pertama adalah model yang mengubah instruksi bahasa Indonesia menjadi JSON spesifikasi aplikasi yang konsisten. Generator Android kemudian memakai spesifikasi itu untuk menyusun proyek.

Contoh masukan:
```text
Buat aplikasi catatan dengan pencarian dan mode gelap
```

Contoh keluaran yang diharapkan:
```json
{
  "project_name": "Catatan",
  "platform": "android",
  "features": ["notes", "search", "dark_mode"],
  "screens": ["home", "notes", "search", "settings"]
}
```

Struktur JSON di atas adalah ilustrasi format target. Format akhir harus disamakan dengan kontrak yang dipakai `generator/spec_builder.py` sebelum pelatihan dimulai.

## Tahapan

1. **Rapikan dataset.** Setiap baris `dataset/examples.jsonl` harus berisi satu contoh valid. Tambahkan variasi bahasa Indonesia, ejaan sehari-hari, kombinasi fitur, permintaan yang kurang jelas, serta contoh yang menguji batas kemampuan.
2. **Tingkatkan kualitas contoh.** Lima contoh awal hanyalah benih dataset, belum cukup untuk fine-tuning yang dapat diandalkan. Mulai kumpulkan ratusan contoh yang ditinjau manusia; target ribuan contoh berkualitas untuk cakupan yang lebih luas. Jangan menyalin kode berlisensi tanpa izin.
3. **Pisahkan data.** Buat set pelatihan, validasi, dan pengujian. Contoh yang hampir sama jangan tersebar di semua set, agar evaluasi tidak menipu.
4. **Pilih model dasar.** Gunakan model bahasa terbuka yang lisensinya sesuai, mendukung bahasa Indonesia, dan cukup kecil untuk sumber daya yang tersedia. Catat nama model, versi, dan lisensinya.
5. **Fine-tuning LoRA/QLoRA.** Jalankan eksperimen awal di lingkungan GPU seperti Google Colab atau layanan GPU yang tepercaya. Ponsel Android dapat dipakai untuk mengelola repo dan memantau proses, tetapi umumnya bukan perangkat yang sesuai untuk melatih model bahasa.
6. **Evaluasi sebelum dipakai.** Ukur JSON valid, kecocokan fitur/layar, konsistensi nama proyek, dan hasil build proyek yang dibuat dari prediksi model. Simpan model terbaik dan hasil evaluasi.
7. **Integrasikan dengan API.** Jalankan model di layanan yang punya RAM/VRAM memadai. API harus memvalidasi keluaran model dan memakai generator proyek; jangan menganggap keluaran model sebagai kode yang pasti aman atau bisa dikompilasi.
8. **Tingkatkan bertahap.** Setelah pembuat spesifikasi stabil, pertimbangkan dataset dan evaluasi terpisah untuk pembuatan kode, perbaikan build, serta pembuatan APK.

## Apa arti “dilatih dari nol”?

Melatih model bahasa dari bobot acak membutuhkan dataset teks sangat besar, banyak GPU, waktu, dan biaya. Untuk proyek awal ini, pilihan yang lebih masuk akal adalah **fine-tuning model dasar yang sudah ada**. Itu tetap proses pelatihan, tetapi bukan melatih seluruh model dari nol.

## Gerbang sebelum pelatihan

- [ ] Kontrak JSON keluaran disepakati dan konsisten dengan generator.
- [ ] Dataset lolos validasi format otomatis.
- [ ] Contoh duplikat dan data yang tidak berizin disingkirkan.
- [ ] Set validasi dan pengujian disiapkan.
- [ ] Model dasar dan lisensinya diperiksa.
- [ ] Ada baseline dari generator aturan saat ini untuk dibandingkan.
- [ ] Tidak ada token, kata sandi, atau rahasia dalam dataset dan log.

**Status saat ini:** AI-Lara belum memiliki model yang sudah di-fine-tune. Dataset awal berisi lima contoh, dan generator saat ini berbasis aturan. Dokumen ini adalah rencana kerja, bukan klaim bahwa pelatihan sudah dilakukan.
