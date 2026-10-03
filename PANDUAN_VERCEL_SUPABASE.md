# PANDUAN DEPLOYMENT: VERCEL, SUPABASE & GITHUB (VERSI 2)

Versi ini berada pada folder: d:\PROGRAM\Gym-Pilates-V2  
Versi 1 (d:\PROGRAM\Gym-Pilates) tetap 100% terkunci dan aman untuk kebutuhan demonstrasi lokal.

---

## 1. Langkah 1: Push ke GitHub

1. Buka [github.com/new](https://github.com/new) dan buat repositori baru (misal: gym-pilates-v2), pilih **Public** atau **Private**, jangan centang README.
2. Di terminal PowerShell, hubungkan dan push repositori V2:
   `powershell
   cd d:\PROGRAM\Gym-Pilates-V2
   git remote add origin https://github.com/USERNAME_KAMU/gym-pilates-v2.git
   git branch -M main
   git push -u origin main
   `

---

## 2. Langkah 2: Setup Database Cloud di Supabase

Karena Vercel bersifat *serverless* (tidak menyimpan file SQLite lokal secara permanen), kita menggunakan basis data PostgreSQL gratis dari Supabase:

1. Buka [supabase.com](https://supabase.com) dan buat akun/login.
2. Klik **New Project**, beri nama: Gym-Pilates, buat kata sandi database (catat kata sandinya), pilih region terdekat (misal: *Singapore*).
3. Setelah project selesai dibuat, buka menu **Project Settings (ikon gerigi)** -> **Database**.
4. Gulir ke bagian **Connection string**, pilih tab **URI** atau **Transaction Pooler (Port 6543)**.
5. Salin URI koneksi tersebut. Formatnya seperti ini:
   `
   postgresql://postgres.[PROJECT-REF]:[PASSWORD_KAMU]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   `
6. **Inisialisasi Tabel & Data Demo ke Supabase:**
   Jalankan perintah ini di PowerShell dari laptop Anda untuk mengisi data awal (admin, member, paket, jadwal) langsung ke cloud Supabase:
   `powershell
   cd d:\PROGRAM\Gym-Pilates-V2
   = postgresql://postgres.[PROJECT-REF]:[PASSWORD_KAMU]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   py seed.py
   `

---

## 3. Langkah 3: Deploy ke Vercel

1. Buka [vercel.com](https://vercel.com) dan login menggunakan akun GitHub Anda.
2. Klik tombol **Add New...** -> **Project**.
3. Pilih repositori **gym-pilates-v2** yang sudah di-push tadi, lalu klik **Import**.
4. Pada bagian **Environment Variables**, tambahkan 2 variabel berikut:
   - SECRET_KEY: zenith-pilates-gym-secret-key-unindra-2026
   - DATABASE_URL: [Tempelkan URI Supabase Anda dari Langkah 2]
5. Klik **Deploy**.
6. Dalam waktu sekitar 30 - 60 detik, website Gym-Pilates Anda sudah aktif secara global di alamat:
   ?? https://gym-pilates-v2.vercel.app

---

## 4. Cara Sinkronisasi Perubahan dari V1 ke V2

Jika di kemudian hari Anda melakukan perbaikan di V1 dan ingin mengirimkannya ke V2:
- Cukup dobel-klik file: sync_v1_to_v2.bat (atau jalankan py sync_v1_to_v2.py).
- File di V2 akan otomatis terbarui tanpa merusak konfigurasi Vercel/Supabase.
- Lakukan git push dari folder V2, dan Vercel akan otomatis me-redeploy versi terbaru!
