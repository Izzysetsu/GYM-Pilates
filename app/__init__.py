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

    # Aman dari serverless error: jangan crash jika create_all gagal atau tabel sudah ada
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"[WARN] db.create_all caught: {e}")

    return app
