import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from config import Config
from utils.logger import logger

class BaseNIDSPreprocessor:
    """Base dataset preprocessor with strict data-leakage prevention."""

    def __init__(self, artifact_dir=None):
        self.artifact_dir = artifact_dir or Config.MODEL_DIR
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_encoders = {}
        self.feature_names = []

    def clean_inf_and_nulls(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int, int, int]:
        """Detect and handle infinite values, missing values, and duplicates."""
        orig_rows = len(df)

        # 1. Replace inf and -inf with NaN
        inf_count = int(np.isinf(df.select_dtypes(include=[np.number])).sum().sum())
        df = df.replace([np.inf, -np.inf], np.nan)

        # 2. Duplicate detection & removal BEFORE split
        df = df.drop_duplicates().reset_index(drop=True)
        clean_rows = len(df)
        dup_count = orig_rows - clean_rows

        # 3. Missing values count & imputation
        missing_count = int(df.isnull().sum().sum())
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype == object or df[col].dtype.name == 'category':
                    mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                    df[col] = df[col].fillna(mode_val)
                else:
                    median_val = df[col].median() if not pd.isna(df[col].median()) else 0.0
                    df[col] = df[col].fillna(median_val)

        return df, dup_count, missing_count, inf_count

    def process(self, df: pd.DataFrame, target_col: str = None) -> tuple[dict, tuple]:
        raise NotImplementedError("Subclasses must implement process()")


class CICIDS2017Preprocessor(BaseNIDSPreprocessor):
    """Dataset-specific preprocessing for CIC-IDS2017 benchmark dataset."""

    def process(self, df: pd.DataFrame, target_col: str = None, random_seed: int = 42) -> tuple[dict, tuple]:
        # Strip column whitespace
        df.columns = df.columns.str.strip()

        # Target column identification
        if not target_col:
            for c in ["Label", "label", "target", "Class"]:
                if c in df.columns:
                    target_col = c
                    break
        if not target_col:
            target_col = df.columns[-1]

        # Clean inf, nulls, duplicates
        df, dup_count, missing_count, inf_count = self.clean_inf_and_nulls(df)

        # Drop non-predictive IP metadata columns if present
        drop_cols = ["Flow ID", "Source IP", "Source Port", "Destination IP", "Timestamp"]
        df = df.drop(columns=[c for c in drop_cols if c in df.columns])

        # Target Label Encoding
        y_raw = df[target_col].astype(str).values
        y_encoded = self.label_encoder.fit_transform(y_raw)

        X_df = df.drop(columns=[target_col])
        self.feature_names = X_df.columns.tolist()

        # Categorical Column Encoding
        cat_cols = X_df.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in cat_cols:
            fe = LabelEncoder()
            X_df[col] = fe.fit_transform(X_df[col].astype(str))
            self.feature_encoders[col] = fe

        X_df = X_df.apply(pd.to_numeric, errors='coerce').fillna(0.0)

        # Train / Validation / Test Split BEFORE scaling to prevent leakage
        X_train_raw, X_temp, y_train, y_temp = train_test_split(
            X_df.values, y_encoded, test_size=0.30, random_state=random_seed, stratify=y_encoded if len(np.unique(y_encoded)) > 1 else None
        )
        X_val_raw, X_test_raw, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.50, random_state=random_seed, stratify=y_temp if len(np.unique(y_temp)) > 1 else None
        )

        # Fit StandardScaler ONLY on X_train
        X_train = self.scaler.fit_transform(X_train_raw)
        X_val = self.scaler.transform(X_val_raw)
        X_test = self.scaler.transform(X_test_raw)

        summary = {
            "dataset_type": "CIC-IDS2017",
            "duplicate_rows_removed": dup_count,
            "missing_values_handled": missing_count,
            "infinite_values_handled": inf_count,
            "training_rows": len(X_train),
            "validation_rows": len(X_val),
            "testing_rows": len(X_test),
            "total_features": X_df.shape[1],
            "feature_names": self.feature_names,
            "num_classes": len(self.label_encoder.classes_),
            "classes": self.label_encoder.classes_.tolist(),
            "target_col": target_col,
            "scaled_min": float(np.min(X_train)),
            "scaled_max": float(np.max(X_train)),
            "scaled_mean": float(np.mean(X_train)),
            "scaled_std": float(np.std(X_train))
        }

        return summary, (X_train, y_train, X_val, y_val, X_test, y_test)


