
---

## 📊 Signal Features (MVP Level)

The MVP focuses on **simple, explainable features**, such as:
- Mean and variance of signal amplitude
- Temporal variance across subcarriers
- Short-time signal energy
- Rate of change over time (Δ features)
- Optional PCA-reduced feature vectors

No complex RF modelling is required at this stage.

---

## 🤖 Inference Model

Recommended classifiers for the MVP:
- **Random Forest**
- **Support Vector Machine (SVM)**

These provide:
- Fast training
- Explainability
- Robust performance with small datasets

Deep learning models are intentionally avoided in v0.1.

---

## 🖥️ User Interface (MVP)

The UI is minimal and functional:
- **Presence Status**: `EMPTY` / `PRESENT`
- **Motion State**: `STILL` / `MOVING` / `WALKING`
- Live signal activity graph (time series)

The UI updates every **200–500 ms**.

---

## 📈 Evaluation Criteria

The MVP is considered successful if it achieves:
- **≥ 85% accuracy** for presence detection
- Reasonable separation between motion classes
- Stable real-time inference without manual recalibration

Evaluation includes:
- Empty room baseline
- Same person, multiple sessions
- Different movement speeds

---

## ⏱️ Development Timeline (Estimated)

| Day | Task |
|----:|------|
| 1–2 | Signal capture & visualisation |
| 3–4 | Feature extraction & dataset creation |
| 5   | Model training & validation |
| 6   | Real-time inference loop |
| 7   | UI, documentation & demo |

---

## 📦 Deliverables

By the end of v0.1, WiTrace provides:
- A working **device-free presence detector**
- Real-time motion classification
- A live demo reacting to human movement
- A strong foundation for localisation in later versions

---

## 🔜 Planned Extensions

- **v0.3** — Zone-based localisation (grid classification)
- **v0.5** — Single-person path tracing
- **v1.0** — Robust room-scale localisation

---

## ⚠️ Ethical Note

WiTrace is designed for **research and experimental purposes only**.  
It does not identify individuals and does not collect personal data.

---

## 📄 Licence
To be defined.

---

**WiTrace v0.1 — Tracing human presence through Wi-Fi signals**
