from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from vehicle_bank.config import load_config
from vehicle_bank.data import SearchQuery, load_catalog, parse_rgb
from vehicle_bank.retrieval import VehicleMemoryBank

DEFAULT_CONFIG = os.environ.get("VEHICLE_BANK_CONFIG", "configs/demo_hybrid.yaml")
PROJECT_ROOT = Path(__file__).resolve().parents[2]

app = FastAPI(title="Vehicle Memory Bank Benchmark")


class SearchRequest(BaseModel):
    query_text: str = ""
    brand: str = ""
    model: str = ""
    body_type: str = ""
    color_name: str = ""
    rgb: str = Field(default="", description="Comma-separated RGB triplet, e.g. 20,80,200")
    top_k: int = 5


@lru_cache(maxsize=1)
def _get_bank() -> VehicleMemoryBank:
    config_path = PROJECT_ROOT / DEFAULT_CONFIG
    config = load_config(config_path)
    catalog = load_catalog(PROJECT_ROOT / config["data"]["catalog_path"], root_dir=PROJECT_ROOT)
    return VehicleMemoryBank(catalog=catalog, config=config)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/search")
def search(payload: SearchRequest) -> dict:
    bank = _get_bank()
    rgb = parse_rgb(payload.rgb)
    query = SearchQuery(
        query_text=payload.query_text,
        brand=payload.brand,
        model=payload.model,
        body_type=payload.body_type,
        color_name=payload.color_name,
        rgb=rgb,
    )
    results = bank.search(query=query, top_k=payload.top_k)
    return {
        "results": [
            {
                "asset_id": r.asset_id,
                "car_id": r.car_id,
                "brand": r.brand,
                "model": r.model,
                "body_type": r.body_type,
                "color_name": r.color_name,
                "score": r.score,
                "caption": r.caption,
                "image_path": str(Path(r.image_path).relative_to(PROJECT_ROOT)),
            }
            for r in results
        ]
    }
