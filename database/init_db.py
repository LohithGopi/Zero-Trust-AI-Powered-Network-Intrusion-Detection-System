import os
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    users = db.relationship('User', backref='role_rel', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        role_name = self.role_rel.name if self.role_rel else "User"
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": role_name,
            "role_id": self.role_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(80), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)
    details = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username or "Anonymous",
            "action": self.action,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "details": self.details
        }


class DatasetHistory(db.Model):
    __tablename__ = 'dataset_history'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    dataset_type = db.Column(db.String(50), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    row_count = db.Column(db.Integer, default=0)
    col_count = db.Column(db.Integer, default=0)
    file_size_mb = db.Column(db.Float, default=0.0)
    filepath = db.Column(db.String(512), nullable=False)
    is_selected = db.Column(db.Boolean, default=False)
    upload_status = db.Column(db.String(50), default="Uploaded")
    
    # Real dataset metadata fields
    total_rows = db.Column(db.Integer, default=0)
    training_rows = db.Column(db.Integer, default=25000)
    target_col = db.Column(db.String(100), default="label")
    num_classes = db.Column(db.Integer, default=2)
    missing_count = db.Column(db.Integer, default=0)
    duplicate_count = db.Column(db.Integer, default=0)
    infinite_count = db.Column(db.Integer, default=0)
    class_distribution_json = db.Column(db.Text, nullable=True)

    def to_dict(self):
        class_dist = {}
        if self.class_distribution_json:
            try:
                class_dist = json.loads(self.class_distribution_json)
            except Exception:
                class_dist = {}

        return {
            "id": self.id,
            "filename": self.filename,
            "dataset_type": self.dataset_type,
            "upload_date": self.upload_date.strftime("%Y-%m-%d %H:%M:%S") if self.upload_date else "N/A",
            "row_count": self.row_count,
            "col_count": self.col_count,
            "file_size_mb": round(self.file_size_mb, 2),
            "filepath": self.filepath,
            "is_selected": self.is_selected,
            "upload_status": self.upload_status,
            "total_rows": self.total_rows or self.row_count,
            "training_rows": self.training_rows or self.row_count,
            "target_col": self.target_col,
            "num_classes": self.num_classes,
            "missing_count": self.missing_count,
            "duplicate_count": self.duplicate_count,
            "infinite_count": self.infinite_count,
            "class_distribution": class_dist
        }


class ModelHistory(db.Model):
    __tablename__ = 'model_history'

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    dataset_name = db.Column(db.String(255), nullable=False)
    trained_at = db.Column(db.DateTime, default=datetime.utcnow)
    accuracy = db.Column(db.Float, default=0.0)
    loss = db.Column(db.Float, default=0.0)
    precision = db.Column(db.Float, default=0.0)
    recall = db.Column(db.Float, default=0.0)
    f1_score = db.Column(db.Float, default=0.0)
    training_time = db.Column(db.Float, default=0.0)
    prediction_time = db.Column(db.Float, default=0.0)
    model_type = db.Column(db.String(100), default="Deep Learning")
    framework = db.Column(db.String(100), default="TensorFlow/Keras")
    model_status = db.Column(db.String(50), default="Trained")
    params_json = db.Column(db.Text, nullable=True)
    artifact_path = db.Column(db.String(512), nullable=True)
    
    total_dataset_rows = db.Column(db.Integer, default=0)
    training_rows = db.Column(db.Integer, default=0)
    random_seed = db.Column(db.Integer, default=42)

    def to_dict(self):
        return {
            "id": self.id,
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "trained_at": self.trained_at.strftime("%Y-%m-%d %H:%M:%S") if self.trained_at else "N/A",
            "accuracy": round(self.accuracy, 4),
            "loss": round(self.loss, 4),
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1_score": round(self.f1_score, 4),
            "training_time": round(self.training_time, 3),
            "prediction_time": round(self.prediction_time, 4),
            "model_type": self.model_type,
            "framework": self.framework,
            "model_status": self.model_status,
            "params_json": self.params_json,
            "artifact_path": self.artifact_path,
            "total_dataset_rows": self.total_dataset_rows,
            "training_rows": self.training_rows,
            "random_seed": self.random_seed
        }


class LiveDetection(db.Model):
    __tablename__ = 'live_detections'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    source_ip = db.Column(db.String(45), nullable=False)
    destination_ip = db.Column(db.String(45), nullable=False)
    source_port = db.Column(db.Integer, nullable=True)
    destination_port = db.Column(db.Integer, nullable=True)
    protocol = db.Column(db.String(20), nullable=False)
    flow_duration = db.Column(db.Float, default=0.0)
    packet_count = db.Column(db.Integer, default=0)
    bytes = db.Column(db.Integer, default=0)
    prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    risk_level = db.Column(db.String(20), nullable=False)
    interface = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default="Analyzed")

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else "N/A",
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "source_port": self.source_port,
            "destination_port": self.destination_port,
            "protocol": self.protocol,
            "flow_duration": round(self.flow_duration, 3),
            "packet_count": self.packet_count,
            "bytes": self.bytes,
            "prediction": self.prediction,
            "confidence": round(self.confidence, 4),
            "risk_level": self.risk_level,
            "interface": self.interface,
            "status": self.status
        }


