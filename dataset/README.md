# Dataset AI Lara

Dataset contoh disimpan sebagai JSONL: satu objek JSON per baris dengan field `instruction` dan `response`.

Contoh:
```json
{"instruction":"Buat aplikasi catatan Android","response":"Rancang aplikasi Kotlin dengan daftar catatan dan penyimpanan lokal."}
```

Data contoh yang saat ini ada di notebook hanya lima baris dan dipakai untuk menguji pipeline. Itu tidak cukup untuk menghasilkan model pembuat APK yang andal.

Sebelum pelatihan yang serius:
- Tambahkan ratusan hingga ribuan contoh yang bervariasi dan diperiksa.
- Sertakan spesifikasi fitur, struktur proyek, kasus validasi, dan contoh kegagalan yang benar.
- Pastikan tidak ada rahasia, data pribadi, atau kode berhak cipta yang tidak boleh digunakan.
- Pisahkan data evaluasi dari data pelatihan.
- Ukur kualitas output dan uji build Android; jangan hanya menilai jawaban teks.
