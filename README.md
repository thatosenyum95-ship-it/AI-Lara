# AI Lara

AI Lara adalah proyek awal untuk membangun sistem yang menerima instruksi bahasa sehari-hari, membantu menyusun aplikasi Android, lalu membangun APK yang dapat diunduh.

## Status saat ini

**Tahap 1 — fondasi proyek.** Repo ini berisi aplikasi Android contoh dan workflow GitHub Actions untuk membangun APK debug. Ini belum merupakan model AI yang dilatih dari nol; fondasi build harus terbukti lebih dulu.

## Cara mencoba

1. Buka tab **Actions** di repo ini.
2. Pilih workflow **Build Android APK**.
3. Tekan **Run workflow** (atau tunggu workflow berjalan setelah commit).
4. Buka hasil run yang selesai, lalu unduh artifact **AI-Lara-debug-apk**.
5. Ekstrak ZIP dan instal `app-debug.apk` di perangkat Android. Android mungkin meminta izin instalasi dari sumber tersebut.

## Rencana pengembangan

- [x] Kerangka aplikasi Android sederhana.
- [x] Build APK otomatis melalui GitHub Actions.
- [ ] UI untuk memasukkan instruksi pembuatan aplikasi.
- [ ] Backend generator yang mengubah instruksi menjadi spesifikasi terstruktur.
- [ ] Validasi keamanan dan pengujian proyek hasil generasi.
- [ ] Eksperimen tokenizer/model kecil dan dataset pelatihan.
- [ ] Pipeline build terisolasi untuk APK yang dihasilkan pengguna.

## Catatan penting

APK debug ini hanya contoh awal untuk menguji pipeline. Jangan gunakan untuk menyimpan rahasia/API key. APK yang dihasilkan AI kelak perlu divalidasi, dibatasi izinnya, dan diuji sebelum dibagikan.

## Teknologi

- Kotlin + Android Gradle Plugin
- Jetpack Compose
- GitHub Actions