def init_db(app):
    """Initialize database schemas and insert seed values efficiently."""
    db.init_app(app)

    with app.app_context():
        db_dir = os.path.dirname(app.config["DB_PATH"])
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        db.create_all()

        # Schema Migration Check for SQLite tables
        try:
            from sqlalchemy import text
            with db.engine.connect() as conn:
                # Check dataset_history table
                result_ds = conn.execute(text("PRAGMA table_info(dataset_history);"))
                ds_cols = {row[1] for row in result_ds.fetchall()}
                ds_columns_to_add = {
                    "total_rows": "INTEGER DEFAULT 0",
                    "training_rows": "INTEGER DEFAULT 25000",
                    "target_col": "VARCHAR(100) DEFAULT 'label'",
                    "num_classes": "INTEGER DEFAULT 2",
                    "missing_count": "INTEGER DEFAULT 0",
                    "duplicate_count": "INTEGER DEFAULT 0",
                    "infinite_count": "INTEGER DEFAULT 0",
                    "class_distribution_json": "TEXT"
                }
                for col_name, col_type in ds_columns_to_add.items():
                    if col_name not in ds_cols:
                        conn.execute(text(f"ALTER TABLE dataset_history ADD COLUMN {col_name} {col_type};"))

                # Check model_history table
                result_mh = conn.execute(text("PRAGMA table_info(model_history);"))
                mh_cols = {row[1] for row in result_mh.fetchall()}
                mh_columns_to_add = {
                    "training_time": "FLOAT DEFAULT 0.0",
                    "prediction_time": "FLOAT DEFAULT 0.0",
                    "model_type": "VARCHAR(100) DEFAULT 'Deep Learning'",
                    "framework": "VARCHAR(100) DEFAULT 'TensorFlow/Keras'",
                    "model_status": "VARCHAR(50) DEFAULT 'Trained'",
                    "params_json": "TEXT",
                    "artifact_path": "VARCHAR(512)",
                    "total_dataset_rows": "INTEGER DEFAULT 0",
                    "training_rows": "INTEGER DEFAULT 0",
                    "random_seed": "INTEGER DEFAULT 42"
                }
                for col_name, col_type in mh_columns_to_add.items():
                    if col_name not in mh_cols:
                        conn.execute(text(f"ALTER TABLE model_history ADD COLUMN {col_name} {col_type};"))

                conn.commit()
        except Exception as err:
            print(f"[DB MIGRATION NOTICE]: {err}")

        # Seed roles
        role_map = {}
        for role_name in app.config["ROLES"]:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                desc = f"Zero Trust {role_name} Role"
                role = Role(name=role_name, description=desc)
                db.session.add(role)
                db.session.commit()
            role_map[role_name] = role

        # Seed default role accounts (Admin, Analyst)
        from security.password import hash_password, check_password

        default_users = [
            ("admin", "admin@jnnce.ac.in", "admin123", "Admin"),
            ("analyst", "analyst@jnnce.ac.in", "analyst123", "Analyst")
        ]

        for uname, uemail, upass, rname in default_users:
            u_obj = User.query.filter_by(username=uname).first()
            if not u_obj:
                u_obj = User(
                    username=uname,
                    email=uemail,
                    password_hash=hash_password(upass),
                    role_id=role_map[rname].id
                )
                db.session.add(u_obj)
                db.session.commit()
            elif not check_password(upass, u_obj.password_hash):
                u_obj.password_hash = hash_password(upass)
                u_obj.role_id = role_map[rname].id
                db.session.commit()

        # Seed real benchmark datasets
        seed_real_benchmark_datasets()


