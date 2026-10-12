# AI Lara

AI Lara adalah proyek bertahap untuk membangun sistem yang menerima instruksi bahasa sehari-hari, menyusun spesifikasi aplikasi Android, lalu nantinya menghasilkan proyek dan APK yang dapat diunduh.

## Status

**Tahap 2 — generator spesifikasi awal.** Repo ini sekarang memiliki:
- Aplikasi Android contoh berbasis Kotlin + Jetpack Compose.
- Workflow GitHub Actions untuk membangun APK debug.
- Modul Python yang mengubah prompt menjadi spesifikasi JSON sederhana.
- API FastAPI untuk mengakses generator tersebut.
- Contoh dataset JSONL dan tes otomatis untuk generator.

**Batasan saat ini:** generator masih berbasis aturan kata kunci, bukan model AI yang dilatih dari nol. Endpoint `/generate-spec` hanya menghasilkan spesifikasi, belum kode Android atau APK.

## Cara mengunduh APK contoh

1. Buka tab [Actions](../../actions).
2. Pilih workflow **Build Android APK**.
3. Buka run yang selesai dengan status sukses.
4. Di bagian Artifacts, unduh `AI-Lara-debug-apk`.
5. Ekstrak ZIP lalu instal `app-debug.apk` di perangkat Android. Android mungkin meminta izin instalasi dari sumber tersebut.

Jika workflow gagal, buka run dan lihat log langkah yang merah.

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

Dokumentasi interaktif FastAPI tersedia di `/docs` saat API dijalankan.

## Tes

```bash
python -m unittest discover -s tests -v
```

## Rencana berikutnya

- [x] Kerangka aplikasi Android.
- [x] Build APK otomatis.
- [x] Generator spesifikasi awal dan tes otomatis.
- [ ] Hubungkan aplikasi Android ke backend yang di-host dengan aman.
- [ ] Tambahkan generator proyek Android dari spesifikasi yang tervalidasi.
- [ ] Jalankan build APK per permintaan dalam lingkungan terisolasi.
- [ ] Buat dataset lebih besar dan eksperimen model kecil yang benar-benar dilatih.
- [ ] Uji keamanan, dependensi, izin Android, dan APK sebelum dibagikan.

## Keamanan

Jangan masukkan rahasia/API key ke kode atau prompt. Sebelum menerima instruksi pengguna untuk membangun APK, backend harus membatasi ukuran input, waktu proses, penggunaan memori, dependensi, izin aplikasi, serta menjalankan build di lingkungan terisolasi.

APK debug saat ini hanya untuk uji coba, bukan rilis produksi.
