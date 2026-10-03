# Sistem Informasi Booking dan Penjadwalan Gym-Pilates Berbasis Python

Aplikasi web manajemen pemesanan sesi latihan, katalog paket, penjadwalan kelas, verifikasi transaksi pembayaran, cetak struk digital (PDF/Print), dan presensi absensi studio.

**Disusun untuk Tugas Rekayasa Perangkat Lunak (RPL)**  
**Program Studi Teknik Informatika, FTIK - Universitas Indraprasta PGRI (UNINDRA)**  
**Kelompok 6:**
- Utari Kusuma Wardana (202343501118)
- Rifan Betra Setiawan (202343501141)
- Sri Wahyu Rifa Nur Hidayat (202343501134)

---

## 📌 Ringkasan Fitur & Modul Sistem

Sistem ini dikembangkan secara penuh berdasarkan spesifikasi kebutuhan (`spec.md`) dan diagram relasi entitas (**ERD**):

1. **Autentikasi & RBAC (Role-Based Access Control):**
   - Hashing password aman menggunakan Werkzeug (`scrypt`/`pbkdf2`).
   - Sesi terisolasi antara **Admin Studio** dan **Member (Pelanggan)**.
   - Tombol pembantu *1-Click Demo Login* untuk mempermudah demonstrasi di hadapan dosen penguji.

2. **Manajemen Paket Gym-Pilates (CRUD):**
   - Admin dapat menambah, memperbarui harga, mengubah kuota sesi, dan menghapus paket.
   - Member dapat menjelajahi katalog paket interaktif.

3. **Manajemen Penjadwalan & Kuota Kelas (Anti Overbooking):**
   - Penjadwalan tanggal sesi, jam mulai, nama instruktur (*coach*), dan kuota maksimal (*kapasitas_maks*).
   - Indikator kapasitas dan sisa slot otomatis terisi secara *real-time*. Sesi yang sudah penuh otomatis dinonaktifkan untuk mencegah *overbooking*.

4. **Alur Pemesanan & Pembayaran:**
   - Member memilih paket dan slot jadwal kelas.
   - Status awal pemesanan berstatus `Pending`.
   - Member dapat mengonfirmasi pembayaran (Transfer Bank / QRIS).
   - Admin memverifikasi pembayaran menjadi status `Lunas` di dasbor.

5. **Cetak Struk Resmi Transaksi (Print & PDF Ready):**
   - Struk faktur pembayaran digital mencantumkan Kode Transaksi `#GP-XXXX`, Rincian Layanan, Nama Instruktur, Total Biaya, dan Stempel Cap `LUNAS`.
   - Siap cetak langsung menggunakan printer kasir/thermal atau disimpan sebagai file PDF (*Print to PDF*).

6. **Modul Presensi / Absensi Studio (Check-in Kehadiran):**
   - Resepsionis/Admin dapat memfilter peserta berdasarkan tanggal sesi.
   - Validasi satu klik tombol *"Tandai Hadir"* yang secara otomatis mencatat `waktu_hadir` dan status kehadiran member.

---

## 🗄️ Pemetaan Basis Data (ERD)

| Nama Tabel | Primary Key | Foreign Key | Deskripsi |
|---|---|---|---|
| `users` | `id_user` | - | Data pengguna (Admin & Member) beserta password hash |
| `packages` | `id_paket` | - | Data paket latihan, harga, kuota sesi, dan fasilitas |
| `schedules` | `id_jadwal` | - | Tanggal sesi, jam mulai, instruktur, kapasitas kuota |
| `bookings` | `id_booking` | `id_user`, `id_paket`, `id_jadwal` | Transaksi pemesanan dengan status bayar (`Pending`, `Lunas`, `Batal`) |
| `attendance` | `id_absensi` | `id_booking` | Catatan kehadiran presensi di studio (`Hadir`, `Tidak Hadir`, `waktu_hadir`) |

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Prasyarat Sistem
- Python 3.10 atau versi lebih baru (Telah teruji pada Python 3.14)
- Web Browser modern (Google Chrome, Microsoft Edge, atau Mozilla Firefox)

### 2. Pemasangan Dependensi
Buka Terminal / PowerShell di folder proyek ini (`d:\PROGRAM\Gym-Pilates`), lalu jalankan:
```bash
py -m pip install -r requirements.txt
```

### 3. Inisialisasi Database & Data Demo (Seeder)
Jalankan script seeder untuk membuat tabel dan mengisi akun demo awal:
```bash
py seed.py
```

### 4. Menjalankan Server Web
Jalankan aplikasi dengan perintah:
```bash
py run.py
```
Akses aplikasi melalui peramban web pada alamat:  
👉 **http://127.0.0.1:5000**

---

## 🔑 Kredensial Akun Bawaan (Demo)

| Peran (Role) | Email | Password | Hak Akses |
|---|---|---|---|
| **Admin Studio** | `admin@gympilates.com` | `admin123` | Akses penuh: Kelola paket, jadwal, verifikasi bayar, absensi studio |
| **Member (Pelanggan)** | `member@gympilates.com` | `member123` | Akses pelanggan: Booking sesi, riwayat transaksi, cetak struk PDF |
| **Member 2** | `utari@gympilates.com` | `utari123` | Akun member kedua (Utari Kusuma W.) |
| **Member 3** | `sri@gympilates.com` | `sri123` | Akun member ketiga (Sri Wahyu Rifa N. H.) |

---

## 🧪 Menjalankan Pengujian Otomatis (Unit Test)

Untuk memastikan seluruh logika transaksi, integritas database, dan pembatasan hak akses berjalan 100% normal:
```bash
py test_app.py
```
Hasil uji: **4 test case lulus (OK)** mencakup homepage, otentikasi login, alur booking member, penerbitan struk, dan validasi absensi studio oleh admin.
