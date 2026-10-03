import os
import sys

# Ensure root directory is added to sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import create_app

# Vercel WSGI entry point
app = create_app()

if __name__ == '__main__':
    app.run()
