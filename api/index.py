import os
import sys

# Tambahkan direktori root proyek ke path Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

# Handler WSGI Vercel
if __name__ == '__main__':
    app.run()
