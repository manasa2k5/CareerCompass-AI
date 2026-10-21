"""Transparent text normalization and skill/interests extraction helpers."""

from __future__ import annotations

import re
from collections.abc import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer

_NON_WORD = re.compile(r"[^a-z0-9+#.\s]")
_WHITESPACE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Lowercase, retain common technical punctuation, and normalize spacing."""
    if not isinstance(text, str):
        return ""
    normalized = _NON_WORD.sub(" ", text.lower())
    return _WHITESPACE.sub(" ", normalized).strip()


def make_vectorizer() -> TfidfVectorizer:
    """Create a deterministic unigram/bigram TF-IDF vectorizer."""
    return TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b[\w+#.]+\b",
        sublinear_tf=True,
    )


def extract_terms(text: str, vocabulary: Iterable[str]) -> list[str]:
    """Return known terms explicitly mentioned in text, longest phrases first."""
    normalized = normalize_text(text)
    found: list[str] = []
    candidates = sorted({term.strip() for term in vocabulary if term and term.strip()},
                        key=lambda term: (-len(term), term.lower()))
    for term in candidates:
        candidate = normalize_text(term)
        if candidate and re.search(rf"(?<![\w+#.]){re.escape(candidate)}(?![\w+#.])", normalized):
            found.append(term)
    return found


def career_document(career: dict) -> str:
    """Build a weighted-by-repetition document from the curated career fields."""
    fields = (
        career.get("title", ""),
        career.get("category", ""),
        career.get("description", ""),
        " ".join(career.get("required_skills", [])),
        " ".join(career.get("required_skills", [])),
        " ".join(career.get("related_skills", [])),
        " ".join(career.get("interests", [])),
        " ".join(career.get("typical_tasks", [])),
        " ".join(career.get("learning_topics", [])),
    )
    return normalize_text(" ".join(str(value) for value in fields))
