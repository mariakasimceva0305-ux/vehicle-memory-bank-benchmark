from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from vehicle_bank.data import build_query_from_row
from vehicle_bank.retrieval import VehicleMemoryBank


def evaluate_memory_bank(
    catalog: pd.DataFrame,
    memory_bank: VehicleMemoryBank,
    top_k: int = 5,
) -> tuple[dict[str, float], list[dict[str, Any]]]:
    hits_at_1 = []
    hits_at_3 = []
    reciprocal_ranks = []
    brand_match = []
    color_match = []
    latency_ms = []
    rows = []

    for _, row in catalog.iterrows():
        query = build_query_from_row(row)
        t0 = time.perf_counter()
        preds = memory_bank.search(query=query, top_k=top_k, exclude_asset_id=str(row["asset_id"]))
        latency_ms.append((time.perf_counter() - t0) * 1000.0)

        relevant_car_id = str(row["car_id"])
        ranked_car_ids = [p.car_id for p in preds]
        rank = None
        for idx, car_id in enumerate(ranked_car_ids, start=1):
            if car_id == relevant_car_id:
                rank = idx
                break

        hits_at_1.append(1.0 if rank == 1 else 0.0)
        hits_at_3.append(1.0 if rank is not None and rank <= 3 else 0.0)
        reciprocal_ranks.append(1.0 / rank if rank is not None else 0.0)

        top1 = preds[0]
        brand_match.append(1.0 if top1.brand == row["brand"] else 0.0)
        color_match.append(1.0 if top1.color_name == row["color_name"] else 0.0)

        rows.append(
            {
                "query_asset_id": row["asset_id"],
                "query_car_id": row["car_id"],
                "query_caption": row["caption"],
                "rank_of_same_car": rank,
                "top1_asset_id": top1.asset_id,
                "top1_car_id": top1.car_id,
                "top1_caption": top1.caption,
                "top1_score": top1.score,
            }
        )

    summary = {
        "queries": float(len(catalog)),
        "recall_at_1": float(np.mean(hits_at_1)),
        "recall_at_3": float(np.mean(hits_at_3)),
        "mrr": float(np.mean(reciprocal_ranks)),
        "top1_brand_match": float(np.mean(brand_match)),
        "top1_color_match": float(np.mean(color_match)),
        "latency_ms_p50": float(np.percentile(latency_ms, 50)),
        "latency_ms_p95": float(np.percentile(latency_ms, 95)),
    }
    return summary, rows


def save_results(summary: dict[str, float], rows: list[dict[str, Any]], output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "latest_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with (output_dir / "latest_rows.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
