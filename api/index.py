import os
import sys
import traceback

# Pastikan root directory ada di sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from app import create_app
    app = create_app()
except Exception as e:
    # Jika ada error saat startup, tampilkan langsung di browser agar jelas penyebabnya
    err_trace = traceback.format_exc()
    print("FATAL ERROR IN VERCEL PYTHON:")
    print(err_trace)

    from flask import Flask
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f'''
        <div style="font-family: sans-serif; padding: 2rem; background: #FFF; color: #111;">
            <h2 style="color: #DC2626;">Diagnostik Startup Error Vercel</h2>
            <p>Aplikasi gagal inisialisasi pada saat cold start:</p>
            <pre style="background: #F3F4F6; padding: 1.5rem; border-radius: 8px; border: 1px solid #E5E7EB; overflow-x: auto;">{err_trace}</pre>
        </div>
        ''', 500

if __name__ == '__main__':
    app.run()
