import os
import re
import ssl

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

database_url = os.environ.get('DATABASE_URL')
if database_url:
    database_url = database_url.strip()

    # Otomatis alihkan direct IPv6 host ke IPv4 Connection Pooler ap-southeast-2
    match = re.search(r'postgresql(?:\+[a-z0-9]+)?://([^:]+):([^@]+)@db\.([a-z0-9]+)\.supabase\.co(?::\d+)?/(.+)', database_url)
    if match:
        user_name, password, project_ref, dbname = match.groups()
        database_url = f"postgresql+pg8000://postgres.{project_ref}:{password}@aws-0-ap-southeast-2.pooler.supabase.com:6543/{dbname}"
    else:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+pg8000://", 1)
        elif database_url.startswith("postgresql://") and "+pg8000" not in database_url:
            database_url = database_url.replace("postgresql://", "postgresql+pg8000://", 1)
else:
    if os.environ.get('VERCEL'):
        database_url = "sqlite:////tmp/gym_pilates.db"
    else:
        database_url = f"sqlite:///{os.path.join(INSTANCE_DIR, 'gym_pilates.db')}"

# Konfigurasi SSL Context agar pg8000 tidak hang saat koneksi ke Supabase pooler
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zenith-pilates-gym-secret-key-unindra-2026'
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    if "pg8000" in database_url:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "ssl_context": ssl_ctx,
                "timeout": 8
            },
            "pool_pre_ping": False,
            "pool_recycle": 280,
        }
    elif not database_url.startswith("sqlite"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": False,
            "pool_recycle": 280,
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}
