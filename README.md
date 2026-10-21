# CareerCompass AI

CareerCompass AI is a local, explainable career exploration chatbot for students and early-career users. It compares a user's stated skills, interests, goals, and preferred work with an illustrative collection of career profiles, then presents text-similarity matches and flexible next steps.

## Problem statement and objectives

Career choices can feel difficult when it is unclear how current interests and skills relate to different roles. This project demonstrates a transparent NLP workflow that can help users explore possibilities without presenting automated results as a verdict or employment prediction.

Objectives:

- Interpret a natural-language description with lightweight, reproducible NLP.
- Retrieve and rank relevant career profiles from a local CSV knowledge base.
- Explain explicitly detected and unconfirmed skills.
- Provide a staged learning roadmap and project prompts.
- Demonstrate multi-turn interaction, interactive comparison, and automated tests.

## Features

- Streamlit chat UI with session-only conversation and profile state.
- 18 illustrative career profiles spanning software, data, AI, infrastructure, design, product, quality, business, mobile, and technical communication.
- TF-IDF vectorization, cosine similarity, configurable relevance threshold, deterministic ranking.
- Rule-based intent matching and retrieval-based career information; no paid API, API key, internet access at runtime, transformer, or LLM.
- Skill and interest phrase detection against the local dataset.
- Career comparison, Plotly match chart, roadmap, and project ideas.
- Reset control that clears profile, messages, matches, and roadmap.

## Technology stack

Python 3.10+, Streamlit, scikit-learn, pandas, Plotly, and pytest. The application uses standard-library modules for text normalization and intent routing.

## Architecture

```text
app.py                         Streamlit page, session state, and application wiring
backend/
  data_loader.py               CSV schema validation and parsing
  nlp_engine.py                normalization, TF-IDF configuration, term extraction
  career_matcher.py            weighted profile composition, ranking, explanations
  chatbot_service.py           transparent intent router and retrieval responses
  roadmap_generator.py         staged, adaptable learning plans
frontend/
  components.py                recommendation cards, chart, roadmap components
  styles.py                    static local CSS
data/
  careers.csv                  illustrative career knowledge base
  conversation_examples.json   representative intent examples
tests/                         offline unit tests
```

## NLP methodology

Text is lowercased, punctuation outside common technical forms is normalized, and whitespace is collapsed. A scikit-learn `TfidfVectorizer` creates unigram and bigram features using English stop words. Each career document combines its title, category, description, required and related skills, interests, tasks, and learning topics. Required skills are repeated once to give explicitly listed role skills modestly greater representation.

When profile fields are supplied separately, skills, goals, interests, and preferences receive configurable fixed emphasis in `backend/career_matcher.py`: explicit skills are repeated twice, goals approximately twice, interests one and a half times, and preferences slightly more than once. Free text is retained at its base weight. These are simple, documented relevance choices, not learned or validated coefficients.

For a user vector \(u\) and a career vector \(c\), cosine similarity is:

```text
cosine_similarity(u, c) = (u · c) / (||u|| × ||c||)
```

Scores are shown as percentages of text/profile similarity for readability. They are not calibrated probabilities, measures of aptitude, or predictions of career success. A configurable threshold filters weak matches. An empty or out-of-vocabulary profile produces no results rather than a misleading recommendation.

Skill extraction detects phrases explicitly present in the user's text. A listed skill that was not detected is called **unconfirmed**, not a skill the user lacks. Matching and ranking are deterministic for a fixed dataset, scikit-learn version, and input.

The chatbot uses transparent keyword and phrase rules for greeting, help, recommendation, career detail, skill, roadmap, project, comparison, profile, and fallback intents. It retrieves facts only from local career records and does not generate unsupported facts.

## Dataset and limitations

`data/careers.csv` uses semicolons to separate list values. Required columns are validated by the loader; missing list values become empty lists, and duplicate career IDs are discarded after the first record. Career descriptions and skill profiles are illustrative examples for this academic project, not authoritative occupational standards. The dataset does not claim salary, employment, or success outcomes.

The matcher is limited by wording and coverage in this small knowledge base. Synonyms can be missed, TF-IDF does not understand context, and overlap can vary when descriptions change. Matching scores should be used as conversation starters. The prototype does not store profiles or conversation history persistently; state is held in the current Streamlit session.

## Installation and running

### Windows PowerShell

From the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
python -m streamlit run app.py
```

If PowerShell blocks activation, use the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### General Python environments

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
python -m streamlit run app.py
```

Python 3.10 or newer is recommended. Runtime career data is loaded from a path relative to the project source, not the shell's current directory. No external service is contacted by the application.

## Example interactions

Try:

> I am a CSE student. I know Java, SQL, HTML, and CSS. I like problem-solving and backend development. What career should I choose?

The app compares this text with local role profiles, is expected to surface Java/backend-related matches, states which listed skills were mentioned or remain unconfirmed, and provides a flexible roadmap.

> I like AI but I am not comfortable with advanced mathematics yet.

The app can show exploratory AI-related paths without treating current math comfort as a disqualifier. It encourages foundational learning; different AI roles have different mathematical emphases.

Other examples include asking for a roadmap, project ideas, a role description, or selecting two career profiles in the comparison tab. An unrelated question receives a clear career-focused fallback; an empty profile asks the user for more information.

## Testing

```powershell
python -m pytest -v
```

Tests cover data schema and parsing, text normalization and vectorization, ranking, term extraction, empty and unknown input, career comparisons, intent routing, roadmap generation, fallback behavior, and local example consistency. Tests do not call external services.

## Five-minute demonstration

1. Launch the app and introduce the project and its local-only, explainable approach.
2. Enter the Java/SQL/backend example in the profile or chat and show the top match explanations.
3. Point out the profile-similarity label and clarify that it is not a success probability.
4. Show the comparison chart and the unconfirmed-skill wording.
5. Open the roadmap and project ideas; compare two careers, then clear the session to demonstrate reset behavior.

## Future enhancements

- Expand and review the curated career profiles with domain experts.
- Add synonym handling and user-tested phrasing while keeping explanations inspectable.
- Add accessibility and localization reviews.
- Add optional, explicit export of a user's own roadmap if a persistence feature is desired.
- Evaluate relevance with a documented, consent-aware set of test profiles before making stronger claims.
