"""Minimal Wayback Machine snapshots API call — one typed row per snapshot.

Docs & schema: https://quanticdata.io/collectors/wayback-machine-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/wayback_machine/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "target": "https://example.com",
        "max_results": 50
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("timestamp"), row.get("captured_at"), row.get("original_url"))
print(f"{len(data['results'])} snapshots, cost ${data['cost']}")
