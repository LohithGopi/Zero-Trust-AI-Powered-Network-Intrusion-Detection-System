import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class StratifiedNIDSSampler:
    """Class-aware reproducible stratified sampler for real NIDS datasets."""

    @staticmethod
    def detect_target_column(df):
        """Identify label/target column in tabular dataset."""
        possible = ["attack_cat", "Label", "label", "target", "Target", "class", "Class"]
        for col in possible:
            if col in df.columns:
                return col
        for col in df.columns:
            if col.strip().lower() in [p.lower() for p in possible]:
                return col
        # Fallback: check last string or categorical column
        return df.columns[-1]

    @classmethod
    def sample_dataset(cls, file_path: str, target_rows: int, random_seed: int = 42, dataset_type: str = "CIC-IDS2017"):
        """
        Perform reproducible stratified sampling on real raw CSV dataset.
        Guarantees zero synthetic rows.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Raw dataset file not found at: '{file_path}'")

        # Memory efficient loading
        df_raw = pd.read_csv(file_path, low_memory=False)
        total_raw_rows = len(df_raw)

        if target_rows > total_raw_rows:
            raise ValueError(
                f"Requested {target_rows:,} rows. Available valid rows: {total_raw_rows:,}. "
                f"Training cannot proceed because requested size exceeds available dataset."
            )

        target_col = cls.detect_target_column(df_raw)

        # Calculate class distribution before sampling
        class_counts_before = df_raw[target_col].astype(str).value_counts()
        class_dist_before = {
            cls_name: int(count) for cls_name, count in class_counts_before.items()
        }

        # If requesting full dataset
        if target_rows == total_raw_rows or target_rows <= 0:
            return df_raw, class_dist_before, class_dist_before, total_raw_rows, total_raw_rows, target_col

        # Stratified sampling
        sample_ratio = target_rows / total_raw_rows

        try:
            # Use train_test_split to get exact stratified subset
            _, df_sampled = train_test_split(
                df_raw,
                test_size=sample_ratio,
                random_state=random_seed,
                stratify=df_raw[target_col]
            )
        except Exception as strat_err:
            # Fallback if a class has < 2 samples for stratification
            df_sampled = df_raw.groupby(target_col, group_keys=False).apply(
                lambda x: x.sample(frac=sample_ratio, random_state=random_seed)
            )

        # Ensure exact requested row count if minor rounding difference occurs
        if len(df_sampled) > target_rows:
            df_sampled = df_sampled.sample(n=target_rows, random_state=random_seed)
        elif len(df_sampled) < target_rows:
            diff = target_rows - len(df_sampled)
            remaining_indices = df_raw.index.difference(df_sampled.index)
            extra_samples = df_raw.loc[remaining_indices].sample(n=min(diff, len(remaining_indices)), random_state=random_seed)
            df_sampled = pd.concat([df_sampled, extra_samples])

        # Calculate class distribution after sampling
        class_counts_after = df_sampled[target_col].astype(str).value_counts()
        class_dist_after = {
            cls_name: int(count) for cls_name, count in class_counts_after.items()
        }

        return df_sampled, class_dist_before, class_dist_after, total_raw_rows, len(df_sampled), target_col
