# Security Policy

## 🔒 Security & Safe Probing Guidelines for FLOP Pulse Monitor

The **FLOP-Pulse-Monitor** is a specialized telemetry and diagnostics toolkit for the decentralized Arthur Hayes FLOP Network and Technocore communication protocol. Because monitoring probes generate recurring network traffic and expose metric endpoints, operators must adhere to these operational security guidelines.

---

### 1. Prometheus Metrics Endpoint Exposure (`:9110/metrics`)

* **Default Loopback Binding**: `exporter_prometheus.py` should be bound to `127.0.0.1` unless protected behind an authenticating reverse proxy (such as Nginx with HTTP Basic Auth, mTLS, or a Tailscale / WireGuard overlay network).
* **Information Disclosure Prevention**: The exporter returns aggregated sequence numbers and anonymized node DID counts. It strictly refuses to log or export plaintext payload bodies, cryptographic nonces, or private credentials.

---

### 2. Probing Hygiene & Anti-DDoS Compliance

* **Rate Limiting**: Automated polling against public Technocore endpoints (`https://technocore.chat`) must adhere to reasonable sampling intervals (recommended: >= 15 seconds).
* **Respect Upstream 429**: When receiving HTTP 429 (Too Many Requests), probes must implement exponential backoff with jitter to protect public gateway capacity.
* **No Secret Storage**: This project requires no private keys or signing passphrases to run. If an operator is prompted for private keys, terminate the process immediately.

---

### 3. Supported Versions

| Version | Supported          | Security Status |
| :---    | :---               | :---            |
| 1.1.x   | :white_check_mark: | Active Security Maintenance |
| 1.0.x   | :white_check_mark: | Maintenance Only |
| < 1.0   | :x:                | Deprecated |

---

### 4. Vulnerability Reporting

If you identify a security issue, metric leak, or denial-of-service vector within this repository:

* **Primary Maintainer DID (Tab 1 Cron Axe)**:  
  `did:key:z6MkgwgcYFVoFe7AdwLneXU27wyWoVaZPHMSPHvDQBD1N2J1`
* **Maintainer Namespace**: `zwf5458/FLOP-Pulse-Monitor`
* **Disclosure Process**: Please do not open public GitHub issues for critical vulnerabilities. Send cryptographic message or reach out via Technocore node operator channels. We commit to reviewing disclosures within 48 hours.
