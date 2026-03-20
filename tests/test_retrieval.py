from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from vehicle_bank.config import load_config
from vehicle_bank.data import SearchQuery, load_catalog
from vehicle_bank.retrieval import VehicleMemoryBank


def test_search_returns_matches() -> None:
    config = load_config(ROOT / "configs/demo_hybrid.yaml")
    catalog = load_catalog(ROOT / "data/demo_catalog/vehicles.csv", root_dir=ROOT)
    bank = VehicleMemoryBank(catalog, config)

    query = SearchQuery(
        query_text="blue toyota camry sedan daylight side view",
        brand="Toyota",
        model="Camry",
        body_type="sedan",
        color_name="blue",
        rgb=(36, 103, 214),
    )
    results = bank.search(query=query, top_k=3)
    assert results
    assert results[0].brand == "Toyota"
