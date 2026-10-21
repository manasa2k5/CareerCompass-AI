"""Rule-based conversational service over the local career matcher."""

from __future__ import annotations

import re
from typing import Any

from backend.career_matcher import CareerMatcher, build_profile_text
from backend.roadmap_generator import generate_roadmap
from backend.nlp_engine import normalize_text


class ChatbotService:
    """Route common intents and retrieve career information without an LLM."""

    def __init__(self, matcher: CareerMatcher) -> None:
        self.matcher = matcher

    def detect_intent(self, message: str) -> str:
        text = normalize_text(message)
        if not text:
            return "insufficient"
        if re.search(r"\b(compare|difference|differ|versus|vs)\b", text):
            return "compare"
        if re.search(r"\b(project|portfolio idea|build something)\b", text):
            return "projects"
        if re.search(r"\b(roadmap|learning plan|study plan)\b", text):
            return "roadmap"
        if re.search(r"\b(learn next|skill gap|skills should i learn|what skills)\b", text):
            return "skills"
        if re.search(r"\b(what is|tell me about|explain|describe)\b", text) and any(
            normalize_text(career["title"]) in text for career in self.matcher.careers
        ):
            return "career_info"
        if re.search(r"\b(hello|hi|hey|good morning|good afternoon)\b", text):
            return "greeting"
        if re.search(r"\b(help|how do i|how can i)\b", text):
            return "help"
        if re.search(r"\b(recommend|suggest|career|role|which path|what should i)\b", text):
            return "recommendations"
        detected = self.matcher.extract_profile_terms(text)
        if detected["skills"] or detected["interests"]:
            return "profile"
        query_vector = self.matcher.vectorizer.transform([text])
        if query_vector.nnz and self.matcher.recommend(text, top_n=1):
            return "profile"
        return "unrelated"

    def respond(self, message: str, profile: str = "") -> dict[str, Any]:
        intent = self.detect_intent(message)
        combined = build_profile_text(f"{profile} {message}".strip())
        response: dict[str, Any] = {"intent": intent, "text": "", "recommendations": [], "roadmap": []}

        if intent == "greeting":
            response["text"] = "Hello! Share your skills, interests, or goals and I can explore career paths with you."
        elif intent == "help":
            response["text"] = (
                "Tell me what you know, what you enjoy, and the kind of work you prefer. "
                "You can also ask about a career, compare roles, request project ideas, or ask for a learning roadmap."
            )
        elif intent == "insufficient":
            response["text"] = "Please share a little about your interests, skills, or career question to get started."
        elif intent == "compare":
            response["text"] = (
                "Choose two careers in the comparison controls below. I’ll compare their illustrative skills and focus areas."
            )
        elif intent == "unrelated":
            response["text"] = (
                "I focus on career exploration, skills, and learning plans. Try describing a subject or skill you enjoy."
            )
        elif intent == "profile":
            response["text"] = "Thanks for sharing. I’ll use those explicitly mentioned details to find exploratory matches."
            response["recommendations"] = self.matcher.recommend(combined)
            if not response["recommendations"]:
                response["text"] += " I need a little more career-related context to find a relevant match."
            elif re.search(r"\b(ai|artificial intelligence)\b", normalize_text(message)) and re.search(
                r"\b(math|mathematics)\b", normalize_text(message)
            ):
                response["text"] = (
                    "AI includes roles with different levels of mathematical depth, so current math comfort "
                    "does not rule out exploring the field. Start with programming, basic algebra and statistics, "
                    "then build toward the math used by a specific role."
                )
        elif intent in {"recommendations", "skills", "roadmap", "career_info", "projects"}:
            response["recommendations"] = self.matcher.recommend(combined)
            if not response["recommendations"]:
                response["text"] = (
                    "I couldn’t find a sufficiently relevant match in the local dataset. "
                    "Add a few skills, subjects you enjoy, or a work area you want to explore."
                )
                return response
            selected = response["recommendations"][0]
            response["selected_career"] = selected
            if intent == "recommendations":
                response["text"] = (
                    "Here are the strongest text/profile similarity matches from the local career dataset. "
                    "They are prompts for exploration, not predictions of success."
                )
            elif intent == "skills":
                response["text"] = (
                    f"For {selected['title']}, explore these unconfirmed illustrative skills next: "
                    + (", ".join(selected["unconfirmed_skills"][:5]) or "build depth in your current skills")
                    + ". 'Unconfirmed' means they were not detected in your text, not that you lack them."
                )
            elif intent == "career_info":
                response["text"] = (
                    f"{selected['title']}: {selected['description']} "
                    f"Typical work includes {', '.join(selected['typical_tasks'][:3])}."
                )
            elif intent == "projects":
                response["text"] = (
                    f"Project ideas for {selected['title']}: "
                    + "; ".join(selected["project_ideas"][:3])
                )
            else:
                response["roadmap"] = generate_roadmap(
                    selected, self.matcher.extract_profile_terms(combined)["skills"]
                )
                response["text"] = (
                    f"Here is a flexible learning roadmap for {selected['title']}. "
                    "Adjust the order and pace to your prior experience."
                )
            if (
                intent != "profile"
                and re.search(r"\b(ai|artificial intelligence)\b", normalize_text(message))
                and re.search(r"\b(math|mathematics)\b", normalize_text(message))
            ):
                response["text"] += (
                    " AI roles vary in mathematical depth; begin with programming, basic algebra, and statistics "
                    "rather than treating current math confidence as a disqualifier."
                )
        elif intent == "profile":
            response["recommendations"] = self.matcher.recommend(combined)
        return response
