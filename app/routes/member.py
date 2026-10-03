from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, abort
from .. import member_required
from ..models import db, Package, Schedule, Booking, Attendance

member_bp = Blueprint('member', __name__)

@member_bp.before_request
@member_required
def require_member():
    pass

@member_bp.route('/dashboard')
def dashboard():
    user = g.user
    user_bookings = Booking.query.filter_by(id_user=user.id_user).order_by(Booking.tanggal_booking.desc()).all()
    
    total_bookings = len(user_bookings)
    pending_bookings = sum(1 for b in user_bookings if b.status_bayar == 'Pending')
    lunas_bookings = sum(1 for b in user_bookings if b.status_bayar == 'Lunas')
    total_hadir = sum(1 for b in user_bookings if b.is_attended)
    
    # Upcoming sessions (Lunas and date >= today)
    today = date.today()
    upcoming = [b for b in user_bookings if b.status_bayar == 'Lunas' and b.schedule.tanggal >= today]
    upcoming.sort(key=lambda b: (b.schedule.tanggal, b.schedule.jam_mulai))

    recent_bookings = user_bookings[:5]

    return render_template(
        'member/dashboard.html',
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        lunas_bookings=lunas_bookings,
        total_hadir=total_hadir,
        upcoming=upcoming,
        recent_bookings=recent_bookings
    )

@member_bp.route('/packages')
def packages():
    package_list = Package.query.all()
    return render_template('member/packages.html', packages=package_list)

@member_bp.route('/book', methods=['GET', 'POST'])
def book():
    packages = Package.query.all()
    today = date.today()
    schedules = Schedule.query.filter(Schedule.tanggal >= today).order_by(Schedule.tanggal.asc(), Schedule.jam_mulai.asc()).all()

    selected_pkg_id = request.args.get('package_id', type=int)

    if request.method == 'POST':
        id_paket = request.form.get('id_paket', type=int)
        id_jadwal = request.form.get('id_jadwal', type=int)

        if not id_paket or not id_jadwal:
            flash('Harap pilih paket dan jadwal sesi latihan.', 'warning')
            return redirect(url_for('member.book', package_id=id_paket))

        paket = db.session.get(Package, id_paket)
        jadwal = db.session.get(Schedule, id_jadwal)

        if not paket or not jadwal:
            flash('Paket atau jadwal yang dipilih tidak valid.', 'danger')
            return redirect(url_for('member.book'))

        # Cek apakah jadwal sudah lewat
        if jadwal.tanggal < today:
            flash('Tidak dapat memesan sesi untuk tanggal yang sudah lewat.', 'danger')
            return redirect(url_for('member.book'))

        # Cek kuota kapasitas
        if jadwal.is_full:
            flash(f'Maaf, kuota untuk jadwal ini sudah penuh ({jadwal.kapasitas_maks} peserta). Silakan pilih jadwal lain.', 'danger')
            return redirect(url_for('member.book', package_id=id_paket))

        # Cek apakah member sudah pernah booking jadwal ini dan statusnya belum batal
        existing_booking = Booking.query.filter_by(
            id_user=g.user.id_user,
            id_jadwal=id_jadwal
        ).filter(Booking.status_bayar != 'Batal').first()

        if existing_booking:
            flash('Anda sudah memiliki pemesanan aktif untuk jadwal sesi ini.', 'warning')
            return redirect(url_for('member.bookings'))

        new_booking = Booking(
            id_user=g.user.id_user,
            id_paket=id_paket,
            id_jadwal=id_jadwal,
            status_bayar='Pending',
            tanggal_booking=datetime.now()
        )

        db.session.add(new_booking)
        db.session.commit()

        flash(f'Pemesanan berhasil dibuat dengan kode {new_booking.kode_booking}! Silakan selesaikan pembayaran.', 'success')
        return redirect(url_for('member.bookings'))

    return render_template(
        'member/book.html',
        packages=packages,
        schedules=schedules,
        selected_pkg_id=selected_pkg_id
    )

@member_bp.route('/bookings')
def bookings():
    status_filter = request.args.get('status')
    query = Booking.query.filter_by(id_user=g.user.id_user)

    if status_filter in ['Pending', 'Lunas', 'Batal']:
        query = query.filter_by(status_bayar=status_filter)

    booking_list = query.order_by(Booking.tanggal_booking.desc()).all()
    return render_template('member/bookings.html', bookings=booking_list, active_status=status_filter)

@member_bp.route('/booking/<int:id_booking>/pay', methods=['POST'])
def pay(id_booking):
    booking = db.session.get(Booking, id_booking)
    if not booking or booking.id_user != g.user.id_user:
        abort(404)

    metode = request.form.get('metode', 'Transfer Bank BCA')
    flash(f'Konfirmasi pembayaran untuk {booking.kode_booking} via {metode} telah dikirim ke Admin Studio untuk verifikasi.', 'success')
    return redirect(url_for('member.bookings'))

@member_bp.route('/receipt/<int:id_booking>')
def receipt(id_booking):
    booking = db.session.get(Booking, id_booking)
    if not booking or (booking.id_user != g.user.id_user and not g.user.is_admin):
        abort(403)

    return render_template('member/receipt.html', booking=booking)
