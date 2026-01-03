import pandas as pd
import numpy as np
from pathlib import Path

WINDOW_SECONDS = 2.0
SAMPLING_INTERVAL = 0.2  # matches logger
WINDOW_SIZE = int(WINDOW_SECONDS / SAMPLING_INTERVAL)

def extract_features(csv_path, label):
    df = pd.read_csv(csv_path)
    signals = df["signal"].values

    rows = []
    for i in range(0, len(signals) - WINDOW_SIZE, WINDOW_SIZE):
        window = signals[i:i + WINDOW_SIZE]
        rows.append({
            "mean": np.mean(window),
            "variance": np.var(window),
            "range": np.max(window) - np.min(window),
            "mean_abs_diff": np.mean(np.abs(np.diff(window))),
            "label": label
        })
    return rows

dataset = []

for label in ["still", "moving", "empty"]:
    for csv in Path(f"data/sessions/{label}").glob("*.csv"):
        dataset.extend(extract_features(csv, label))

out = Path("data/processed")
out.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(dataset)
df.to_csv(out / "dataset.csv", index=False)

print(f"Dataset built with {len(df)} samples")
print(df["label"].value_counts())
