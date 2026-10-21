"""Streamlit entry point for CareerCompass AI."""

from __future__ import annotations

import streamlit as st

from backend.career_matcher import CareerMatcher
from backend.chatbot_service import ChatbotService
from backend.data_loader import load_careers
from backend.nlp_engine import normalize_text
from frontend.components import render_career_card, render_comparison_chart, render_roadmap
from frontend.styles import APP_CSS

st.set_page_config(page_title="CareerCompass AI", page_icon="🧭", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


@st.cache_resource
def get_career_data():
    careers = load_careers()
    matcher = CareerMatcher(careers)
    return careers, matcher, ChatbotService(matcher)


def reset_session() -> None:
    st.session_state["messages"] = []
    st.session_state["profile_context"] = ""
    st.session_state["latest_recommendations"] = []
    st.session_state["latest_roadmap"] = []


for key, default in (
    ("messages", []),
    ("profile_context", ""),
    ("latest_recommendations", []),
    ("latest_roadmap", []),
):
    if key not in st.session_state:
        st.session_state[key] = default

try:
    careers, matcher, chatbot = get_career_data()
except (ValueError, OSError) as exc:
    st.error(f"Career data could not be loaded: {exc}")
    st.stop()

with st.sidebar:
    st.markdown("## Your profile")
    profile_context = st.text_area(
        "Skills, interests, goals, and preferred work",
        value=st.session_state["profile_context"],
        height=150,
        placeholder="For example: I study computer science, know Java and SQL, and enjoy backend development.",
        help="Only share information relevant to career exploration. This app does not need personal identifiers.",
    )
    st.session_state["profile_context"] = profile_context
    threshold = st.slider(
        "Minimum text/profile similarity",
        min_value=0.0,
        max_value=0.2,
        value=0.025,
        step=0.005,
        help="This filters weak text matches. It is not a career-success probability.",
    )
    matcher.relevance_threshold = threshold
    if st.button("Clear conversation and profile", use_container_width=True):
        reset_session()
        st.rerun()
    st.caption("Your profile and conversation remain in this browser session only.")

user_history = [
    item["content"]
    for item in st.session_state["messages"]
    if item["role"] == "user"
]
active_profile = " ".join([profile_context, *user_history]).strip()
if active_profile:
    st.session_state["latest_recommendations"] = matcher.recommend(
        active_profile, top_n=3, relevance_threshold=threshold
    )

st.markdown(
    '<div class="hero"><div class="eyebrow">Explore with clarity</div>'
    '<h1>CareerCompass AI</h1>'
    '<p class="muted">An explainable, local NLP career exploration assistant for students and early-career users.</p></div>',
    unsafe_allow_html=True,
)

overview, chat_tab, matches_tab, compare_tab, method_tab = st.tabs(
    ["Overview", "Career chat", "Recommendations & roadmap", "Compare careers", "How it works"]
)

with overview:
    st.subheader("A practical starting point for your next step")
    first, second, third = st.columns(3)
    first.metric("Career profiles", len(careers))
    second.metric("Recommendation method", "TF-IDF + cosine")
    third.metric("External API required", "No")
    st.write(
        "Describe what you know, what interests you, or what kind of work you want to explore. "
        "CareerCompass compares your text with a small illustrative local knowledge base, explains its matches, "
        "and suggests flexible learning steps."
    )
    st.info("Similarity scores describe overlap with the dataset text; they are not probabilities of employability or success.")

with chat_tab:
    st.subheader("Conversation")
    for entry in st.session_state["messages"]:
        with st.chat_message(entry["role"]):
            st.write(entry["content"])
    prompt = st.chat_input("Share your interests, skills, or a career question")
    if prompt is not None:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.spinner("Looking for relevant career profiles..."):
            full_profile = " ".join(
                [profile_context]
                + [item["content"] for item in st.session_state["messages"] if item["role"] == "user"]
            )
            result = chatbot.respond(prompt, profile=profile_context)
            if result.get("recommendations"):
                result["recommendations"] = matcher.recommend(
                    full_profile, top_n=3, relevance_threshold=threshold
                )
                if not result["recommendations"]:
                    result["text"] = (
                        "I couldn’t find a sufficiently relevant match in the local dataset. "
                        "Add a few skills, subjects you enjoy, or a work area you want to explore."
                    )
                else:
                    if result.get("roadmap"):
                        result["roadmap"] = chatbot.respond(
                            "learning roadmap",
                            profile=full_profile,
                        ).get("roadmap", [])
                    selected = result.get("selected_career")
                    if selected:
                        selected_id = selected["career_id"]
                        result["selected_career"] = next(
                            career for career in result["recommendations"]
                            if career["career_id"] == selected_id
                        ) if any(c["career_id"] == selected_id for c in result["recommendations"]) else result["recommendations"][0]
            st.session_state["latest_recommendations"] = result.get("recommendations", [])
            st.session_state["latest_roadmap"] = result.get("roadmap", [])
            assistant_text = result["text"]
            st.session_state["messages"].append({"role": "assistant", "content": assistant_text})
        st.rerun()

with matches_tab:
    st.subheader("Top career matches")
    if st.session_state["latest_recommendations"]:
        for rank, career in enumerate(st.session_state["latest_recommendations"], start=1):
            render_career_card(career, rank)
        st.markdown("#### Similarity comparison")
        render_comparison_chart(st.session_state["latest_recommendations"])
        st.markdown("#### Learning roadmap")
        roadmap = st.session_state["latest_roadmap"]
        if not roadmap:
            selected = st.session_state["latest_recommendations"][0]
            roadmap = chatbot.respond(
                f"roadmap for {selected['title']}",
                profile=profile_context + " " + " ".join(
                    item["content"] for item in st.session_state["messages"] if item["role"] == "user"
                ),
            ).get("roadmap", [])
        render_roadmap(roadmap)
        st.markdown("**Starter project ideas**")
        st.write(", ".join(st.session_state["latest_recommendations"][0]["project_ideas"]))
    else:
        st.info("Start a conversation or add profile details, then ask for a recommendation or learning plan.")

with compare_tab:
    st.subheader("Compare two career profiles")
    left, right = st.columns(2)
    options = {career["title"]: career["career_id"] for career in careers}
    first_title = left.selectbox("First career", list(options))
    second_title = right.selectbox(
        "Second career", list(options), index=min(1, len(options) - 1)
    )
    if first_title == second_title:
        st.info("Select two different career profiles to compare.")
    else:
        comparison = matcher.compare(options[first_title], options[second_title])
        shared, first_only, second_only = st.columns(3)
        shared.markdown("**Shared required skills**")
        shared.write(", ".join(comparison["shared_skills"]) or "No shared listed skills")
        first_only.markdown(f"**{first_title} focus**")
        first_only.write(", ".join(comparison["first_unique_skills"]) or "No additional listed skills")
        second_only.markdown(f"**{second_title} focus**")
        second_only.write(", ".join(comparison["second_unique_skills"]) or "No additional listed skills")
        st.caption("Career profiles are illustrative and are not authoritative occupational standards.")

with method_tab:
    st.subheader("How the NLP works")
    st.markdown(
        """
1. **Normalize:** lowercase text, clean punctuation, and standardize whitespace.
2. **Represent:** scikit-learn converts the user's profile and each local career description into TF-IDF vectors using unigrams and bigrams.
3. **Compare:** cosine similarity ranks text overlap between the profile and each career document.
4. **Explain:** explicitly mentioned dataset skills and interests are listed separately from unconfirmed skills.
5. **Guide:** curated learning topics and projects are arranged into flexible stages.

Explicit skills and goals receive more emphasis when profile fields are provided. The chatbot uses transparent rule-based intent matching and retrieval; it does not use a transformer, a large language model, or generated facts. Similarity is a text relevance measure, not a calibrated prediction.
        """
    )
    st.caption("Career data, profile text, and conversation are processed locally; nothing is written to persistent storage by this app.")
