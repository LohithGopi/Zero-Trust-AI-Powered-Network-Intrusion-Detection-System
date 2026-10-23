import sys
import os

sys.path.insert(0, r"E:\ML")

print(f"Python executable: {sys.executable}", flush=True)
print(f"Current working dir: {os.getcwd()}", flush=True)

# 1. Config import
import config
from config import Config
print(f"BASE_DIR: {config.BASE_DIR}", flush=True)
print(f"DB_PATH: {Config.DB_PATH}", flush=True)
print(f"SQLALCHEMY_DATABASE_URI: {Config.SQLALCHEMY_DATABASE_URI}", flush=True)
print(f"DATASET_RAW_DIR: {Config.DATASET_RAW_DIR}", flush=True)

# 2. Database import
from database.init_db import db, DatasetHistory, ModelHistory
print("Database models imported successfully.", flush=True)

# 3. Check database contents
import sqlite3
con = sqlite3.connect(Config.DB_PATH)
cur = con.cursor()
datasets = cur.execute("SELECT id, filename, filepath FROM dataset_history").fetchall()
print(f"Found {len(datasets)} datasets in DB:", flush=True)
for d in datasets:
    exists = os.path.exists(d[2])
    print(f"  - [{d[0]}] {d[1]} -> {d[2]} (Exists on disk: {exists})", flush=True)

models = cur.execute("SELECT id, model_name, artifact_path FROM model_history").fetchall()
print(f"Found {len(models)} models in DB:", flush=True)
for m in models:
    exists = os.path.exists(m[2])
    print(f"  - [{m[0]}] {m[1]} -> {m[2]} (Exists on disk: {exists})", flush=True)
con.close()

# 4. Check App import
print("Importing app modules...", flush=True)
from api.auth_routes import auth_bp
print("auth_bp imported", flush=True)
from api.dataset_routes import dataset_bp
print("dataset_bp imported", flush=True)
from api.model_routes import model_bp
print("model_bp imported", flush=True)
from api.live_detection_routes import live_detection_bp
print("live_detection_bp imported", flush=True)

from app import create_app
print("Calling create_app()...", flush=True)
test_app = create_app()
print(f"Flask App created successfully with root_path: {test_app.root_path}", flush=True)
print("ALL VERIFICATIONS PASSED SUCCESSFULLY ON E:\\ML!", flush=True)
