import unittest
from datetime import date, time, datetime, timedelta
from app import create_app
from app.models import db, User, Package, Schedule, Booking, Attendance

class GymPilatesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create test admin
            admin = User(nama_lengkap="Admin Test", email="admin@test.com", role="Admin")
            admin.set_password("admin123")

            # Create test member
            member = User(nama_lengkap="Member Test", email="member@test.com", role="Member")
            member.set_password("member123")

            # Create package
            pkg = Package(nama_paket="Pilates Mat 4 Sesi", harga=400000.0, kuota_sesi=4, deskripsi="Tes paket")

            # Create schedule
            sch = Schedule(tanggal=date.today() + timedelta(days=1), jam_mulai=time(10, 0), instruktur="Coach Maya", kapasitas_maks=5)

            db.session.add_all([admin, member, pkg, sch])
            db.session.commit()

            self.admin_id = admin.id_user
            self.member_id = member.id_user
            self.pkg_id = pkg.id_paket
            self.sch_id = sch.id_jadwal

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ZENITH', response.data)
        self.assertIn(b'Pilates Mat 4 Sesi', response.data)

    def test_login_member(self):
        # Failed login
        resp = self.client.post('/auth/login', data={'email': 'member@test.com', 'password': 'wrong'}, follow_redirects=True)
        self.assertIn(b'Email atau password tidak sesuai', resp.data)

        # Successful member login
        resp = self.client.post('/auth/login', data={'email': 'member@test.com', 'password': 'member123'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Portal Pelanggan', resp.data)

    def test_member_booking_and_receipt(self):
        # Login first
        self.client.post('/auth/login', data={'email': 'member@test.com', 'password': 'member123'})

        # Book schedule
        resp = self.client.post('/member/book', data={'id_paket': self.pkg_id, 'id_jadwal': self.sch_id}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Pemesanan berhasil dibuat', resp.data)

        with self.app.app_context():
            booking = Booking.query.filter_by(id_user=self.member_id).first()
            self.assertIsNotNone(booking)
            self.assertEqual(booking.status_bayar, 'Pending')
            booking_id = booking.id_booking

        # Access receipt
        resp = self.client.get(f'/member/receipt/{booking_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'BUKTI PEMBAYARAN', resp.data)

    def test_admin_dashboard_and_attendance(self):
        # Login admin
        self.client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin123'})

        # Admin dashboard
        resp = self.client.get('/admin/dashboard')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Dasbor Administrator', resp.data)

        # Create booking for today
        with self.app.app_context():
            today_sch = Schedule(tanggal=date.today(), jam_mulai=time(14, 0), instruktur="Coach Amanda", kapasitas_maks=4)
            db.session.add(today_sch)
            db.session.commit()

            b = Booking(id_user=self.member_id, id_paket=self.pkg_id, id_jadwal=today_sch.id_jadwal, status_bayar='Lunas')
            db.session.add(b)
            db.session.commit()
            today_b_id = b.id_booking

        # Check attendance list
        resp = self.client.get('/admin/attendance')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Daftar Kehadiran Sesi', resp.data)

        # Mark attendance
        resp = self.client.post(f'/admin/attendance/mark/{today_b_id}', data={'status_hadir': 'Hadir'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        with self.app.app_context():
            att = Attendance.query.filter_by(id_booking=today_b_id).first()
            self.assertIsNotNone(att)
            self.assertEqual(att.status_hadir, 'Hadir')

if __name__ == '__main__':
    unittest.main()
