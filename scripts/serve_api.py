from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))
os.environ.setdefault("VEHICLE_BANK_CONFIG", "configs/demo_hybrid.yaml")

if __name__ == "__main__":
    uvicorn.run("vehicle_bank.api:app", host="127.0.0.1", port=8000, reload=True)
