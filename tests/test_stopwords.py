"""Regression tests for explicit stopword configuration."""

import pytest

from yake import KeywordExtractor


@pytest.mark.parametrize("stopwords", [set(), [], ()])
def test_empty_stopwords_disable_default_list(stopwords):
    """Empty collections must not fall back to language stopwords."""
    extractor = KeywordExtractor(
        lan="en", n=1, top=100, dedup_lim=1.0, stopwords=stopwords
    )

    assert extractor.stopword_set == set()
    keywords = extractor.extract_keywords(
        "The language model explains the science."
    )
    assert "the" in {keyword.lower() for keyword, _ in keywords}


def test_none_stopwords_keep_language_defaults():
    """Omitted and None stopwords retain the same default extraction."""
    default = KeywordExtractor(lan="en", n=1, top=100)
    explicit_none = KeywordExtractor(
        lan="en", n=1, top=100, stopwords=None
    )
    text = "The language model explains the science."

    assert "the" in default.stopword_set
    assert explicit_none.stopword_set == default.stopword_set
    assert (
        explicit_none.extract_keywords(text) == default.extract_keywords(text)
    )
    assert "the" not in {
        keyword.lower() for keyword, _ in default.extract_keywords(text)
    }


def test_nonempty_stopwords_replace_defaults_and_are_copied():
    """Custom words replace rather than extend the built-in list."""
    custom = {"science"}
    extractor = KeywordExtractor(
        lan="en", n=1, top=100, dedup_lim=1.0, stopwords=custom
    )
    custom.add("language")

    assert extractor.stopword_set == {"science"}
    keywords = {
        keyword.lower()
        for keyword, _ in extractor.extract_keywords(
            "The language model explains the science."
        )
    }
    assert "science" not in keywords
    assert "the" in keywords
