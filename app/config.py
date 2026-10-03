import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Kompatibilitas skema Supabase/PostgreSQL untuk SQLAlchemy
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    # Fallback lokal SQLite
    database_url = f"sqlite:///{os.path.join(INSTANCE_DIR, 'gym_pilates.db')}"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zenith-pilates-gym-secret-key-unindra-2026'
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Engine options untuk kestabilan koneksi serverless Supabase
    if not database_url.startswith("sqlite"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}
