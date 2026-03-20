from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from vehicle_bank.config import load_config
from vehicle_bank.data import load_catalog
from vehicle_bank.evaluation import evaluate_memory_bank, save_results
from vehicle_bank.retrieval import VehicleMemoryBank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = load_config(ROOT / args.config)
    catalog = load_catalog(ROOT / config["data"]["catalog_path"], root_dir=ROOT)
    bank = VehicleMemoryBank(catalog=catalog, config=config)

    summary, rows = evaluate_memory_bank(
        catalog=catalog,
        memory_bank=bank,
        top_k=config["evaluation"]["top_k"],
    )
    save_results(summary, rows, ROOT / config["evaluation"]["output_dir"])
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
