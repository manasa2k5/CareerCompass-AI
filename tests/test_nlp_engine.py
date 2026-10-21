from backend.nlp_engine import extract_terms, make_vectorizer, normalize_text


def test_normalize_text_standardizes_case_spacing_and_punctuation():
    assert normalize_text("  Java,  SQL!! C++ \n") == "java sql c++"


def test_vectorizer_builds_unigram_and_bigram_features():
    vectorizer = make_vectorizer()
    matrix = vectorizer.fit_transform(["data analysis with python", "python for data science"])
    assert matrix.shape == (2, len(vectorizer.get_feature_names_out()))
    assert "data analysis" in vectorizer.get_feature_names_out()


def test_extract_terms_matches_phrases_without_partial_word_matches():
    assert extract_terms("I use Java and SQL daily", ["Java", "JavaScript", "SQL"]) == ["Java", "SQL"]
