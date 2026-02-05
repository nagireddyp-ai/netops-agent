from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import duckdb
import numpy as np
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer

from .models import Runbook


class RunbookIndex:
    def __init__(self, db_path: str = "outputs/netops.duckdb") -> None:
        self.db_path = db_path
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.runbooks: List[Runbook] = []
        self.embeddings: np.ndarray | None = None

    def load_runbooks(self, runbook_path: Path) -> None:
        payload = yaml.safe_load(runbook_path.read_text())
        self.runbooks = [Runbook(**rb) for rb in payload.get("runbooks", [])]

    def build(self) -> None:
        corpus = [" ".join([rb.title, rb.category, *rb.steps, *rb.commands]) for rb in self.runbooks]
        self.embeddings = self.vectorizer.fit_transform(corpus).toarray()

    def persist(self) -> None:
        if self.embeddings is None:
            raise ValueError("Index not built")
        conn = duckdb.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runbooks (
                runbook_id VARCHAR,
                title VARCHAR,
                category VARCHAR,
                content VARCHAR,
                embedding DOUBLE[]
            );
            """
        )
        conn.execute("DELETE FROM runbooks")
        for rb, embedding in zip(self.runbooks, self.embeddings):
            content = "\n".join([rb.title, *rb.steps, *rb.commands])
            conn.execute(
                "INSERT INTO runbooks VALUES (?, ?, ?, ?, ?)",
                [rb.runbook_id, rb.title, rb.category, content, embedding.tolist()],
            )

    def query(self, text: str, top_k: int = 1) -> List[Tuple[Runbook, float]]:
        if self.embeddings is None:
            raise ValueError("Index not built")
        query_vec = self.vectorizer.transform([text]).toarray()[0]
        scores = self._cosine_similarity(self.embeddings, query_vec)
        ranked = np.argsort(scores)[::-1][:top_k]
        return [(self.runbooks[idx], float(scores[idx])) for idx in ranked]

    @staticmethod
    def _cosine_similarity(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
        denominator = np.linalg.norm(matrix, axis=1) * (np.linalg.norm(vector) + 1e-8)
        return (matrix @ vector) / (denominator + 1e-8)
