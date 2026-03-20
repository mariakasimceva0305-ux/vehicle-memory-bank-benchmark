from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from vehicle_bank.config import load_config
from vehicle_bank.data import SearchQuery, load_catalog, parse_rgb
from vehicle_bank.retrieval import VehicleMemoryBank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--text", default="")
    parser.add_argument("--brand", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--body-type", default="")
    parser.add_argument("--color-name", default="")
    parser.add_argument("--rgb", default="")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    config = load_config(ROOT / args.config)
    catalog = load_catalog(ROOT / config["data"]["catalog_path"], root_dir=ROOT)
    bank = VehicleMemoryBank(catalog=catalog, config=config)

    query = SearchQuery(
        query_text=args.text,
        brand=args.brand,
        model=args.model,
        body_type=args.body_type,
        color_name=args.color_name,
        rgb=parse_rgb(args.rgb),
    )
    results = bank.search(query=query, top_k=args.top_k)
    for idx, r in enumerate(results, start=1):
        print(f"{idx}. {r.brand} {r.model} | {r.body_type} | {r.color_name} | score={r.score:.4f}")


if __name__ == "__main__":
    main()
