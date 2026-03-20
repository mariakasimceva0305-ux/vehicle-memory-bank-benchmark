from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from PIL import Image


@dataclass
class SearchQuery:
    query_text: str = ""
    brand: str = ""
    model: str = ""
    body_type: str = ""
    color_name: str = ""
    rgb: tuple[int, int, int] | None = None
    image_path: str | None = None

    def canonical_text(self) -> str:
        parts = [
            self.query_text.strip(),
            self.brand.strip(),
            self.model.strip(),
            self.body_type.strip(),
            self.color_name.strip(),
        ]
        return " ".join([p for p in parts if p]).strip()


def load_catalog(csv_path: str | Path, root_dir: str | Path | None = None) -> pd.DataFrame:
    root_dir = Path(root_dir) if root_dir else Path(csv_path).parent
    df = pd.read_csv(csv_path)
    for col in ["brand", "model", "body_type", "color_name", "caption", "view_label", "lighting"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)
    if "image_path" in df.columns:
        df["image_path"] = df["image_path"].map(lambda x: str((root_dir / x).resolve()))
    return df


def image_feature(path: str | Path) -> np.ndarray:
    img = Image.open(path).convert("RGB").resize((128, 72))
    arr = np.asarray(img).astype(np.float32) / 255.0
    # Focus more on mid-lower region where the car body is drawn in demo assets.
    crop = arr[18:66, 12:116]
    hsv_like = np.stack(
        [
            crop[..., 0],
            crop[..., 1],
            crop[..., 2],
        ],
        axis=-1,
    )
    hist, _ = np.histogramdd(
        hsv_like.reshape(-1, 3),
        bins=(6, 6, 6),
        range=((0.0, 1.0), (0.0, 1.0), (0.0, 1.0)),
    )
    vec = hist.flatten()
    denom = np.linalg.norm(vec) + 1e-8
    return vec / denom


def build_query_from_row(row: pd.Series) -> SearchQuery:
    rgb = (int(row["r"]), int(row["g"]), int(row["b"]))
    return SearchQuery(
        query_text=str(row["caption"]),
        brand=str(row["brand"]),
        model=str(row["model"]),
        body_type=str(row["body_type"]),
        color_name=str(row["color_name"]),
        rgb=rgb,
        image_path=str(row["image_path"]),
    )


def parse_rgb(value: str | None) -> Optional[tuple[int, int, int]]:
    if not value:
        return None
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 3:
        return None
    try:
        nums = tuple(int(p) for p in parts)
    except ValueError:
        return None
    if any(n < 0 or n > 255 for n in nums):
        return None
    return nums
