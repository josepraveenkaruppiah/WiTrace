import subprocess
import time
import re

iface = "wlo1"

signal_re = re.compile(r"signal: (-?\d+) dBm")
rx_re = re.compile(r"rx bitrate: ([0-9.]+) MBit/s")
tx_re = re.compile(r"tx bitrate: ([0-9.]+) MBit/s")

with open("data/raw/link_metrics.csv", "w") as f:
    f.write("timestamp,signal,rx_rate,tx_rate\n")

    while True:
        out = subprocess.getoutput(f"iw dev {iface} link")

        signal = signal_re.search(out)
        rx = rx_re.search(out)
        tx = tx_re.search(out)

        if signal and rx and tx:
            f.write(
                f"{time.time()},"
                f"{signal.group(1)},"
                f"{rx.group(1)},"
                f"{tx.group(1)}\n"
            )
            f.flush()

        time.sleep(0.2)
