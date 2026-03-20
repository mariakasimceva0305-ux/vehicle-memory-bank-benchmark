from __future__ import annotations

from typing import Any

import pandas as pd


def load_mad_cars_subset(limit: int = 1000) -> pd.DataFrame:
    """
    Optional adapter for the public MAD-Cars dataset.
    Requires internet access and `datasets` installed in the environment.

    The public card exposes fields such as `car_id`, `view_id`, `url`, `color`, `brand`, and `model`.
    This helper keeps the project extensible without making online data a hard requirement for local demo runs.
    """
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("Install `datasets` to enable MAD-Cars loading.") from exc

    ds = load_dataset("yandex/mad-cars", split=f"train[:{limit}]")
    df = ds.to_pandas()
    return df
