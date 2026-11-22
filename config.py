import os
import secrets

# Suppress TensorFlow verbose info logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Central configuration class for AI Zero Trust NIDS Application."""
    
    # Secret keys for sessions and JWT (Zero Trust: loaded from env or cryptographically generated)
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or secrets.token_hex(32)
    JWT_EXPIRATION_HOURS = 8

    # Database Configuration
    DB_PATH = os.path.join(BASE_DIR, "database", "database.db")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directory Paths
    DATASET_RAW_DIR = os.path.join(BASE_DIR, "datasets", "raw")
    DATASET_SAMPLED_DIR = os.path.join(BASE_DIR, "datasets", "sampled")
    DATASET_PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    # Dataset Default Limits & Specifications
    DATASET_LIMITS = {
        "CIC-IDS2017": {
            "total_rows": 2830743,
            "default_training_rows": 25000,
            "min_training_rows": 25000,
            "max_training_rows": 50000,
            "allow_full": False
        },
        "UNSW-NB15": {
            "total_rows": 2540044,
            "default_training_rows": 25000,
            "min_training_rows": 25000,
            "max_training_rows": 50000,
            "allow_full": False
        },
        "NSL-KDD": {
            "total_rows": 148517,
            "default_training_rows": 148517,
            "min_training_rows": 1000,
            "max_training_rows": 148517,
            "allow_full": True
        }
    }

    # Artifact File Paths
    MODEL_FILE_PATH = os.path.join(MODEL_DIR, "lstm_model.keras")
    SCALER_FILE_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
    ENCODER_FILE_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
    REPORT_FILE_PATH = os.path.join(MODEL_DIR, "latest_report.json")

    # Allowed Upload File Extensions
    ALLOWED_EXTENSIONS = {"csv"}

    # Zero Trust & Role Configuration
    ROLES = ["Admin", "Analyst"]
    DEFAULT_ADMIN_USER = "admin"
    DEFAULT_ADMIN_PASS = "Admin@123"
    DEFAULT_ADMIN_EMAIL = "admin@zerotrust-nids.local"

    # Known Dataset Preset Column Mappings
    DATASET_SCHEMAS = {
        "NSL-KDD": [
            "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
            "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
            "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
            "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
            "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
            "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
            "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
            "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
            "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"
        ],
        "UNSW-NB15": [
            "dur", "proto", "service", "state", "spkts", "dpkts", "sbytes", "dbytes",
            "rate", "sttl", "dttl", "sload", "dload", "sloss", "dloss", "sinpkt",
            "dinpkt", "sjit", "djit", "swnd", "dwnd", "tcprtt", "synack", "ackdat",
            "smean", "dmean", "trans_depth", "response_body_len", "ct_srv_src",
            "ct_state_ttl", "ct_dst_ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm",
            "ct_dst_src_ltm", "is_ftp_login", "ct_ftp_cmd", "ct_flw_http_mthd",
            "ct_src_ltm", "ct_srv_dst", "is_sm_ips_ports", "label"
        ],
        "CICIDS2017": [
            "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
            "Total Length of Fwd Packets", "Total Length of Bwd Packets", "Fwd Packet Length Max",
            "Fwd Packet Length Min", "Fwd Packet Length Mean", "Bwd Packet Length Max",
            "Bwd Packet Length Min", "Bwd Packet Length Mean", "Flow Bytes/s", "Flow Packets/s",
            "Flow IAT Mean", "Flow IAT Std", "FIN Flag Count", "SYN Flag Count", "RST Flag Count",
            "PSH Flag Count", "ACK Flag Count", "URG Flag Count", "Label"
        ]
    }

    @staticmethod
    def init_app(app):
        """Ensure required directories exist on startup."""
        for path in [Config.DATASET_RAW_DIR, Config.DATASET_PROCESSED_DIR, Config.MODEL_DIR, Config.LOG_DIR]:
            os.makedirs(path, exist_ok=True)
