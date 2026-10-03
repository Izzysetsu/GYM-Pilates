from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, abort
from .. import admin_required
from ..models import db, User, Package, Schedule, Booking, Attendance

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@admin_required
def require_admin():
    pass

@admin_bp.route('/dashboard')
def dashboard():
    today = date.today()

    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status_bayar='Pending').count()
    lunas_bookings = Booking.query.filter_by(status_bayar='Lunas').count()

    # Total pendapatan dihitung langsung di database menggunakan SQL SUM instan (0.01 detik)
    total_revenue = db.session.query(db.func.sum(Package.harga)).join(
        Booking, Booking.id_paket == Package.id_paket
    ).filter(Booking.status_bayar == 'Lunas').scalar() or 0

    total_members = User.query.filter_by(role='Member').count()
    schedules_today = Schedule.query.filter_by(tanggal=today).count()

    recent_bookings = Booking.query.order_by(Booking.tanggal_booking.desc()).limit(8).all()
    today_schedules = Schedule.query.filter_by(tanggal=today).order_by(Schedule.jam_mulai.asc()).all()

    return render_template(
        'admin/dashboard.html',
        total_revenue=total_revenue,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        lunas_bookings=lunas_bookings,
        total_members=total_members,
        schedules_today=schedules_today,
        recent_bookings=recent_bookings,
        today_schedules=today_schedules,
        today=today
    )

# --- CRUD PAKET ---
@admin_bp.route('/packages')
def packages():
    package_list = Package.query.order_by(Package.id_paket.asc()).all()
    return render_template('admin/packages.html', packages=package_list)

@admin_bp.route('/packages/add', methods=['POST'])
def add_package():
    nama_paket = request.form.get('nama_paket', '').strip()
    harga = request.form.get('harga', type=float)
    kuota_sesi = request.form.get('kuota_sesi', type=int)
    deskripsi = request.form.get('deskripsi', '').strip()

    if not nama_paket or harga is None or not kuota_sesi:
        flash('Harap lengkapi semua kolom paket yang wajib diisi.', 'danger')
        return redirect(url_for('admin.packages'))

    paket = Package(
        nama_paket=nama_paket,
        harga=harga,
        kuota_sesi=kuota_sesi,
        deskripsi=deskripsi
    )
    db.session.add(paket)
    db.session.commit()

    flash(f'Paket "{nama_paket}" berhasil ditambahkan!', 'success')
    return redirect(url_for('admin.packages'))

@admin_bp.route('/packages/<int:id_paket>/edit', methods=['POST'])
def edit_package(id_paket):
    paket = db.session.get(Package, id_paket)
    if not paket:
        abort(404)

    paket.nama_paket = request.form.get('nama_paket', '').strip()
    paket.harga = request.form.get('harga', type=float)
    paket.kuota_sesi = request.form.get('kuota_sesi', type=int)
    paket.deskripsi = request.form.get('deskripsi', '').strip()

    db.session.commit()
    flash(f'Paket "{paket.nama_paket}" berhasil diperbarui!', 'success')
    return redirect(url_for('admin.packages'))

@admin_bp.route('/packages/<int:id_paket>/delete', methods=['POST'])
def delete_package(id_paket):
    paket = db.session.get(Package, id_paket)
    if not paket:
        abort(404)

    # Cek apakah ada booking aktif yang mereferensikan paket ini
    active_booking_count = paket.bookings.count()
    if active_booking_count > 0:
        flash(f'Paket tidak dapat dihapus karena sudah memiliki {active_booking_count} data pemesanan terkait.', 'danger')
        return redirect(url_for('admin.packages'))

    db.session.delete(paket)
    db.session.commit()
    flash('Paket berhasil dihapus.', 'info')
    return redirect(url_for('admin.packages'))


# --- CRUD JADWAL ---
@admin_bp.route('/schedules')
def schedules():
    schedule_list = Schedule.query.order_by(Schedule.tanggal.desc(), Schedule.jam_mulai.asc()).all()
    return render_template('admin/schedules.html', schedules=schedule_list)

@admin_bp.route('/schedules/add', methods=['POST'])
def add_schedule():
    tanggal_str = request.form.get('tanggal')
    jam_str = request.form.get('jam_mulai')
    instruktur = request.form.get('instruktur', '').strip()
    kapasitas_maks = request.form.get('kapasitas_maks', type=int)

    if not tanggal_str or not jam_str or not instruktur or not kapasitas_maks:
        flash('Harap lengkapi semua kolom jadwal.', 'danger')
        return redirect(url_for('admin.schedules'))

    try:
        tanggal_obj = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
        jam_obj = datetime.strptime(jam_str, '%H:%M').time()
    except ValueError:
        flash('Format tanggal atau jam tidak valid.', 'danger')
        return redirect(url_for('admin.schedules'))

    jadwal = Schedule(
        tanggal=tanggal_obj,
        jam_mulai=jam_obj,
        instruktur=instruktur,
        kapasitas_maks=kapasitas_maks
    )
    db.session.add(jadwal)
    db.session.commit()

    flash(f'Jadwal sesi bersama {instruktur} berhasil ditambahkan!', 'success')
    return redirect(url_for('admin.schedules'))

