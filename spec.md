# Aplikasi Booking dan Penjadwalan Gym-Pilates berbasis Python

**Oleh Kelompok 6:**
* Utari Kusuma Wardana (202343501118)
* Rifan Betra Setiawan (202343501141)
* Sri Wahyu Rifa Nur Hidayat (202343501134)

**PROGRAM STUDI TEKNIK INFORMATIKA**
**FAKULTAS TEKNIK DAN ILMU KOMPUTER**
**UNIVERSITAS INDRAPRASTA PGRI**
**2026**

---

## 1. Pendahuluan (Introduction)

### 1.1 Tujuan (Purpose)
Dokumen ini bertujuan untuk mendefinisikan kebutuhan fungsional dan non-fungsional dari Sistem Informasi Booking dan Penjadwalan Gym-Pilates Berbasis Python. Dokumen ini menjadi acuan bagi tim pengembang (developer), penguji (tester), serta pengajar/dosen penguji untuk memastikan sistem yang dikembangkan sesuai dengan batasan dan spesifikasi yang ditentukan.

### 1.2 Konvensi Dokumen (Document Conventions)
* **Teks Tebal (Bold):** Digunakan untuk penekanan istilah penting, nama aktor, dan modul utama.
* **Kode Identifikasi Kebutuhan:**
  * **FR-xxx** (Functional Requirement): Menandakan kebutuhan fungsional.
  * **NFR-xxx** (Non-Functional Requirement): Menandakan kebutuhan non-fungsional.

### 1.3 Audiens yang Dituju dan Saran Pembacaan (Intended Audience)
Dokumen ini ditujukan untuk:
* **Pengembang Sistem (Developers):** Sebagai panduan koding dan arsitektur aplikasi berbasis Python.
* **Penguji (QA/Tester):** Sebagai acuan pembuatan skenario software testing (unit/integration test).
* **Dosen/Penguji Tugas RPL:** Untuk melakukan evaluasi terhadap kelengkapan spesifikasi kebutuhan perangkat lunak.

### 1.4 Scope Proyek (Project Scope)
Aplikasi Web Gym-Pilates ini menyediakan fasilitas bagi Pelanggan untuk mendaftar, memilih paket keanggotaan/kelas, melakukan booking dan pembayaran, melihat jadwal latihan, serta melakukan absensi presensi saat datang ke lokasi. Bagi Admin, sistem ini mempermudah verifikasi pembayaran, pengelolaan jadwal instruktur/kelas, pencatatan absensi, dan pencetakan struk bukti transaksi.

### 1.5 Referensi (References)
* Wiegers, Karl, & Beatty, Joy. (2013). Software Requirements (3rd Edition). Microsoft Press.
* IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications.

---

## 2. Deskripsi Umum (Overall Description)

### 2.1 Perspektif Produk (Product Perspective)
Sistem ini merupakan aplikasi web standalone berbasis Python (menggunakan framework seperti Django atau Flask) yang terhubung ke basis data relasional (PostgreSQL/MySQL) dan dapat diakses melalui peramban web (web browser) baik di perangkat desktop maupun mobile.

### 2.2 Fitur Produk (Product Features)
* **Autentikasi dan Otorisasi:** Login, Registrasi, dan Manajemen Profil.
* **Manajemen Paket Gym-Pilates:** Katalog paket latihan/keanggotaan.
* **Booking & Pembayaran:** Pemesanan sesi kelas dan konfirmasi transaksi.
* **Manajemen Jadwal:** Penjadwalan kelas Pilates/Gym harian dan mingguan.
* **Absensi / Presensi Kehadiran:** Pencatatan kehadiran pelanggan di studio.
* **Cetak Struk Transaksi:** Output struk bukti pembayaran/booking (PDF/Thermal Printer).

### 2.3 Kelas dan Karakteristik Pengguna (User Classes)
* **Admin Studio:**
  * **Tugas:** Mengelola paket, jadwal kelas, mengkonfirmasi/memvalidasi pembayaran, mencetak struk, serta mencatat/memverifikasi absensi pelanggan.
  * **Akses:** Kontrol penuh (Full Access) pada Dasbor Admin.
