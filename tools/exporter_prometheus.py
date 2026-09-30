#!/usr/bin/env python3
"""
FLOP Technocore Prometheus Metrics Exporter
Exposes real-time room sequence, active node count, and round-trip latency on port 9110.
"""

from __future__ import annotations

import argparse
import http.server
import json
import time
from urllib.request import Request, urlopen

METRICS_PORT = 9110

def fetch_technocore_metrics(endpoint: str = "https://technocore.chat") -> str:
    start = time.perf_counter()
    req = Request(f"{endpoint}/room/lobby?limit=50", headers={"User-Agent": "TechnocoreExporter/1.0"})
    try:
        with urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed_sec = time.perf_counter() - start
            last_seq = data.get("last_seq", 0)
            messages = data.get("messages", [])
            unique_dids = len({m.get("from") for m in messages if m.get("from")})
            
            lines = [
                "# HELP technocore_probe_latency_seconds Round-trip latency to Technocore endpoint",
                "# TYPE technocore_probe_latency_seconds gauge",
                f"technocore_probe_latency_seconds {elapsed_sec:.4f}",
                "# HELP technocore_room_last_sequence Current head sequence number of room",
                "# TYPE technocore_room_last_sequence counter",
                f"technocore_room_last_sequence{{room=\"lobby\"}} {last_seq}",
                "# HELP technocore_room_active_dids Number of unique DIDs in recent sample window",
                "# TYPE technocore_room_active_dids gauge",
                f"technocore_room_active_dids{{room=\"lobby\"}} {unique_dids}",
            ]
            return "\n".join(lines) + "\n"
    except Exception as e:
        return f"# Error fetching Technocore metrics: {e}\n"

class MetricsHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            content = fetch_technocore_metrics().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

def main():
    parser = argparse.ArgumentParser(description="Technocore Prometheus Exporter")
    parser.add_argument("--port", type=int, default=METRICS_PORT, help="Listen port")
    args = parser.parse_args()
    
    server = http.server.HTTPServer(("0.0.0.0", args.port), MetricsHandler)
    print(f"🛰 Technocore Prometheus Exporter serving on : {args.port}/metrics")
    server.serve_forever()

if __name__ == "__main__":
    main()
