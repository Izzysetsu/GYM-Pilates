from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Member') # 'Admin' atau 'Member'
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relasi

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    @property
    def is_admin(self):
        return self.role.lower() == 'admin'

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Package(db.Model):
    __tablename__ = 'packages'

    id_paket = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_paket = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Numeric(12, 2), nullable=False)
    kuota_sesi = db.Column(db.Integer, nullable=False, default=1)
    deskripsi = db.Column(db.Text, nullable=True)

    # Relasi

    @property
    def formatted_harga(self):
        return f"Rp {int(self.harga):,}".replace(',', '.')

    def __repr__(self):
        return f"<Package {self.nama_paket} - {self.harga}>"


class Schedule(db.Model):
    __tablename__ = 'schedules'

    id_jadwal = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tanggal = db.Column(db.Date, nullable=False)
    jam_mulai = db.Column(db.Time, nullable=False)
    instruktur = db.Column(db.String(100), nullable=False)
    kapasitas_maks = db.Column(db.Integer, nullable=False, default=10)

    # Relasi

    @property
    def booked_count(self):
        return self.bookings.filter(Booking.status_bayar != 'Batal').count()

    @property
    def available_slots(self):
        return max(0, self.kapasitas_maks - self.booked_count)

    @property
    def is_full(self):
        return self.available_slots <= 0

    @property
    def formatted_jam(self):
        return self.jam_mulai.strftime('%H:%M') if self.jam_mulai else ''

    @property
    def formatted_tanggal(self):
        return self.tanggal.strftime('%d %b %Y') if self.tanggal else ''

    def __repr__(self):
        return f"<Schedule {self.tanggal} {self.jam_mulai} with {self.instruktur}>"


class Booking(db.Model):
    __tablename__ = 'bookings'

    id_booking = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE'), nullable=False)
    id_paket = db.Column(db.Integer, db.ForeignKey('packages.id_paket'), nullable=False)
    id_jadwal = db.Column(db.Integer, db.ForeignKey('schedules.id_jadwal'), nullable=False)
    status_bayar = db.Column(db.String(20), nullable=False, default='Pending') # 'Pending', 'Lunas', 'Batal'
    tanggal_booking = db.Column(db.DateTime, default=datetime.now)

    # Relasi dengan eager loading (lazy='joined') agar 1 query mengambil semua relasi
    user = db.relationship('User', backref=db.backref('bookings', lazy='dynamic'), lazy='joined')
    package = db.relationship('Package', backref=db.backref('bookings', lazy='dynamic'), lazy='joined')
    schedule = db.relationship('Schedule', backref=db.backref('bookings', lazy='dynamic'), lazy='joined')
    attendance = db.relationship('Attendance', backref=db.backref('booking', uselist=False), uselist=False, cascade='all, delete-orphan', lazy='joined')

    @property
    def kode_booking(self):
        return f"GP-{self.tanggal_booking.strftime('%y%m')}-{self.id_booking:04d}"

    @property
    def is_attended(self):
        return self.attendance is not None and self.attendance.status_hadir == 'Hadir'

    def __repr__(self):
        return f"<Booking {self.kode_booking} - {self.status_bayar}>"


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id_absensi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_booking = db.Column(db.Integer, db.ForeignKey('bookings.id_booking', ondelete='CASCADE'), nullable=False)
    status_hadir = db.Column(db.String(20), nullable=False, default='Hadir') # 'Hadir', 'Tidak Hadir'
    waktu_hadir = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Attendance ID:{self.id_absensi} Booking:{self.id_booking} {self.status_hadir}>"
