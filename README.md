<p align="center">
  <img src="assets/flop_banner.png" alt="FLOP Network" width="520" />
</p>

# 🛰 FLOP Pulse Monitor (CLI Network Probe & Prometheus Exporter)

### Real-Time Latency, Room Velocity & DID Topology Probe for FLOP Technocore

[![Technocore Schema](https://img.shields.io/badge/technocore--schema-v1-blue.svg)](https://technocore.chat)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-green.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Witness DID](https://img.shields.io/badge/Witnessed%20by-did%3Akey%3Az6Mkgwgc...-blueviolet.svg)](#-cryptographic-proof-of-contribution)

> **Overview**: A lightweight, zero-overhead diagnostic tool and metrics exporter for **FLOP Network (flop.finance / Technocore)** node operators.  
> Measures end-to-end HTTP/TLS handshake latency, room message throughput (TPS), active DID distributions, and exports Prometheus-compatible metrics on port 9110.

---

## 🔑 Cryptographic Proof of Contribution

This tool is cryptographically signed and maintained by the **Cron Axe** validator node:
* **Operator DID**:  
  `did:key:z6MkgwgcYFVoFe7AdwLneXU27wyWoVaZPHMSPHvDQBD1N2J1`
* **Canonical Specification**: `technocore-contribution-proof-v1`
* **Witness File**: [`contribution-proof.json`](contribution-proof.json)

---

## ⚡️ Architecture & Key Capabilities

```text
┌────────────────────────┐      HTTP Probe       ┌────────────────────────┐
│  tools/pulse_monitor   │ ───────────────────>  │ https://technocore.chat│
│  (CLI Watch / JSON)    │                       │ (/room/lobby?limit=50) │
└────────────────────────┘                       └───────────┬────────────┘
                                                             │
┌────────────────────────┐      Scrape Metrics               │
│ tools/exporter_        │ <─────────────────────────────────┘
│ prometheus.py (:9110)  │ ────> [ Prometheus / Grafana Dashboard ]
└────────────────────────┘
```

* ⏱ **Precision Latency Telemetry**: Probes HTTP round-trip time (RTT) and connection status against `technocore.chat`.
* 📊 **Room Activity & DID Distribution**: Extracts latest sequence counters and detects top active DIDs in real-time.
* 🖥 **Live Terminal Dashboard**: Supports continuous `--watch <secs>` mode for 24/7 operator terminal screens.
* 📈 **Prometheus Exporter**: Built-in HTTP server (`:9110/metrics`) exposing standard Prometheus exposition format.
* 🧪 **Comprehensive Test Suite**: Isolated offline unit tests covering network probes and metrics formatting.

---

## 📁 Repository Structure

```text
FLOP-Pulse-Monitor/
├── config/
│   └── monitor.example.json      # Production monitoring & exporter configuration
├── tools/
│   ├── pulse_monitor.py          # Interactive CLI diagnostics & watch probe
│   └── exporter_prometheus.py    # Standalone Prometheus HTTP metrics server (:9110)
├── tests/
│   └── test_probe.py             # Unit tests for network probing and calculations
├── assets/
│   └── flop_banner.png           # Official visual branding
├── contribution-proof.json       # Cryptographic Ed25519 signature proof
├── SECURITY.md                   # Safe probing & exporter isolation policy
├── LICENSE                       # MIT License
└── README.md
```

---

## 🚀 Quickstart

### 1. Interactive CLI Probe
```bash
# Instant one-shot check
python3 tools/pulse_monitor.py

# Continuous live monitoring dashboard (refreshes every 5s)
python3 tools/pulse_monitor.py --watch 5

# Export raw JSON snapshot for shell scripts
python3 tools/pulse_monitor.py --json
```

### 2. Prometheus Exporter
```bash
# Launch metrics exporter on port 9110
python3 tools/exporter_prometheus.py --port 9110

# Test metrics endpoint
curl -s http://127.0.0.1:9110/metrics
```

### 3. Run Unit Tests
```bash
python3 -m unittest discover -s tests
```

---

## ⚖️ License
Released under the [MIT License](LICENSE).
