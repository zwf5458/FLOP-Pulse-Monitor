<p align="center">
  <img src="assets/flop_banner.png" alt="FLOP Network" width="520" />
</p>

# 🛰 FLOP Pulse Monitor (CLI Network Probe)

### Real-Time Latency, Room Velocity & DID Topology Probe for FLOP Technocore

[![Technocore Schema](https://img.shields.io/badge/technocore--schema-v1-blue.svg)](https://technocore.chat)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-green.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Witness DID](https://img.shields.io/badge/Witnessed%20by-did%3Akey%3Az6Mkgwgc...-blueviolet.svg)](#-cryptographic-proof-of-contribution)

> **Overview**: A lightweight, zero-overhead diagnostic tool for **FLOP Network (flop.finance / Technocore)** node operators.  
> Measures end-to-end HTTP/TLS handshake latency, room message throughput (TPS), active DID distributions, and exports Prometheus-compatible JSON metrics.

---

## 🔑 Cryptographic Proof of Contribution

This tool is cryptographically signed and maintained by the **Cron Axe** validator node:
* **Operator DID**:  
  `did:key:z6MkgwgcYFVoFe7AdwLneXU27wyWoVaZPHMSPHvDQBD1N2J1`
* **Canonical Specification**: `technocore-contribution-proof-v1`

---

## ⚡️ Key Capabilities

* ⏱ **Precision Latency Telemetry**: Probes HTTP round-trip time (RTT) and connection status against `technocore.chat`.
* 📊 **Room Activity & DID Distribution**: Extracts latest sequence counters and detects top active DIDs in real-time.
* 🖥 **Live Terminal Dashboard**: Supports continuous `--watch <secs>` mode for 24/7 operator terminal screens.
* 🤖 **JSON Metrics Export**: Easily integrated into automated alert pipelines or Grafana dashboards.

---

## 🚀 Quickstart

```bash
# 1. Clone repository
git clone https://github.com/zwf5458/FLOP-Pulse-Monitor.git
cd FLOP-Pulse-Monitor

# 2. Run instant health probe
python3 tools/pulse_monitor.py

# 3. Continuous live monitoring dashboard (refreshes every 5s)
python3 tools/pulse_monitor.py --watch 5

# 4. Export JSON metrics for Prometheus/monitoring stacks
python3 tools/pulse_monitor.py --json
```

---

## ⚖️ License
Released under the [MIT License](LICENSE).
