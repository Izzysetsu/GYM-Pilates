from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('member.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Harap masukkan email dan password.', 'warning')
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id_user
            session['role'] = user.role
            session['nama_lengkap'] = user.nama_lengkap

            flash(f'Selamat datang kembali, {user.nama_lengkap}!', 'success')

            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('member.dashboard'))
        else:
            flash('Email atau password tidak sesuai. Silakan coba lagi.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('member.dashboard'))

    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not nama_lengkap or not email or not password:
            flash('Semua kolom wajib diisi.', 'warning')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Konfirmasi password tidak cocok.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password minimal terdiri dari 6 karakter.', 'warning')
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email sudah terdaftar. Silakan login atau gunakan email lain.', 'danger')
            return render_template('auth/register.html')

        new_user = User(
            nama_lengkap=nama_lengkap,
            email=email,
            role='Member'
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Pendaftaran akun berhasil! Silakan login untuk mulai booking kelas.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Anda telah berhasil keluar (logout).', 'info')
    return redirect(url_for('auth.login'))
