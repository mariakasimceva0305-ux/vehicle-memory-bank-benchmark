from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from vehicle_bank.data import SearchQuery, image_feature


@dataclass
class SearchResult:
    asset_id: str
    car_id: str
    brand: str
    model: str
    body_type: str
    color_name: str
    score: float
    caption: str
    image_path: str


class VehicleMemoryBank:
    def __init__(self, catalog: pd.DataFrame, config: dict[str, Any]) -> None:
        self.catalog = catalog.reset_index(drop=True).copy()
        self.config = config
        self.vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
        self.text_matrix = self.vectorizer.fit_transform(self.catalog["caption"].tolist())
        self.image_matrix = None
        if config["retrieval"].get("use_image_features", True):
            self.image_matrix = np.vstack([image_feature(p) for p in self.catalog["image_path"].tolist()])

    def _text_scores(self, query_text: str) -> np.ndarray:
        if not query_text.strip():
            return np.zeros(len(self.catalog), dtype=np.float32)
        q = self.vectorizer.transform([query_text])
        scores = (self.text_matrix @ q.T).toarray().ravel()
        return scores.astype(np.float32)

    @staticmethod
    def _rgb_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
        av = np.array(a, dtype=np.float32)
        bv = np.array(b, dtype=np.float32)
        return float(np.linalg.norm(av - bv))

    def _metadata_scores(self, query: SearchQuery) -> np.ndarray:
        scores = np.zeros(len(self.catalog), dtype=np.float32)
        weights = self.config["retrieval"]["weights"]
        if query.brand:
            scores += np.where(self.catalog["brand"].str.lower() == query.brand.lower(), weights["brand"], 0.0)
        if query.model:
            scores += np.where(self.catalog["model"].str.lower() == query.model.lower(), weights["model"], 0.0)
        if query.body_type:
            scores += np.where(self.catalog["body_type"].str.lower() == query.body_type.lower(), weights["body_type"], 0.0)
        if query.color_name:
            scores += np.where(self.catalog["color_name"].str.lower() == query.color_name.lower(), weights["color_name"], 0.0)
        if query.rgb is not None:
            dists = self.catalog.apply(
                lambda r: self._rgb_distance(query.rgb, (int(r["r"]), int(r["g"]), int(r["b"]))),
                axis=1,
            ).values.astype(np.float32)
            scores += weights["rgb"] * (1.0 - np.clip(dists / 255.0, 0.0, 1.0))
        return scores

    def _image_scores(self, query_image_path: str | None) -> np.ndarray:
        if not query_image_path or self.image_matrix is None:
            return np.zeros(len(self.catalog), dtype=np.float32)
        q = image_feature(query_image_path)
        return (self.image_matrix @ q).astype(np.float32)

    def search(
        self,
        query: SearchQuery,
        top_k: int = 5,
        exclude_asset_id: str | None = None,
    ) -> list[SearchResult]:
        text_scores = self._text_scores(query.canonical_text())
        metadata_scores = self._metadata_scores(query)
        image_scores = self._image_scores(query.image_path)

        weights = self.config["retrieval"]["weights"]
        total = (
            weights["text"] * text_scores
            + metadata_scores
            + weights.get("image", 0.0) * image_scores
        )

        if exclude_asset_id is not None:
            mask = self.catalog["asset_id"] == exclude_asset_id
            total = np.where(mask, -1e9, total)

        order = np.argsort(-total)[:top_k]
        rows = self.catalog.iloc[order]
        return [
            SearchResult(
                asset_id=str(row["asset_id"]),
                car_id=str(row["car_id"]),
                brand=str(row["brand"]),
                model=str(row["model"]),
                body_type=str(row["body_type"]),
                color_name=str(row["color_name"]),
                score=float(total[idx]),
                caption=str(row["caption"]),
                image_path=str(row["image_path"]),
            )
            for idx, (_, row) in zip(order, rows.iterrows())
        ]