* **Pelanggan (Member):**
  * **Tugas:** Memilih paket, melakukan booking sesuai jadwal yang tersedia, melakukan pembayaran, melihat riwayat absensi, serta menerima struk digital/cetak.
  * **Akses:** Terbatas pada profil, pemesanan, dan riwayat mandiri.

### 2.4 Lingkungan Operasi (Operating Environment)
* **Sisi Server:** Python 3.10+, Framework Web (Django / Flask), Database Engine (PostgreSQL / MySQL / SQLite).
* **Sisi Klien:** Web Browser modern (Google Chrome, Mozilla Firefox, Safari, Microsoft Edge).

### 2.5 Batasan Desain dan Implementasi (Constraints)
* Aplikasi dikembangkan menggunakan ekosistem bahasa pemrograman Python.
* Antarmuka berbasis web responsive (HTML5/CSS3/JavaScript atau Bootstrap/Tailwind).
* Koneksi internet yang stabil diperlukan untuk pemrosesan data real-time.

### 2.6 Asumsi dan Dependensi (Assumptions and Dependencies)
* Pengguna memiliki perangkat (smartphone/laptop) dengan browser dan akses internet.
* Pustaka (library) Python untuk pembuatan PDF (seperti ReportLab atau WeasyPrint) berfungsi dengan baik untuk fitur cetak struk.

---

## 3. Kebutuhan Fungsional (System Features / Functional Requirements)

### 3.1 Modul Otentikasi dan Akun
* **FR-LOG-01:** Sistem harus memungkinkan pengguna (Admin & Pelanggan) untuk login menggunakan username/email dan password.
* **FR-LOG-02:** Sistem harus menyediakan form registrasi bagi Pelanggan baru.
* **FR-LOG-03:** Sistem harus menyediakan fitur Logout dan pembatasan hak akses halaman berdasarkan peran (Role-Based Access Control).

### 3.2 Modul Pilihan Paket Gym-Pilates
* **FR-PKT-01:** Admin dapat menambah, mengubah, dan menghapus (CRUD) daftar paket latihan (misal: Paket Harian, Member Bulanan, Kelas Private Pilates).
* **FR-PKT-02:** Pelanggan dapat melihat rincian paket, harga, kuota sesi, dan fasilitas paket.

### 3.3 Modul Jadwal & Booking
* **FR-JDW-01:** Admin dapat mengelola jadwal kelas Gym/Pilates (tanggal, jam, nama instruktur, dan kapasitas kuota).
* **FR-JDW-02:** Pelanggan dapat memilih jadwal kelas dan melakukan booking tempat sesuai paket yang dimiliki.

### 3.4 Modul Pembayaran & Cetak Struk
* **FR-BYR-01:** Sistem harus mencatat transaksi pemesanan/booking paket oleh Pelanggan.
* **FR-BYR-02:** Admin dapat memverifikasi status pembayaran (Cash/Transfer).
* **FR-BYR-03:** Sistem harus dapat membuat dan mengunduh/mencetak Struk Bukti Pembayaran dalam format PDF yang mencantumkan ID Transaksi, Nama Pelanggan, Paket, Jadwal, dan Total Biaya.

### 3.5 Modul Absensi Kehadiran
* **FR-ABS-01:** Admin dapat mencatat kehadiran Pelanggan pada jadwal kelas yang di-booking.
* **FR-ABS-02:** Pelanggan dapat melihat riwayat absensi dan sisa kuota sesi pertemuan mereka.

---

## 4. Kebutuhan Antarmuka Eksternal (External Interface Requirements)

### 4.1 Antarmuka Pengguna (User Interface)
* **Halaman Utama (Landing Page):** Informasi umum studio, pilihan paket, dan tombol login/register.
* **Dashboard Pelanggan:** Tampilan jadwal yang bisa dibooking, status keanggotaan, dan tombol riwayat/cetak struk.
* **Dashboard Admin:** Panel navigasi kelola data paket, jadwal, verifikasi transaksi, dan modul absensi cepat.

