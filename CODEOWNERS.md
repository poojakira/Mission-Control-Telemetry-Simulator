# 🛡️ Project Code Owners

This document defines the ownership and primary points of contact for various modules within CommandX.

## 🤖 Robotics Engineering
**Primary Owner**: [Rhutvik Pachghare](https://github.com/rhutvik)

Responsible for core orbital physics, GNC algorithms, and hardware integration.

| Resource | Responsibility |
| :--- | :--- |
| `mission_engine.py` | Orbital Physics (J2, Hohmann, Keplerian) |
| `gnc_kalman.py` | Guidance & Navigation (EKF) |
| `rl_pilot.py` | Actuator Control & PID Logic |
| `graphics_engine.py` | 3D Tactical Visuals |
| `model_3d.py` | Spacecraft Geometry Models |
| `subsystem_manager.py` | Hardware Abstraction Layer |
| `emergency_ops.py` | Safety & Fail-safe Protocols |

## 🧠 Machine Learning Engineering
**Primary Owner**: [Pooja Kiran](https://github.com/poojakira)

Responsible for intelligent optimization, data pipelines, and anomaly detection.

| Resource | Responsibility |
| :--- | :--- |
| `ga_optimizer.py` | Trajectory Planning via Genetic Algorithms |
| `streaming_ml_engine.py` | Asynchronous ML Inference Backend |
| `system_analytics.py` | Monte Carlo IV&V Simulation Suite |
| `data_processor.py` | TLE Parsing & Catalog Management |
| `run_anomaly_test.py` | Cyber Anomaly Detection Tests |
| `entropy_engine.py` | Information Entropy & State Analysis |

---

> [!NOTE]
> For general inquiries regarding the dashboard or deployment, please refer to the [README.md](file:///home/rhutvik/CommandX/README.md).
