import os
from functools import wraps
from flask import Flask, session, redirect, url_for, flash, g
from .config import Config
from .models import db, User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu untuk mengakses halaman ini.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login sebagai Admin.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'Admin':
            flash('Akses ditolak. Halaman ini hanya untuk Administrator studio.', 'danger')
            return redirect(url_for('member.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def member_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'Member':
            flash('Akses dialihkan ke dashboard Admin.', 'info')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def create_app(config_class=Config):
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            try:
                g.user = db.session.get(User, user_id)
            except Exception:
                g.user = None

    @app.context_processor
    def inject_user():
        return dict(current_user=getattr(g, 'user', None))

    # Health check route
    @app.route('/health')
    def health():
        db_status = "ok"
        try:
            db.session.execute(db.text("SELECT 1"))
        except Exception as e:
            db_status = f"db error: {str(e)}"
        return {
            "status": "healthy",
            "database": db_status,
            "database_uri": app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else "local"
        }

    # Register blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.member import member_bp
    from .routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(member_bp, url_prefix='/member')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # db.create_all() dihilangkan dari runtime serverless karena skema sudah dibuat di Supabase


    # Tangkap error 500 dan tampilkan pesan diagnostik jelas
    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        err_msg = traceback.format_exc()
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        safe_uri = db_uri.split('@')[-1] if '@' in db_uri else db_uri
        has_env = "DATABASE_URL" in os.environ
        raw_env_preview = os.environ.get('DATABASE_URL', '')[:25] + '...' if has_env else 'TIDAK ADA'

        return f'''
        <div style="font-family: system-ui, sans-serif; max-width: 850px; margin: 3rem auto; padding: 2rem; background: #FFF; color: #111; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <span style="background: #FEE2E2; color: #DC2626; font-weight: 800; font-size: 1.25rem; padding: 0.5rem 0.8rem; border-radius: 8px;">500</span>
                <h2 style="margin: 0; color: #DC2626;">Diagnostik Kesalahan Aplikasi di Vercel</h2>
            </div>
            
            <div style="background: #FEF2F2; border-left: 4px solid #DC2626; padding: 1rem; border-radius: 4px; margin-bottom: 1.5rem;">
                <strong>Deskripsi:</strong> {str(e)}
            </div>

            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem; font-size: 0.9rem; line-height: 1.6;">
                <div><strong>Status Environment Variable:</strong> <span style="color: {'#16A34A' if has_env else '#DC2626'}; font-weight: 700;">{'DATABASE_URL Ditemukan (' + raw_env_preview + ')' if has_env else 'DATABASE_URL TIDAK DITEMUKAN di Environment Variables Vercel!'}</span></div>
                <div><strong>Target Database:</strong> {safe_uri}</div>
            </div>

            <strong>Traceback Lengkap:</strong>
            <pre style="background: #0F172A; color: #38BDF8; padding: 1.25rem; border-radius: 8px; overflow-x: auto; font-size: 0.8rem; line-height: 1.5; margin-top: 0.5rem;">{err_msg}</pre>
        </div>
        ''', 500

    return app

