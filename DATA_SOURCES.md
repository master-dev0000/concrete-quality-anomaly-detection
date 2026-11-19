# 📊 Data Sources & Engineering Benchmarks: Concrete Quality & Anomaly Detection

This repository contains machine learning pipelines for predicting compressive strength ($f_{ck}$) of high-performance concrete from early mix proportions and detecting structural integrity anomalies from sensor telemetry. Raw sensor streams and lab datasets are maintained according to international scientific standards.

---

## 1. UCI Concrete Compressive Strength Benchmark (Prof. I-Cheng Yeh)
* **Authoritative Source:** UC Irvine Machine Learning Repository
* **Direct Access Portal:** [UCI Concrete Compressive Strength Dataset](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength)
* **Academic Reference:** Yeh, I-C. (1998). *"Modeling of strength of high-performance concrete using artificial neural networks."* Cement and Concrete Research, 28(12), 1797-1808.
* **Volume:** 1,030 rigorously tested concrete cylinder formulations.
* **Format:** CSV / OpenML Dataset ID `4353`
* **Licensing:** Creative Commons Attribution 4.0 International (CC BY 4.0).

### Physical Features & Chemical Proportioning
| Feature Name | Type | Physical Unit | Engineering Role in Concrete Technology |
| :--- | :--- | :--- | :--- |
| `cement` | Continuous | $kg/m^3$ | Primary hydraulic binder (alite/belite phases) |
| `blast_furnace_slag` | Continuous | $kg/m^3$ | Supplementary cementitious material (latent hydraulic) |
| `fly_ash` | Continuous | $kg/m^3$ | Pozzolanic micro-filler, reduces heat of hydration |
| `water` | Continuous | $kg/m^3$ | Governs water-to-binder ratio ($w/b$), porosimetry |
| `superplasticizer` | Continuous | $kg/m^3$ | High-range water reducer (steric hindrance dispersion) |
| `coarse_aggregate` | Continuous | $kg/m^3$ | Coarse gravel skeleton ($> 4.75\text{ mm}$) |
| `fine_aggregate` | Continuous | $kg/m^3$ | Fine sand matrix ($< 4.75\text{ mm}$) |
| `age` | Integer | Days ($1 - 365$) | Curing duration prior to axial compression break |
| `compressive_strength` | Continuous | Megapascals ($MPa$) | **Target:** Cylinder compressive strength ($f_{ck}$) |

---

## 2. EMPA / SIMA Z24 Bridge Structural Health Monitoring (SHM) Telemetry
* **Authoritative Source:** EMPA (Swiss Federal Laboratories for Materials Science and Technology) & Katholieke Universiteit Leuven
* **Direct Access Portal:** [LANL Damage Prognosis & Benchmark Problems](https://www.lanl.gov/projects/damage-prognosis/benchmark-problems/) & EMPA Research Archives
* **Academic Reference:** Maeck, J., & De Roeck, G. (2003). *"Damage detection on the Z24 bridge."* Mechanical Systems and Signal Processing, 17(1), 133-142.
* **Domain Focus:** Continuous multi-sensor structural health monitoring under operating ambient conditions and progressive structural failure.
* **Licensing:** Open Academic Research Benchmark.

### Sensor Channels & Measurement Parameters
| Channel Group | Sensor Technology | Physical Unit | Signal Processing & Anomaly Application |
| :--- | :--- | :--- | :--- |
| `accel_ch01` to `accel_ch16` | Triaxial capacitive accelerometers | $g$ ($m/s^2$) | Operational Modal Analysis (OMA), natural frequencies |
| `strain_sg01` to `strain_sg08` | Vibrating wire strain gauges | Microstrain ($\mu\epsilon$) | Static/quasi-static deformation and tendon tension |
| `temp_deck_top` / `temp_deck_bot` | Pt100 RTD temperature probes | $^{\circ}\text{C}$ | Thermal gradient compensation (filters seasonal drift) |
| `damage_state` | Binary Ground Truth | $[0, 1]$ | $0 = $ Healthy bridge baseline; $1 = $ Progressive pier settlement/crack |

---

## Synthetic Data Generator & Pipeline Ingestion
```python
import numpy as np
import pandas as pd

def generate_sensor_stream_sample(n_points: int = 1000, anomaly_fraction: float = 0.05) -> pd.DataFrame:
    """Generates synthetic structural strain telemetry with thermal sinusoidal cycles and injected anomalies."""
    np.random.seed(42)
    time = np.linspace(0, 100, n_points)
    # Baseline thermal expansion + dynamic live load noise
    strain = 250 + 40 * np.sin(2 * np.pi * time / 24) + np.random.normal(0, 5, n_points)
    is_anomaly = np.zeros(n_points, dtype=int)
    
    # Inject localized structural anomalies (tendon slip / settling)
    anomaly_indices = np.random.choice(n_points, size=int(n_points * anomaly_fraction), replace=False)
    strain[anomaly_indices] += np.random.choice([-65, 85], size=len(anomaly_indices))
    is_anomaly[anomaly_indices] = 1
    
    return pd.DataFrame({"timestamp": time, "strain_microstrain": strain, "anomaly": is_anomaly})
```
