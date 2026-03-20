from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

os.environ["VEHICLE_BANK_CONFIG"] = "configs/demo_hybrid.yaml"

from fastapi.testclient import TestClient
from vehicle_bank.api import app


def test_health() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_search() -> None:
    client = TestClient(app)
    resp = client.post(
        "/search",
        json={
            "query_text": "black bmw x5 suv",
            "brand": "BMW",
            "model": "X5",
            "body_type": "suv",
            "color_name": "black",
            "rgb": "35,35,35",
            "top_k": 3,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["results"]) == 3
