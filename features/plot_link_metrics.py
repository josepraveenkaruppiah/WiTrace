import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/link_metrics.csv")

plt.figure(figsize=(10, 4))
plt.plot(df["timestamp"], df["signal"], label="RSSI (dBm)")
plt.xlabel("Time")
plt.ylabel("Signal Strength")
plt.title("WiTrace – Wi-Fi Signal Disturbance Over Time")
plt.legend()
plt.tight_layout()

plt.savefig("data/processed/rssi_plot.png")
print("Plot saved to data/processed/rssi_plot.png")

