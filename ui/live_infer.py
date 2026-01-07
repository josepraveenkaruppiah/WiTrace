import subprocess
import time
import re
from collections import deque, Counter

import numpy as np
import pandas as pd
import joblib


# -----------------------------
# WiTrace Live Inference Config
# -----------------------------
IFACE = "wlo1"

SAMPLE_INTERVAL = 0.2          # seconds between samples
WINDOW_SECONDS = 2.0           # feature window size
WINDOW_SIZE = int(WINDOW_SECONDS / SAMPLE_INTERVAL)

MODEL_PATH = "model/witrace_rf.joblib"

# Smoothing: majority vote over last N predictions
SMOOTH_HISTORY = 3             # smaller = faster reaction, larger = smoother


# -----------------------------
# Feature columns (MUST match training)
# -----------------------------
FEATURE_COLUMNS = ["mean", "variance", "range", "mean_abs_diff"]


# -----------------------------
# Helpers
# -----------------------------
signal_re = re.compile(r"signal:\s*(-?\d+)\s*dBm")


def get_signal() -> tuple[int | None, str]:
    """Return (RSSI_dBm or None, raw iw output)."""
    out = subprocess.getoutput(f"iw dev {IFACE} link")
    m = signal_re.search(out)
    if not m:
        return None, out
    return int(m.group(1)), out


def features_from_window(vals: deque) -> pd.DataFrame:
    """Compute features from window and return a 1-row DataFrame with named columns."""
    arr = np.array(list(vals), dtype=float)

    row = {
        "mean": float(np.mean(arr)),
        "variance": float(np.var(arr)),
        "range": float(np.max(arr) - np.min(arr)),
        "mean_abs_diff": float(np.mean(np.abs(np.diff(arr)))) if len(arr) > 1 else 0.0,
    }

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


def majority_vote(labels: deque) -> str:
    """Return most common label in deque."""
    return Counter(labels).most_common(1)[0][0]


def main() -> None:
    print("WiTrace Live Inference starting...", flush=True)
    print(f"Interface: {IFACE}", flush=True)
    print(f"Window: {WINDOW_SECONDS}s ({WINDOW_SIZE} samples) | Interval: {SAMPLE_INTERVAL}s", flush=True)
    print(f"Loading model: {MODEL_PATH}", flush=True)

    model = joblib.load(MODEL_PATH)

    print("Model loaded ✅", flush=True)
    print("-" * 60, flush=True)

    window = deque(maxlen=WINDOW_SIZE)
    history = deque(maxlen=SMOOTH_HISTORY)

    try:
        while True:
            sig, raw = get_signal()

            if sig is None:
                print("\n[WARN] Couldn't parse RSSI from iw output:\n" + raw + "\n", flush=True)
                time.sleep(1.0)
                continue

            window.append(sig)

            # While filling the initial window, print progress
            if len(window) < WINDOW_SIZE:
                print(f"Collecting window... {len(window)}/{WINDOW_SIZE} | RSSI={sig} dBm", flush=True)
                time.sleep(SAMPLE_INTERVAL)
                continue

            X = features_from_window(window)
            pred = model.predict(X)[0]
            history.append(pred)
            stable = majority_vote(history)

            window_var = float(np.var(np.array(list(window), dtype=float)))

            print(
                f"RSSI={sig:>4} dBm | pred={pred:<6} | stable={stable:<6} | var={window_var:.2f}",
                flush=True
            )

            time.sleep(SAMPLE_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped.", flush=True)


if __name__ == "__main__":
    main()