class UNSWNB15Preprocessor(BaseNIDSPreprocessor):
    """Dataset-specific preprocessing for UNSW-NB15 benchmark dataset."""

    def process(self, df: pd.DataFrame, target_col: str = None, random_seed: int = 42) -> tuple[dict, tuple]:
        df.columns = df.columns.str.strip()

        if "attack_cat" in df.columns:
            target_col = "attack_cat"
        elif not target_col:
            for c in ["attack_cat", "label", "Label", "target"]:
                if c in df.columns:
                    target_col = c
                    break
        if not target_col:
            target_col = df.columns[-1]

        # Clean inf, nulls, duplicates
        df, dup_count, missing_count, inf_count = self.clean_inf_and_nulls(df)

        # Drop id column if present
        if "id" in df.columns:
            df = df.drop(columns=["id"])

        y_raw = df[target_col].astype(str).values
        y_encoded = self.label_encoder.fit_transform(y_raw)

        X_df = df.drop(columns=[target_col])
        # Eliminate target leakage: drop all label and attack category annotations from input features
        leakage_cols = ["attack_cat", "label", "Label", "target", "Target", "id", "ID"]
        drop_from_X = [c for c in leakage_cols if c in X_df.columns]
        if drop_from_X:
            X_df = X_df.drop(columns=drop_from_X)

        self.feature_names = X_df.columns.tolist()

        cat_cols = X_df.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in cat_cols:
            fe = LabelEncoder()
            X_df[col] = fe.fit_transform(X_df[col].astype(str))
            self.feature_encoders[col] = fe

        X_df = X_df.apply(pd.to_numeric, errors='coerce').fillna(0.0)

        X_train_raw, X_temp, y_train, y_temp = train_test_split(
            X_df.values, y_encoded, test_size=0.30, random_state=random_seed, stratify=y_encoded if len(np.unique(y_encoded)) > 1 else None
        )
        X_val_raw, X_test_raw, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.50, random_state=random_seed, stratify=y_temp if len(np.unique(y_temp)) > 1 else None
        )

        X_train = self.scaler.fit_transform(X_train_raw)
        X_val = self.scaler.transform(X_val_raw)
        X_test = self.scaler.transform(X_test_raw)

        summary = {
            "dataset_type": "UNSW-NB15",
            "duplicate_rows_removed": dup_count,
            "missing_values_handled": missing_count,
            "infinite_values_handled": inf_count,
            "training_rows": len(X_train),
            "validation_rows": len(X_val),
            "testing_rows": len(X_test),
            "total_features": X_df.shape[1],
            "feature_names": self.feature_names,
            "num_classes": len(self.label_encoder.classes_),
            "classes": self.label_encoder.classes_.tolist(),
            "target_col": target_col,
            "scaled_min": float(np.min(X_train)),
            "scaled_max": float(np.max(X_train)),
            "scaled_mean": float(np.mean(X_train)),
            "scaled_std": float(np.std(X_train))
        }

        return summary, (X_train, y_train, X_val, y_val, X_test, y_test)


class NSLKDDPreprocessor(BaseNIDSPreprocessor):
    """Dataset-specific preprocessing for NSL-KDD benchmark dataset."""

    def process(self, df: pd.DataFrame, target_col: str = None, random_seed: int = 42) -> tuple[dict, tuple]:
        df.columns = df.columns.str.strip()

        if not target_col:
            for c in ["label", "Label", "target", "class"]:
                if c in df.columns:
                    target_col = c
                    break
        if not target_col:
            target_col = df.columns[-1]

        df, dup_count, missing_count, inf_count = self.clean_inf_and_nulls(df)

        y_raw = df[target_col].astype(str).values
        y_encoded = self.label_encoder.fit_transform(y_raw)

        X_df = df.drop(columns=[target_col])
        leakage_cols = ["label", "Label", "target", "class", "difficulty_level", "difficulty"]
        drop_from_X = [c for c in leakage_cols if c in X_df.columns]
        if drop_from_X:
            X_df = X_df.drop(columns=drop_from_X)
        self.feature_names = X_df.columns.tolist()

        cat_cols = X_df.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in cat_cols:
            fe = LabelEncoder()
            X_df[col] = fe.fit_transform(X_df[col].astype(str))
            self.feature_encoders[col] = fe

        X_df = X_df.apply(pd.to_numeric, errors='coerce').fillna(0.0)

        X_train_raw, X_temp, y_train, y_temp = train_test_split(
            X_df.values, y_encoded, test_size=0.30, random_state=random_seed, stratify=y_encoded if len(np.unique(y_encoded)) > 1 else None
        )
        X_val_raw, X_test_raw, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.50, random_state=random_seed, stratify=y_temp if len(np.unique(y_temp)) > 1 else None
        )

        X_train = self.scaler.fit_transform(X_train_raw)
        X_val = self.scaler.transform(X_val_raw)
        X_test = self.scaler.transform(X_test_raw)

        summary = {
            "dataset_type": "NSL-KDD",
            "duplicate_rows_removed": dup_count,
            "missing_values_handled": missing_count,
            "infinite_values_handled": inf_count,
            "training_rows": len(X_train),
            "validation_rows": len(X_val),
            "testing_rows": len(X_test),
            "total_features": X_df.shape[1],
            "feature_names": self.feature_names,
            "num_classes": len(self.label_encoder.classes_),
            "classes": self.label_encoder.classes_.tolist(),
            "target_col": target_col,
            "scaled_min": float(np.min(X_train)),
            "scaled_max": float(np.max(X_train)),
            "scaled_mean": float(np.mean(X_train)),
            "scaled_std": float(np.std(X_train))
        }

        return summary, (X_train, y_train, X_val, y_val, X_test, y_test)


class DataPreprocessor:
    """Preprocessor Factory providing dataset-specific preprocessing pipelines."""

    @staticmethod
    def get_preprocessor(dataset_type: str, artifact_dir: str = None) -> BaseNIDSPreprocessor:
        dt = (dataset_type or "").upper()
        if "CIC" in dt:
            return CICIDS2017Preprocessor(artifact_dir=artifact_dir)
        elif "UNSW" in dt:
            return UNSWNB15Preprocessor(artifact_dir=artifact_dir)
        else:
            return NSLKDDPreprocessor(artifact_dir=artifact_dir)

    def process(self, df: pd.DataFrame) -> tuple[dict, tuple]:
        """Legacy compatibility wrapper."""
        prep = NSLKDDPreprocessor()
        summary, (X_train, y_train, X_val, y_val, X_test, y_test) = prep.process(df)
        legacy_tuple = (X_train, X_test, y_train, y_test)
        return summary, legacy_tuple
