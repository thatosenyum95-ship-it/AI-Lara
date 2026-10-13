# Peta Jalan AI Lara

## Tujuan
Menerima instruksi bahasa Indonesia, menyusun spesifikasi aplikasi, menghasilkan kerangka sumber Android, lalu membangun APK melalui pipeline yang terisolasi.

## Bagian proyek
- `notebooks/AI-Lara-Training.ipynb`: uji Qwen2.5-1.5B-Instruct dan pelatihan percobaan LoRA di Google Colab.
- `dataset/`: contoh data untuk pengembangan. Data awal sangat kecil dan bukan dataset pelatihan berkualitas.
- `backend/`: API FastAPI untuk pemeriksaan kesehatan, spesifikasi, dan sumber proyek.
- `generator/`: pembentukan spesifikasi serta kode Kotlin/Compose awal.
- `app/` dan konfigurasi Gradle: aplikasi Android contoh.
- `.github/workflows/build-apk.yml`: build APK debug otomatis di GitHub Actions.

## Status realistis
- Kerangka Android dan workflow build tersedia di repositori.
- Generator saat ini merupakan prototipe berbasis aturan; workflow manual menerima prompt, membuat kerangka sumber Android, lalu menjalankan Gradle untuk menghasilkan APK debug. Workflow ini belum otomatis menggunakan adapter Qwen yang dilatih.
- Endpoint generator menghasilkan berkas sumber awal, bukan paket proyek lengkap atau APK per permintaan.
- Notebook kini memuat alur pelatihan LoRA percobaan dan ekspor adapter, tetapi pengguna tetap harus menjalankan sel di Colab.
- Contoh dataset saat ini hanya untuk memeriksa alur kerja. Jangan menganggap hasilnya siap produksi.

## Tahapan pengembangan
1. Jalankan tes Python dan workflow build APK.
2. Jalankan notebook Colab dari atas ke bawah menggunakan GPU; simpan adapter ke Google Drive dan jalankan sel uji respons.
3. Ganti dataset contoh dengan banyak contoh berkualitas dan evaluasi pada data terpisah.
4. Buat penghubung backend ke model/adapter yang dievaluasi.
5. Tingkatkan generator menjadi proyek Android dengan fitur nyata, bukan hanya layar awal.
6. Tambahkan validasi kode, pembatasan izin/dependensi, batas waktu, batas ukuran, dan pengujian APK.

## Keamanan
Jangan menaruh token, password, atau kunci API di repositori. Jangan menjalankan kode hasil model tanpa validasi. Build per permintaan harus dijalankan dalam lingkungan terisolasi dengan batas sumber daya.
