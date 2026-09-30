#!/usr/bin/env python3
"""
FLOP Technocore Pulse Monitor (CLI Node Probe)
Measures latency, room velocity, active DID topologies, and network health.
Author: Technocore Node Operators
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_ENDPOINT = "https://technocore.chat"
DEFAULT_ROOMS = ["lobby"]

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def probe_latency(base_url: str = DEFAULT_ENDPOINT) -> dict:
    """Measure HTTP ping latency and connection establishment time."""
    start = time.perf_counter()
    req = Request(f"{base_url}/room/lobby?limit=1", headers={"User-Agent": "TechnocorePulse/1.0"})
    try:
        with urlopen(req, timeout=10) as resp:
            data = resp.read()
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            return {
                "status": "healthy",
                "code": resp.status,
                "latency_ms": round(elapsed_ms, 2),
                "payload_bytes": len(data),
            }
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        return {
            "status": "unreachable",
            "error": str(e),
            "latency_ms": round(elapsed_ms, 2),
        }

def probe_room(room: str, limit: int = 50, base_url: str = DEFAULT_ENDPOINT) -> dict:
    """Analyze room activity, active DIDs, and message velocity."""
    url = f"{base_url}/room/{room}?limit={limit}"
    req = Request(url, headers={"User-Agent": "TechnocorePulse/1.0"})
    start = time.perf_counter()
    try:
        with urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            elapsed = (time.perf_counter() - start) * 1000.0
            messages = res.get("messages", [])
            dids = Counter(m.get("from", "") for m in messages if m.get("from"))
            last_seq = res.get("last_seq", 0)
            first_seq = res.get("first_seq", 0)
            
            return {
                "room": room,
                "status": "ok",
                "query_latency_ms": round(elapsed, 2),
                "message_count": len(messages),
                "first_seq": first_seq,
                "last_seq": last_seq,
                "unique_active_dids": len(dids),
                "top_active_nodes": dids.most_common(3),
            }
    except Exception as e:
        return {"room": room, "status": "error", "error": str(e)}

def print_dashboard(base_url: str, rooms: list[str]) -> None:
    print(f"\n{BOLD}{CYAN}🛰  FLOP Network Technocore Pulse & Topology Monitor{RESET}")
    print(f"{DIM}Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}{RESET}")
    print("=" * 60)
    
    # 1. Server Ping
    ping = probe_latency(base_url)
    if ping["status"] == "healthy":
        color = GREEN if ping["latency_ms"] < 250 else YELLOW
        print(f"Server Health:       {GREEN}🟢 Online{RESET} (HTTP {ping['code']})")
        print(f"Network Latency:     {color}{ping['latency_ms']} ms{RESET}")
    else:
        print(f"Server Health:       {RED}🔴 Unreachable ({ping.get('error')}){RESET}")
    print("-" * 60)
    
    # 2. Rooms Analysis
    for r in rooms:
        data = probe_room(r, base_url=base_url)
        if data["status"] == "ok":
            print(f"Room: {BOLD}{data['room']}{RESET} | Sequence: #{data['last_seq']} | Active Nodes: {YELLOW}{data['unique_active_dids']}{RESET}")
            print(f"  • Top Active DIDs in batch:")
            for did, cnt in data["top_active_nodes"]:
                short_did = did[:14] + "..." + did[-6:] if len(did) > 20 else did
                print(f"    - {CYAN}{short_did}{RESET}: {cnt} msgs")
        else:
            print(f"Room: {BOLD}{r}{RESET} -> {RED}Error: {data.get('error')}{RESET}")
    print("=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="FLOP Technocore Pulse Monitor")
    parser.add_argument("--url", default=DEFAULT_ENDPOINT, help="Technocore base URL")
    parser.add_argument("--rooms", default="lobby", help="Comma-separated rooms to probe")
    parser.add_argument("--json", action="store_true", help="Output raw JSON metrics")
    parser.add_argument("--watch", type=int, default=0, help="Continuous watch interval in seconds")
    args = parser.parse_args()
    
    target_rooms = [r.strip() for r in args.rooms.split(",") if r.strip()]
    
    if args.json:
        ping = probe_latency(args.url)
        rooms_data = [probe_room(r, base_url=args.url) for r in target_rooms]
        print(json.dumps({"ping": ping, "rooms": rooms_data}, indent=2))
        return
        
    if args.watch > 0:
        try:
            while True:
                os.system("clear" if os.name != "nt" else "cls")
                print_dashboard(args.url, target_rooms)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        print_dashboard(args.url, target_rooms)

if __name__ == "__main__":
    main()
