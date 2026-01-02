import pandas as pd
import numpy as np

WINDOW_SECONDS = 2.0
SAMPLING_INTERVAL = 0.2  # from logger
WINDOW_SIZE = int(WINDOW_SECONDS / SAMPLING_INTERVAL)

df = pd.read_csv("data/raw/link_metrics.csv")

signals = df["signal"].values
timestamps = df["timestamp"].values

features = []

for i in range(0, len(signals) - WINDOW_SIZE, WINDOW_SIZE):
    window = signals[i:i + WINDOW_SIZE]

    feat = {
        "start_time": timestamps[i],
        "mean": np.mean(window),
        "variance": np.var(window),
        "range": np.max(window) - np.min(window),
        "mean_abs_diff": np.mean(np.abs(np.diff(window)))
    }

    features.append(feat)

features_df = pd.DataFrame(features)
features_df.to_csv("data/processed/features.csv", index=False)

print(f"Extracted {len(features_df)} windows")