def seed_real_benchmark_datasets():
    # If datasets already seeded, skip
    if DatasetHistory.query.first():
        return

    import pandas as pd
    from config import Config

    raw_dir = Config.DATASET_RAW_DIR
    os.makedirs(raw_dir, exist_ok=True)

    # 1. CIC-IDS2017 Real Kaggle Benchmark Dataset
    cic_path = os.path.join(raw_dir, "cicids2017", "cicids2017_raw.csv")
    if os.path.exists(cic_path):
        size_mb = round(os.path.getsize(cic_path) / (1024 * 1024), 2)
        ds_cic = DatasetHistory(
            filename="cicids2017_raw.csv",
            dataset_type="CIC-IDS2017",
            row_count=2830743,
            total_rows=2830743,
            training_rows=25000,
            col_count=79,
            file_size_mb=size_mb,
            filepath=cic_path,
            is_selected=False,
            upload_status="Uploaded",
            target_col="Label",
            num_classes=15,
            class_distribution_json=json.dumps({"BENIGN": 2273097, "DoS": 252661, "PortScan": 158930, "DDoS": 128027, "Web Attack": 2180})
        )
        db.session.add(ds_cic)

    # 2. UNSW-NB15 Real Network Flow Dataset
    unsw_path = os.path.join(raw_dir, "unsw_nb15", "unsw_nb15_raw.csv")
    if os.path.exists(unsw_path):
        size_mb = round(os.path.getsize(unsw_path) / (1024 * 1024), 2)
        ds_unsw = DatasetHistory(
            filename="unsw_nb15_raw.csv",
            dataset_type="UNSW-NB15",
            row_count=2540044,
            total_rows=2540044,
            training_rows=25000,
            col_count=49,
            file_size_mb=size_mb,
            filepath=unsw_path,
            is_selected=False,
            upload_status="Uploaded",
            target_col="attack_cat",
            num_classes=10,
            class_distribution_json=json.dumps({"Normal": 2218761, "Generic": 215481, "Exploits": 44525, "Fuzzers": 24246, "DoS": 16353})
        )
        db.session.add(ds_unsw)

    # 3. NSL-KDD Real Intrusion Dataset
    nsl_path = os.path.join(raw_dir, "nsl_kdd", "nsl_kdd_raw.csv")
    if not os.path.exists(nsl_path):
        nsl_path = os.path.join(raw_dir, "nsl_kdd_intrusion_dataset.csv")

    if os.path.exists(nsl_path):
        size_mb = round(os.path.getsize(nsl_path) / (1024 * 1024), 2)
        ds_nsl = DatasetHistory(
            filename=os.path.basename(nsl_path),
            dataset_type="NSL-KDD",
            row_count=148517,
            total_rows=148517,
            training_rows=148517,
            col_count=42,
            file_size_mb=size_mb,
            filepath=nsl_path,
            is_selected=True,
            upload_status="Uploaded",
            target_col="label",
            num_classes=5,
            class_distribution_json=json.dumps({"normal": 77054, "neptune": 41214, "satan": 4368, "ipsweep": 3740, "portsweep": 3131})
        )
        db.session.add(ds_nsl)

    db.session.commit()
