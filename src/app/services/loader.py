import os
import pandas as pd
from app.config import INPUT_DIR, DEBUG

def load_emails():
    all_files = [
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.endswith(".csv") and os.path.isfile(os.path.join(INPUT_DIR, f))
    ]

    if not all_files:
        raise FileNotFoundError(f"No CSV files found in {INPUT_DIR}")

    dataframes = []
    for file in all_files:
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            if "email" not in df.columns or "status" not in df.columns:
                raise ValueError(f"File {file} missing 'email' or 'status' column")
            df["__source_file"] = file
            dataframes.append(df)
            if DEBUG:
                print(f"[loader] Uploaded {len(df)} emails from {file}")
        except Exception as e:
            raise Exception(f"Processing error {file}: {e}")

    return pd.concat(dataframes, ignore_index=True)


def save_emails(df):
    if "__source_file" not in df.columns:
        raise ValueError("No information about the source file (__source_file).")

    for file, group in df.groupby("__source_file"):
        try:
            group = group.drop(columns=["__source_file"])
            group.to_csv(file, index=False)
            if DEBUG:
                print(f"[loader] Saved {len(group)} emails to {file}")
        except Exception as e:
            raise Exception(f"Error saving to {file}: {e}")
