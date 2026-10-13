# AI Lara

AI Lara adalah proyek bertahap untuk membangun sistem yang menerima instruksi bahasa sehari-hari, menyusun spesifikasi aplikasi Android, lalu nantinya menghasilkan proyek dan APK yang dapat diunduh.

## Status

**Notebook pelatihan:** [AI-Lara-Training.ipynb](notebooks/AI-Lara-Training.ipynb) — memuat Qwen, menyiapkan LoRA, menjalankan pelatihan percobaan, dan menyimpan adapter. Jalankan di Google Colab dengan GPU; dataset bawaan hanya contoh kecil.

**Peta jalan:** [docs/ROADMAP.md](docs/ROADMAP.md). Format dan pedoman data: [dataset/README.md](dataset/README.md).

**Tahap 3 — prototipe generator + build dari prompt.** Repo ini sekarang memiliki:
- Aplikasi Android contoh berbasis Kotlin + Jetpack Compose.
- Workflow GitHub Actions untuk membangun APK debug, dengan input deskripsi aplikasi saat dijalankan manual.
- Modul Python yang mengubah prompt menjadi spesifikasi JSON sederhana.
- API FastAPI untuk mengakses generator tersebut.
- Contoh dataset JSONL dan tes otomatis untuk generator.

**Batasan saat ini:** generator masih berbasis aturan kata kunci, bukan model AI yang dilatih dari nol. Endpoint `/generate-project` menghasilkan berkas awal Kotlin/Compose dan manifest berdasarkan fitur yang dikenali, tetapi belum mengemas proyek lengkap atau membangun APK dari prompt. Kode hasil generator harus diuji sebelum dipakai.

## Membuat APK dari deskripsi aplikasi

1. Buka tab [Actions](../../actions).
2. Pilih workflow **Build Android APK**, lalu tekan **Run workflow**.
3. Isi kolom `prompt` dengan deskripsi aplikasi dalam bahasa Indonesia, lalu jalankan workflow.
4. Tunggu hingga semua langkah selesai dengan status sukses.
5. Buka run tersebut, lalu unduh artifact `AI-Lara-debug-apk` di bagian Artifacts.
6. Ekstrak ZIP untuk mendapatkan `app-debug.apk`. Android mungkin meminta izin instalasi dari sumber tersebut.

Workflow ini menjalankan generator berbasis aturan kata kunci, lalu mengompilasi kerangka aplikasi menggunakan Gradle. **Ini belum menggunakan adapter Qwen dari Colab**, dan fitur aplikasi yang dibuat masih berupa kerangka UI, bukan implementasi penuh semua fitur. Jika workflow gagal, buka run dan periksa log langkah yang merah.

## Menjalankan API secara lokal

Memerlukan Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Tes endpoint kesehatan:

```bash
curl http://127.0.0.1:8000/health
```

Contoh membuat spesifikasi:

```bash
curl -X POST http://127.0.0.1:8000/generate-spec \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Buat aplikasi catatan dengan fitur pencarian"}'
```

Untuk membuat kode sumber awal, kirim permintaan ke `/generate-project` dengan body JSON yang sama. Respons berisi pemetaan path berkas ke konten sumber; endpoint ini belum membuat ZIP atau APK.\n\nDokumentasi interaktif FastAPI tersedia di `/docs` saat API dijalankan.

## Tes

```bash
python -m unittest discover -s tests -v
```

## Rencana berikutnya

- [x] Kerangka aplikasi Android.
- [x] Build APK otomatis.
- [x] Generator spesifikasi awal dan tes otomatis.
- [ ] Hubungkan aplikasi Android ke backend yang di-host dengan aman.
- [x] Generator kode sumber Android awal dari spesifikasi.\n- [x] Jalankan build APK berdasarkan prompt manual melalui GitHub Actions.
- [ ] Hubungkan adapter Qwen yang dievaluasi ke backend dengan aman.
- [ ] Tingkatkan generator agar fitur aplikasi benar-benar berfungsi, bukan hanya tampil sebagai daftar UI.
- [ ] Buat dataset lebih besar dan eksperimen model kecil yang benar-benar dilatih.
- [ ] Uji keamanan, dependensi, izin Android, dan APK sebelum dibagikan.

## Keamanan

Jangan masukkan rahasia/API key ke kode atau prompt. Sebelum menerima instruksi pengguna untuk membangun APK, backend harus membatasi ukuran input, waktu proses, penggunaan memori, dependensi, izin aplikasi, serta menjalankan build di lingkungan terisolasi.

APK debug saat ini hanya untuk uji coba, bukan rilis produksi.