### 4.2 Antarmuka Perangkat Lunak (Software Interfaces)
* **Python Engine:** Menjalankan logika bisnis (backend).
* **Database Management System (DBMS):** Menyimpan tabel Users, Packages, Schedules, Bookings, Attendance, dan Transactions.
* **PDF Generation Library:** Menggunakan paket Python (ReportLab/WeasyPrint) untuk merender template HTML/CSS menjadi berkas struk PDF.

### 4.3 Antarmuka Komunikasi (Communication Interfaces)
* Protokol HTTP/HTTPS untuk pertukaran data antara web browser dan aplikasi server Python.

---

## 5. Kebutuhan Non-Fungsional (Non-functional Requirements)

### 5.1 Performa (Performance Requirements)
* **NFR-PER-01:** Waktu respons memuat halaman web tidak boleh melebihi 3 detik dalam kondisi koneksi standar.
* **NFR-PER-02:** Proses pembuatan (generation) berkas PDF struk bukti pembayaran maksimal 2 detik.

### 5.2 Keamanan (Security Requirements)
* **NFR-SEC-01:** Password pengguna harus dienkripsi menggunakan algoritma hashing aman (seperti PBKDF2 atau BCrypt) sebelum disimpan di database.
* **NFR-SEC-02:** Sistem harus mencegah akses tak terotorisasi (Unauthorized Access) ke Dasbor Admin tanpa sesi login yang valid.

### 5.3 Keandalan & Kemudahan Penggunaan (Usability & Reliability)
* **NFR-USE-01:** Antarmuka sistem dirancang ramah pengguna (user-friendly) dan responsif jika dibuka dari ponsel pintar.
* **NFR-REL-01:** Data transaksi dan absensi disimpan secara konsisten (ACID compliance) untuk mencegah duplikasi pemesanan (double booking).

---

## 6. Lampiran (Appendices)

### Lampiran A: Glosarium
* **Booking:** Proses pemesanan tempat atau sesi latihan oleh pelanggan sebelum kelas dimulai.
* **Gym-Pilates:** Jenis olahraga penguatan inti tubuh yang jadwalnya terbatas berdasarkan kuota instruktur.
* **RBAC (Role-Based Access Control):** Pengaturan hak akses berdasarkan peran pengguna (Admin/Pelanggan).
* **Framework (Django / Flask):** Kerangka kerja pengembangan web berbasis Python yang digunakan untuk mempercepat pembuatan aplikasi dengan menyediakan standar struktur folder dan pustaka (library) bawaan.
* **DBMS (Database Management System):** Sistem perangkat lunak yang digunakan untuk mengelola basis data relasional seperti PostgreSQL atau MySQL untuk menyimpan data pengguna, jadwal, dan transaksi.
* **Struk / Invoice Digital:** Bukti pembayaran dan booking sah yang dihasilkan oleh sistem dalam format PDF yang dapat diunduh oleh pelanggan atau dicetak oleh admin.

### Lampiran B: Deskripsi Use Case Diagram
**1. Pelanggan (Member)**
* **Registrasi & Login:** Mendaftarkan akun baru dan masuk ke dalam sistem.
* **Melihat Katalog Paket:** Melihat daftar paket Gym/Pilates yang tersedia beserta harganya.
* **Melakukan Booking:** Memilih jadwal latihan yang tersedia dan memesan slot (kuota).
* **Pembayaran:** Melakukan pembayaran dan mengunggah/mengonfirmasi bukti pembayaran.
* **Melihat Riwayat & Absensi:** Memantau sisa sesi latihan dan riwayat kehadiran.
* **Unduh Struk:** Mengunduh bukti pembayaran (PDF) yang sah.

**2. Admin**
* **Kelola Data Paket:** Menambah, mengedit, atau menghapus paket layanan Gym/Pilates.
* **Kelola Jadwal & Instruktur:** Mengatur tanggal, jam, dan instruktur kelas serta menentukan kapasitas maksimal (kuota).
* **Verifikasi Pembayaran:** Mengecek transaksi pelanggan dan mengubah status dari Pending menjadi Lunas/Success.
* **Catat/Verifikasi Absensi:** Menandai kehadiran pelanggan saat tiba di studio berdasarkan data booking hari tersebut.
* **Cetak Laporan & Struk:** Mencetak struk untuk pelanggan di tempat atau mencetak laporan transaksi bulanan.

