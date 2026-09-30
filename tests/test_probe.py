#!/usr/bin/env python3
"""
Unit tests for FLOP Pulse Monitor and Prometheus Exporter.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from tools.exporter_prometheus import fetch_technocore_metrics
from tools.pulse_monitor import probe_latency, probe_room


class TestPulseMonitor(unittest.TestCase):

    @patch("tools.pulse_monitor.urlopen")
    def test_probe_latency_healthy(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b'{"status":"ok"}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        result = probe_latency("https://fake.technocore.chat")
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["code"], 200)
        self.assertIn("latency_ms", result)
        self.assertGreaterEqual(result["latency_ms"], 0.0)

    @patch("tools.pulse_monitor.urlopen")
    def test_probe_latency_unreachable(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection timeout")

        result = probe_latency("https://fake.technocore.chat")
        self.assertEqual(result["status"], "unreachable")
        self.assertIn("Connection timeout", result["error"])

    @patch("tools.pulse_monitor.urlopen")
    def test_probe_room_metrics(self, mock_urlopen):
        fake_payload = {
            "first_seq": 100,
            "last_seq": 105,
            "messages": [
                {"from": "did:key:nodeA", "seq": 101},
                {"from": "did:key:nodeB", "seq": 102},
                {"from": "did:key:nodeA", "seq": 103},
            ]
        }
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(fake_payload).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        data = probe_room("lobby", limit=10, base_url="https://fake.technocore.chat")
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["room"], "lobby")
        self.assertEqual(data["last_seq"], 105)
        self.assertEqual(data["unique_active_dids"], 2)
        self.assertEqual(data["top_active_nodes"][0], ("did:key:nodeA", 2))

    @patch("tools.exporter_prometheus.urlopen")
    def test_prometheus_metrics_export(self, mock_urlopen):
        fake_payload = {
            "last_seq": 200,
            "messages": [
                {"from": "did:key:node1"},
                {"from": "did:key:node2"}
            ]
        }
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(fake_payload).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        metrics = fetch_technocore_metrics("https://fake.technocore.chat")
        self.assertIn("technocore_probe_latency_seconds", metrics)
        self.assertIn('technocore_room_last_sequence{room="lobby"} 200', metrics)
        self.assertIn('technocore_room_active_dids{room="lobby"} 2', metrics)


if __name__ == "__main__":
    unittest.main()
