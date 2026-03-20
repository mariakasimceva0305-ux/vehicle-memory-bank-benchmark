from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from vehicle_bank.data import load_catalog


def test_catalog_loads() -> None:
    df = load_catalog(ROOT / "data/demo_catalog/vehicles.csv", root_dir=ROOT)
    assert len(df) >= 30
    assert {"asset_id", "car_id", "brand", "model", "image_path"}.issubset(df.columns)