### Lampiran C: Rancangan Basis Data

#### 1. Entity Relationship Diagram (ERD)
![Entity Relationship Diagram](User Booking Attendance Flow-2026-10-03-030110.jpg)[cite: 2]

#### 2. Tabel Users
| Field | Tipe Data | Keterangan |
|---|---|---|
| id_user | Integer (PK) | Primary Key, Auto Increment |
| nama_lengkap | Varchar | Nama pengguna |
| email | Varchar | Email pengguna (Unique) |
| password | Varchar | Password (Hashed) |
| role | Enum | Status akses ('Admin', 'Member') |

#### 3. Tabel Packages (Paket Gym-Pilates)
| Field | Tipe Data | Keterangan |
|---|---|---|
| id_paket | Integer (PK) | Primary Key, Auto Increment |
| nama_paket | Varchar | Contoh: "Private Pilates 4 Sesi" |
| harga | Decimal | Harga paket |
| kuota_sesi | Integer | Jumlah pertemuan/sesi yang didapat |
| deskripsi | Text | Penjelasan fasilitas paket |

#### 4. Tabel Schedules (Jadwal Kelas)
| Field | Tipe Data | Keterangan |
|---|---|---|
| id_jadwal | Integer (PK) | Primary Key, Auto Increment |
| tanggal | Date | Tanggal kelas berlangsung |
| jam_mulai | Time | Waktu mulai |
| instruktur | Varchar | Nama pelatih/instruktur |
| kapasitas_maks | Integer | Maksimal member dalam satu kelas |

#### 5. Tabel Bookings (Pemesanan & Transaksi)
| Field | Tipe Data | Keterangan |
|---|---|---|
| id_booking | Integer (PK) | Primary Key, Auto Increment |
| id_user | Integer (FK) | Relasi ke Tabel Users |
| id_paket | Integer (FK) | Relasi ke Tabel Packages |
| id_jadwal | Integer (FK) | Relasi ke Tabel Schedules |
| status_bayar | Enum | ('Pending', 'Lunas', 'Batal') |
| tanggal_booking | DateTime | Waktu saat melakukan pemesanan |

#### 6. Tabel Attendance (Absensi Kehadiran)
| Field | Tipe Data | Keterangan |
|---|---|---|
| id_absensi | Integer (PK) | Primary Key, Auto Increment |
| id_booking | Integer (FK) | Relasi ke Tabel Bookings |
| status_hadir | Enum | ('Hadir', 'Tidak Hadir') |
| waktu_hadir | DateTime | Timestamp otomatis saat divalidasi |

### Lampiran D: Alur Kerja Sistem (System Workflow)

**Alur Pemesanan dan Pembayaran (Booking Flow)**
1. Pelanggan melakukan proses Login ke dalam sistem.
2. Pelanggan membuka menu Katalog Paket dan memilih paket yang diinginkan.
3. Sistem menampilkan daftar Jadwal Tersedia (kuota belum penuh).
4. Pelanggan memilih jadwal kelas.
5. Sistem men-generate `id_booking` dengan status pembayaran Pending.
6. Pelanggan melakukan pembayaran dan sistem mencatat transaksi.
7. Admin melakukan verifikasi pembayaran di Dasbor Admin.
8. Status booking berubah menjadi Lunas.
9. Pelanggan dapat mengunduh Struk PDF.

**Alur Absensi (Attendance Flow)**
1. Pelanggan datang ke studio pada jadwal yang telah dibooking.
2. Pelanggan menyebutkan Nama atau ID Booking kepada Admin.
3. Admin mencari data pelanggan pada menu Absensi Hari Ini.
4. Admin menekan tombol Hadir.
5. Sistem mencatat `waktu_hadir` dan mengurangi `kuota_sesi` pelanggan pada database.