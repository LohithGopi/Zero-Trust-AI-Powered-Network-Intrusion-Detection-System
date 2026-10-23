import os
import pandas as pd
import numpy as np
from config import Config
from utils.logger import logger

class DatasetLoader:
    """Loader module for network intrusion detection CSV datasets."""

    @staticmethod
    def load_dataset(filepath: str, dataset_type: str = "Custom") -> pd.DataFrame:
        """Load CSV dataset into Pandas DataFrame and apply schema mappings if needed."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file not found at: {filepath}")

        logger.info(f"Loading dataset: {os.path.basename(filepath)} (Type: {dataset_type})")

        # Load raw CSV
        try:
            df = pd.read_csv(filepath, low_memory=False)
        except Exception as e:
            # Fallback handling for headerless CSVs (e.g. raw NSL-KDD)
            if dataset_type in Config.DATASET_SCHEMAS:
                headers = Config.DATASET_SCHEMAS[dataset_type]
                df = pd.read_csv(filepath, header=None, names=headers, low_memory=False)
            else:
                raise ValueError(f"Failed to parse CSV file: {str(e)}")

        # Ensure header mapping if headerless DataFrame loaded with default integers
        if dataset_type in Config.DATASET_SCHEMAS and len(df.columns) == len(Config.DATASET_SCHEMAS[dataset_type]):
            if str(df.columns[0]).isdigit():
                df.columns = Config.DATASET_SCHEMAS[dataset_type]

        # Standardize target label column name
        df = DatasetLoader.standardize_label_column(df, dataset_type)
        return df

    @staticmethod
    def standardize_label_column(df: pd.DataFrame, dataset_type: str) -> pd.DataFrame:
        """Standardize attack label column across different benchmark datasets."""
        possible_label_cols = ["label", "Label", "attack_cat", "class", "target", "Label ", "prediction", "ground_truth"]
        found_col = None

        for col in possible_label_cols:
            if col in df.columns:
                found_col = col
                break

        if found_col and found_col != "label":
            df.rename(columns={found_col: "label"}, inplace=True)
        elif not found_col and "label" not in df.columns:
            # Pick last column as target if label not found explicitly, excluding known metadata columns
            last_col = df.columns[-1]
            meta_cols = {"model_name", "interface", "status", "risk_level", "confidence", "prediction", "timestamp", "id"}
            if str(last_col).lower() not in meta_cols:
                df.rename(columns={last_col: "label"}, inplace=True)
            elif "prediction" in df.columns:
                df["label"] = df["prediction"]
            elif "status" in df.columns:
                df["label"] = df["status"]
            else:
                df["label"] = "Normal"

        # Clean target string whitespace
        df["label"] = df["label"].astype(str).str.strip()
        return df

    @staticmethod
    def generate_synthetic_dataset(filename: str = "synthetic_nids_sample.csv", num_samples: int = 1500) -> str:
        """Generate a realistic synthetic network traffic dataset for immediate testing out of the box."""
        np.random.seed(42)

        protocols = ["tcp", "udp", "icmp"]
        flags = ["SF", "S0", "REJ", "RSTR", "SH"]
        attack_types = ["Normal", "DoS", "Probe", "R2L", "U2R"]

        data = {
            "flow_duration": np.random.exponential(scale=12.5, size=num_samples).round(4),
            "protocol": np.random.choice(protocols, size=num_samples, p=[0.7, 0.25, 0.05]),
            "src_port": np.random.randint(1024, 65535, size=num_samples),
            "dst_port": np.random.choice([80, 443, 22, 21, 53, 3389, 8080], size=num_samples),
            "packet_count": np.random.randint(1, 500, size=num_samples),
            "bytes_sent": np.random.randint(40, 150000, size=num_samples),
            "bytes_received": np.random.randint(40, 300000, size=num_samples),
            "avg_packet_size": np.random.uniform(50.0, 1460.0, size=num_samples).round(2),
            "packets_per_sec": np.random.uniform(0.1, 5000.0, size=num_samples).round(2),
            "tcp_flags": np.random.choice(flags, size=num_samples, p=[0.6, 0.2, 0.1, 0.05, 0.05]),
            "serror_rate": np.random.uniform(0.0, 1.0, size=num_samples).round(2),
            "rerror_rate": np.random.uniform(0.0, 1.0, size=num_samples).round(2),
            "same_srv_rate": np.random.uniform(0.0, 1.0, size=num_samples).round(2),
            "label": np.random.choice(attack_types, size=num_samples, p=[0.5, 0.25, 0.15, 0.06, 0.04])
        }

        df = pd.DataFrame(data)

        # Introduce small missing & duplicate rows to test preprocessing pipeline resilience
        df.iloc[10:15, df.columns.get_loc("bytes_received")] = np.nan
        df = pd.concat([df, df.iloc[20:25]], ignore_index=True)

        target_path = os.path.join(Config.DATASET_RAW_DIR, filename)
        df.to_csv(target_path, index=False)
        logger.info(f"Synthetic sample dataset created at: {target_path} ({len(df)} rows, {len(df.columns)} cols)")

        return target_path
