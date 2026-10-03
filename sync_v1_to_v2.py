# Script Sinkronisasi Otomatis dari V1 (Lokal Terkunci) ke V2 (Cloud/Vercel)
import os
import shutil

V1_DIR = r"d:\PROGRAM\Gym-Pilates"
V2_DIR = r"d:\PROGRAM\Gym-Pilates-V2"

# File dan folder yang disinkronkan dari V1
DIRS_TO_SYNC = ["app"]
FILES_TO_SYNC = ["seed.py", "run.py", "test_app.py", "spec.md"]

print("Memulai sinkronisasi dari V1 ke V2...")

for folder in DIRS_TO_SYNC:
    src_f = os.path.join(V1_DIR, folder)
    dst_f = os.path.join(V2_DIR, folder)
    if os.path.exists(src_f):
        # Kecualikan config.py agar setting Supabase V2 tidak tertimpa
        for root, dirs, files in os.walk(src_f):
            rel_root = os.path.relpath(root, src_f)
            dst_root = os.path.join(dst_f, rel_root)
            os.makedirs(dst_root, exist_ok=True)
            for file in files:
                if file == "config.py":
                    continue
                shutil.copy2(os.path.join(root, file), os.path.join(dst_root, file))
        print(f"[SYNC] Folder {folder} berhasil diperbarui.")

for file in FILES_TO_SYNC:
    src_p = os.path.join(V1_DIR, file)
    dst_p = os.path.join(V2_DIR, file)
    if os.path.exists(src_p):
        shutil.copy2(src_p, dst_p)
        print(f"[SYNC] Berkas {file} berhasil disinkronkan.")

print("Sinkronisasi selesai! Versi 2 siap di-push.")
