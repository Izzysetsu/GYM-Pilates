from datetime import date, time, datetime, timedelta
from app import create_app
from app.models import db, User, Package, Schedule, Booking, Attendance

app = create_app()

def seed_database():
    with app.app_context():
        # Drop all & recreate for fresh clean slate
        db.drop_all()
        db.create_all()
        print("Database tables initialized successfully.")

        # 1. Seed Users (Admin & Members)
        admin = User(
            nama_lengkap="Administrator Studio",
            email="admin@gympilates.com",
            role="Admin"
        )
        admin.set_password("admin123")

        member1 = User(
            nama_lengkap="Rifan Betra Setiawan",
            email="member@gympilates.com",
            role="Member"
        )
        member1.set_password("member123")

        member2 = User(
            nama_lengkap="Utari Kusuma Wardana",
            email="utari@gympilates.com",
            role="Member"
        )
        member2.set_password("utari123")

        member3 = User(
            nama_lengkap="Sri Wahyu Rifa Nur Hidayat",
            email="sri@gympilates.com",
            role="Member"
        )
        member3.set_password("sri123")

        db.session.add_all([admin, member1, member2, member3])
        db.session.commit()
        print("Users seeded: Admin & 3 Members.")

        # 2. Seed Packages (Paket Gym-Pilates)
        pkg1 = Package(
            nama_paket="Single Visit Reformer Pilates",
            harga=150000.00,
            kuota_sesi=1,
            deskripsi="1 Sesi pengenalan Reformer Pilates dengan bimbingan instruktur dasar. Cocok untuk pemula."
        )
        pkg2 = Package(
            nama_paket="Paket Mat Pilates 4 Sesi",
            harga=450000.00,
            kuota_sesi=4,
            deskripsi="4 Sesi penguatan core, perbaikan postur punggung, dan pernapasan ritmik menggunakan matras anti-slip premium."
        )
        pkg3 = Package(
            nama_paket="Paket Kombo Gym & Pilates 8 Sesi",
            harga=850000.00,
            kuota_sesi=8,
            deskripsi="8 Sesi fleksibel kombinasi latihan Reformer Pilates dan fasilitas gym beban bebas selama 30 hari."
        )
        pkg4 = Package(
            nama_paket="Private 1-on-1 Pilates VIP 10 Sesi",
            harga=1600000.00,
            kuota_sesi=10,
            deskripsi="10 Sesi privat eksklusif 1 pelatih 1 member. Penyesuaian program tubuh personal dan evaluasi postur mingguan."
        )
        pkg5 = Package(
            nama_paket="Unlimited Monthly Platinum Pass",
            harga=2300000.00,
            kuota_sesi=30,
            deskripsi="Akses tanpa batas seluruh kelas mat pilates, reformer group, fasilitas locker room sauna, dan konsultasi gizi."
        )

        db.session.add_all([pkg1, pkg2, pkg3, pkg4, pkg5])
        db.session.commit()
        print("Packages seeded: 5 paket.")

        # 3. Seed Schedules (Jadwal Kelas)
        today = date.today()
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)

        sch1 = Schedule(
            tanggal=today,
            jam_mulai=time(8, 0),
            instruktur="Amanda Stephanie",
            kapasitas_maks=8
        )
        sch2 = Schedule(
            tanggal=today,
            jam_mulai=time(10, 30),
            instruktur="Jessica Tan",
            kapasitas_maks=8
        )
        sch3 = Schedule(
            tanggal=today,
            jam_mulai=time(16, 0),
            instruktur="David Pratama",
            kapasitas_maks=10
        )
        sch4 = Schedule(
            tanggal=tomorrow,
            jam_mulai=time(9, 0),
            instruktur="Amanda Stephanie",
            kapasitas_maks=8
        )
        sch5 = Schedule(
            tanggal=tomorrow,
            jam_mulai=time(14, 0),
            instruktur="Jessica Tan",
            kapasitas_maks=8
        )
        sch6 = Schedule(
            tanggal=day_after,
            jam_mulai=time(10, 0),
            instruktur="David Pratama",
            kapasitas_maks=10
        )

        db.session.add_all([sch1, sch2, sch3, sch4, sch5, sch6])
        db.session.commit()
        print("Schedules seeded: 6 sesi kelas.")

        # 4. Seed Bookings (Pemesanan & Transaksi)
        # Booking 1: Rifan -> Sesi Hari ini jam 08:00 (Lunas & Sudah Hadir)
        b1 = Booking(
            id_user=member1.id_user,
            id_paket=pkg1.id_paket,
            id_jadwal=sch1.id_jadwal,
            status_bayar="Lunas",
            tanggal_booking=datetime.now() - timedelta(days=1)
        )

        # Booking 2: Utari -> Sesi Hari ini jam 10:30 (Lunas, Belum Hadir)
        b2 = Booking(
            id_user=member2.id_user,
            id_paket=pkg2.id_paket,
            id_jadwal=sch2.id_jadwal,
            status_bayar="Lunas",
            tanggal_booking=datetime.now() - timedelta(hours=6)
        )

        # Booking 3: Sri Wahyu -> Sesi Besok jam 09:00 (Pending)
        b3 = Booking(
            id_user=member3.id_user,
            id_paket=pkg3.id_paket,
            id_jadwal=sch4.id_jadwal,
            status_bayar="Pending",
            tanggal_booking=datetime.now() - timedelta(hours=2)
        )

        db.session.add_all([b1, b2, b3])
        db.session.commit()
        print("Bookings seeded: 3 pemesanan.")

        # 5. Seed Attendance (Absensi Kehadiran)
        # b1 sudah divalidasi hadir
        att1 = Attendance(
            id_booking=b1.id_booking,
            status_hadir="Hadir",
            waktu_hadir=datetime.combine(today, time(8, 5))
        )
        db.session.add(att1)
        db.session.commit()
        print("Attendance seeded: 1 record kehadiran.")

        print("\n=======================================================")
        print("[SUKSES] Seeding Selesai! Data awal aplikasi siap digunakan:")
        print("Admin:  admin@gympilates.com  |  password: admin123")
        print("Member: member@gympilates.com |  password: member123")
        print("=======================================================\n")

if __name__ == '__main__':
    seed_database()