@admin_bp.route('/schedules/<int:id_jadwal>/edit', methods=['POST'])
def edit_schedule(id_jadwal):
    jadwal = db.session.get(Schedule, id_jadwal)
    if not jadwal:
        abort(404)

    tanggal_str = request.form.get('tanggal')
    jam_str = request.form.get('jam_mulai')
    instruktur = request.form.get('instruktur', '').strip()
    kapasitas_maks = request.form.get('kapasitas_maks', type=int)

    try:
        jadwal.tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
        jadwal.jam_mulai = datetime.strptime(jam_str, '%H:%M').time()
        jadwal.instruktur = instruktur
        jadwal.kapasitas_maks = kapasitas_maks
        db.session.commit()
        flash('Jadwal berhasil diperbarui.', 'success')
    except Exception as e:
        flash(f'Gagal memperbarui jadwal: {str(e)}', 'danger')

    return redirect(url_for('admin.schedules'))

@admin_bp.route('/schedules/<int:id_jadwal>/delete', methods=['POST'])
def delete_schedule(id_jadwal):
    jadwal = db.session.get(Schedule, id_jadwal)
    if not jadwal:
        abort(404)

    if jadwal.bookings.count() > 0:
        flash('Jadwal tidak dapat dihapus karena sudah memiliki peserta yang mendaftar.', 'danger')
        return redirect(url_for('admin.schedules'))

    db.session.delete(jadwal)
    db.session.commit()
    flash('Jadwal berhasil dihapus.', 'info')
    return redirect(url_for('admin.schedules'))


# --- KELOLA TRANSAKSI / BOOKINGS ---
@admin_bp.route('/bookings')
def bookings():
    status_filter = request.args.get('status')
    query = Booking.query

    if status_filter in ['Pending', 'Lunas', 'Batal']:
        query = query.filter_by(status_bayar=status_filter)

    booking_list = query.order_by(Booking.tanggal_booking.desc()).all()
    return render_template('admin/bookings.html', bookings=booking_list, active_status=status_filter)

@admin_bp.route('/bookings/<int:id_booking>/status', methods=['POST'])
def update_booking_status(id_booking):
    booking = db.session.get(Booking, id_booking)
    if not booking:
        abort(404)

    new_status = request.form.get('status_bayar')
    if new_status in ['Pending', 'Lunas', 'Batal']:
        booking.status_bayar = new_status
        db.session.commit()
        flash(f'Status pemesanan {booking.kode_booking} berhasil diubah menjadi "{new_status}".', 'success')
    else:
        flash('Status tidak valid.', 'danger')

    return redirect(url_for('admin.bookings'))


# --- MODUL ABSENSI STUDIO ---
@admin_bp.route('/attendance')
def attendance():
    tanggal_str = request.args.get('tanggal')
    if tanggal_str:
        try:
            target_date = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    # Dapatkan semua booking yang lunas pada tanggal tersebut
    bookings_today = Booking.query.join(Schedule).filter(
        Schedule.tanggal == target_date,
        Booking.status_bayar == 'Lunas'
    ).order_by(Schedule.jam_mulai.asc()).all()

    return render_template(
        'admin/attendance.html',
        bookings=bookings_today,
        target_date=target_date
    )

@admin_bp.route('/attendance/mark/<int:id_booking>', methods=['POST'])
def mark_attendance(id_booking):
    booking = db.session.get(Booking, id_booking)
    if not booking:
        abort(404)

    status_hadir = request.form.get('status_hadir', 'Hadir')

    if booking.attendance:
        booking.attendance.status_hadir = status_hadir
        booking.attendance.waktu_hadir = datetime.now()
    else:
        absensi = Attendance(
            id_booking=booking.id_booking,
            status_hadir=status_hadir,
            waktu_hadir=datetime.now()
        )
        db.session.add(absensi)

    db.session.commit()
    flash(f'Presensi untuk {booking.user.nama_lengkap} berhasil ditandai sebagai "{status_hadir}".', 'success')
    
    # Kembali ke tanggal jadwal terkait
    return redirect(url_for('admin.attendance', tanggal=booking.schedule.tanggal.strftime('%Y-%m-%d')))
