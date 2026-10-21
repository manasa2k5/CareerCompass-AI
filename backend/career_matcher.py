"""TF-IDF career ranking, comparisons, and match explanations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sklearn.metrics.pairwise import cosine_similarity

from backend.data_loader import load_careers
from backend.nlp_engine import career_document, extract_terms, make_vectorizer, normalize_text

PROFILE_WEIGHTS = {
    "text": 1.0,
    "skills": 2.0,
    "interests": 1.5,
    "goals": 1.8,
    "preferences": 1.2,
}


def build_profile_text(profile: str | Mapping[str, Any]) -> str:
    """Combine profile fields with documented emphasis on explicit skills and goals."""
    if isinstance(profile, str):
        return normalize_text(profile)
    pieces: list[str] = []
    for field, weight in PROFILE_WEIGHTS.items():
        value = profile.get(field, "")
        if isinstance(value, (list, tuple, set)):
            value = " ".join(str(item) for item in value)
        normalized = normalize_text(str(value))
        if normalized:
            pieces.extend([normalized] * int(weight + 0.5))
    return " ".join(pieces)


class CareerMatcher:
    """Build an in-memory TF-IDF index and rank curated career profiles."""

    def __init__(
        self,
        careers: list[dict[str, Any]] | None = None,
        relevance_threshold: float = 0.025,
    ) -> None:
        self.careers = careers if careers is not None else load_careers()
        if not self.careers:
            raise ValueError("At least one career profile is required.")
        if not 0 <= relevance_threshold <= 1:
            raise ValueError("relevance_threshold must be between 0 and 1.")
        self.relevance_threshold = relevance_threshold
        self.vectorizer = make_vectorizer()
        documents = [career_document(career) for career in self.careers]
        self.matrix = self.vectorizer.fit_transform(documents)
        self._skills = sorted(
            {skill for career in self.careers for skill in
             (career.get("required_skills", []) + career.get("related_skills", []))},
            key=lambda item: (len(item), item.lower()),
        )
        self._interests = sorted(
            {interest for career in self.careers for interest in career.get("interests", [])},
            key=lambda item: (len(item), item.lower()),
        )

    def extract_profile_terms(self, text: str) -> dict[str, list[str]]:
        return {
            "skills": extract_terms(text, self._skills),
            "interests": extract_terms(text, self._interests),
        }

    def recommend(
        self,
        profile: str | Mapping[str, Any],
        top_n: int = 3,
        relevance_threshold: float | None = None,
    ) -> list[dict[str, Any]]:
        query = build_profile_text(profile)
        if not query.strip() or top_n <= 0:
            return []
        threshold = self.relevance_threshold if relevance_threshold is None else relevance_threshold
        if not 0 <= threshold <= 1:
            raise ValueError("relevance_threshold must be between 0 and 1.")
        query_vector = self.vectorizer.transform([query])
        if query_vector.nnz == 0:
            return []
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        detected = self.extract_profile_terms(query)
        ranked = sorted(
            enumerate(scores),
            key=lambda pair: (-float(pair[1]), self.careers[pair[0]]["title"].lower()),
        )
        results: list[dict[str, Any]] = []
        for index, score in ranked:
            if score <= 0 or score < threshold:
                continue
            career = self.careers[index]
            required = career.get("required_skills", [])
            related = career.get("related_skills", [])
            mentioned = set(detected["skills"])
            relevant = [skill for skill in required + related if skill in mentioned]
            unconfirmed = [skill for skill in required if skill not in mentioned]
            result = dict(career)
            result.update(
                similarity_score=round(float(score) * 100, 1),
                relevant_skills=relevant,
                unconfirmed_skills=unconfirmed,
                explanation=self._explain(career, score, relevant, detected["interests"]),
            )
            results.append(result)
            if len(results) >= top_n:
                break
        return results

    @staticmethod
    def _explain(career: dict[str, Any], score: float, skills: list[str],
                 interests: list[str]) -> str:
        reasons: list[str] = []
        if skills:
            reasons.append("your stated skills include " + ", ".join(skills[:4]))
        matching_interests = [item for item in career.get("interests", []) if item in interests]
        if matching_interests:
            reasons.append("you mentioned interests such as " + ", ".join(matching_interests[:3]))
        if not reasons:
            reasons.append("your profile text overlaps with the role's description and learning topics")
        return (
            f"{career['title']} is a text/profile similarity match ({score * 100:.1f}%); "
            + "; ".join(reasons)
            + ". This score is not a probability of career success."
        )

    def compare(self, first_id: str, second_id: str) -> dict[str, Any]:
        by_id = {career["career_id"]: career for career in self.careers}
        if first_id not in by_id or second_id not in by_id:
            raise ValueError("Choose two career IDs that exist in the career dataset.")
        first, second = by_id[first_id], by_id[second_id]
        first_skills = set(first.get("required_skills", []))
        second_skills = set(second.get("required_skills", []))
        return {
            "first": first,
            "second": second,
            "shared_skills": sorted(first_skills & second_skills),
            "first_unique_skills": sorted(first_skills - second_skills),
            "second_unique_skills": sorted(second_skills - first_skills),
            "first_interests": first.get("interests", []),
            "second_interests": second.get("interests", []),
        }
