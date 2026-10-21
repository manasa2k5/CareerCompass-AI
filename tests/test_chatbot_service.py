import json
from pathlib import Path

from backend.career_matcher import CareerMatcher
from backend.chatbot_service import ChatbotService


def service():
    return ChatbotService(CareerMatcher())


def test_chatbot_routes_common_intents():
    bot = service()
    assert bot.detect_intent("Hello there") == "greeting"
    assert bot.detect_intent("Can you help me?") == "help"
    assert bot.detect_intent("Give me a learning roadmap") == "roadmap"
    assert bot.detect_intent("Suggest a project idea") == "projects"
    assert bot.detect_intent("Compare data analysis and data science") == "compare"
    assert bot.detect_intent("What skills should I learn next?") == "skills"


def test_chatbot_recommends_from_natural_language_profile():
    result = service().respond(
        "I am a CSE student. I know Java, SQL, HTML, and CSS. I like problem-solving and backend development."
    )
    assert result["intent"] == "profile"
    assert result["recommendations"]
    assert result["recommendations"][0]["career_id"] == "java_backend_developer"


def test_chatbot_handles_greetings_empty_and_unrelated_queries():
    bot = service()
    assert bot.respond("Hi")["intent"] == "greeting"
    assert bot.respond("  ")["intent"] == "insufficient"
    unrelated = bot.respond("What is the weather on Mars?")
    assert unrelated["intent"] == "unrelated"
    assert "focus on career exploration" in unrelated["text"]


def test_chatbot_gives_non_exclusionary_ai_math_guidance():
    result = service().respond("I like AI but I am not comfortable with advanced mathematics yet.")
    assert result["recommendations"]
    assert any(
        career["career_id"] in {"ai_engineer", "machine_learning_engineer", "nlp_engineer"}
        for career in result["recommendations"]
    )


def test_chatbot_roadmap_intent_returns_stages():
    result = service().respond("Can you make a roadmap for data analysis?")
    assert result["intent"] == "roadmap"
    assert len(result["roadmap"]) == 4


def test_local_conversation_examples_are_valid_and_match_intent_router():
    examples_path = Path(__file__).resolve().parents[1] / "data" / "conversation_examples.json"
    examples = json.loads(examples_path.read_text(encoding="utf-8"))
    bot = service()
    assert examples
    for example in examples:
        assert bot.detect_intent(example["user"]) == example["intent"]
