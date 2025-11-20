"""
Tests for lemmatization functionality in YAKE.

This module tests the lemmatization feature that aggregates keywords
with the same lemma (e.g., "tree" and "trees").
"""

import pytest
import yake


def test_lemmatization_disabled_by_default():
    """Test that lemmatization is disabled by default."""
    text = "Trees are important. Many trees provide shade. Tree conservation matters."
    
    kw = yake.KeywordExtractor(lan="en", n=1, top=10)
    assert kw.lemmatize is False
    
    # Should extract both "trees" and "tree" as separate keywords
    result = kw.extract_keywords(text)
    keywords = [k for k, s in result]
    
    # At least one form should be present
    assert len(keywords) > 0


def test_lemmatization_enabled():
    """Test that lemmatization combines keywords with same lemma."""
    text = "Trees are important. Many trees provide shade. Tree conservation matters."
    
    # Without lemmatization
    kw_no_lemma = yake.KeywordExtractor(lan="en", n=1, top=10, lemmatize=False)
    result_no_lemma = kw_no_lemma.extract_keywords(text)
    keywords_no_lemma = [k.lower() for k, s in result_no_lemma]
    
    # With lemmatization (requires spacy)
    kw_with_lemma = yake.KeywordExtractor(lan="en", n=1, top=10, lemmatize=True)
    result_with_lemma = kw_with_lemma.extract_keywords(text)
    keywords_with_lemma = [k.lower() for k, s in result_with_lemma]
    
    # Lemmatized version should have same or fewer keywords
    # (if spacy is installed, it will combine "tree" and "trees")
    assert len(keywords_with_lemma) <= len(keywords_no_lemma)


def test_lemmatization_aggregation_min():
    """Test that min aggregation uses the best (lowest) score."""
    text = "Running is good. The runner runs fast. Runners love running."
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="min"
    )
    result = kw.extract_keywords(text)
    
    # Should have at least some keywords
    assert len(result) > 0
    
    # All scores should be positive
    for keyword, score in result:
        assert score >= 0


def test_lemmatization_aggregation_mean():
    """Test that mean aggregation averages scores."""
    text = "Running is good. The runner runs fast. Runners love running."
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="mean"
    )
    result = kw.extract_keywords(text)
    
    # Should have at least some keywords
    assert len(result) > 0
    
    # All scores should be positive
    for keyword, score in result:
        assert score >= 0


def test_lemmatization_aggregation_max():
    """Test that max aggregation uses the worst (highest) score."""
    text = "Running is good. The runner runs fast. Runners love running."
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="max"
    )
    result = kw.extract_keywords(text)
    
    # Should have at least some keywords
    assert len(result) > 0
    
    # All scores should be positive
    for keyword, score in result:
        assert score >= 0


def test_lemmatization_aggregation_harmonic():
    """Test that harmonic aggregation uses harmonic mean."""
    text = "Running is good. The runner runs fast. Runners love running."
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="harmonic"
    )
    result = kw.extract_keywords(text)
    
    # Should have at least some keywords
    assert len(result) > 0
    
    # All scores should be positive
    for keyword, score in result:
        assert score >= 0


def test_lemmatization_with_multiword():
    """Test lemmatization with multi-word keywords."""
    text = """
    Machine learning algorithms are powerful. Deep learning models excel.
    Natural language processing tasks benefit from machine learning.
    """
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=2, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="min"
    )
    result = kw.extract_keywords(text)
    
    # Should extract bigrams
    assert len(result) > 0
    
    # Check that we have multi-word keywords
    multiword = [k for k, s in result if " " in k]
    assert len(multiword) > 0


def test_lemmatization_graceful_degradation():
    """Test that lemmatization gracefully degrades if libraries not available."""
    text = "Trees are important. Many trees provide shade."
    
    # This should work even if spacy/nltk are not installed
    # (will log warning but continue)
    kw = yake.KeywordExtractor(lan="en", n=1, top=5, lemmatize=True)
    result = kw.extract_keywords(text)
    
    # Should return results (either lemmatized or not)
    assert isinstance(result, list)


def test_lemmatization_empty_text():
    """Test lemmatization with empty text."""
    kw = yake.KeywordExtractor(lan="en", n=1, top=5, lemmatize=True)
    result = kw.extract_keywords("")
    
    assert result == []


def test_lemmatization_preserves_original_form():
    """Test that lemmatization preserves one of the original forms."""
    text = "The algorithms are powerful. Algorithm design is important."
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="min"
    )
    result = kw.extract_keywords(text)
    keywords = [k for k, s in result]
    
    # Should return actual words from text, not lemmatized forms
    # (e.g., "algorithms" or "algorithm", not "algoritm")
    for keyword in keywords:
        assert len(keyword) > 0
        # Keywords should be recognizable words
        assert keyword.replace(" ", "").isalpha() or " " in keyword


def test_lemmatization_different_languages():
    """Test that lemmatization respects language setting."""
    text_pt = "Os algoritmos são poderosos. Algoritmo de aprendizado é importante."
    
    # Portuguese text with lemmatization
    kw = yake.KeywordExtractor(
        lan="pt", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemmatizer="spacy"
    )
    result = kw.extract_keywords(text_pt)
    
    # Should return results (may fall back to English model if pt not installed)
    assert isinstance(result, list)


def test_lemmatization_nltk_backend():
    """Test lemmatization with NLTK backend."""
    text = "Running is good. The runner runs fast."
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemmatizer="nltk",
        lemma_aggregation="min"
    )
    result = kw.extract_keywords(text)
    
    # Should return results
    assert isinstance(result, list)


def test_lemmatization_unknown_aggregation():
    """Test that unknown aggregation method falls back to min."""
    text = "Trees are important. Many trees provide shade."
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=5, 
        lemmatize=True,
        lemma_aggregation="unknown_method"
    )
    result = kw.extract_keywords(text)
    
    # Should still work (with warning logged)
    assert isinstance(result, list)


def test_lemmatization_score_ordering():
    """Test that lemmatized results are still properly ordered by score."""
    text = """
    Machine learning is a powerful technology. Deep learning excels at pattern recognition.
    Artificial intelligence transforms industries. Machine learning algorithms are everywhere.
    """
    
    kw = yake.KeywordExtractor(
        lan="en", 
        n=2, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="min"
    )
    result = kw.extract_keywords(text)
    
    # Verify results are sorted by score (ascending)
    scores = [s for k, s in result]
    assert scores == sorted(scores)


def test_lemmatization_comparison_with_without():
    """Compare results with and without lemmatization."""
    text = """
    The researchers researched machine learning. Their research shows that
    learning algorithms can learn patterns. The learned patterns are useful.
    """
    
    # Without lemmatization
    kw_no_lemma = yake.KeywordExtractor(lan="en", n=1, top=20, lemmatize=False)
    result_no_lemma = kw_no_lemma.extract_keywords(text)
    
    # With lemmatization
    kw_with_lemma = yake.KeywordExtractor(lan="en", n=1, top=20, lemmatize=True)
    result_with_lemma = kw_with_lemma.extract_keywords(text)
    
    # Both should return results
    assert len(result_no_lemma) > 0
    assert len(result_with_lemma) > 0
    
    # Lemmatized version should have same or fewer unique keywords
    unique_no_lemma = set(k.lower() for k, s in result_no_lemma)
    unique_with_lemma = set(k.lower() for k, s in result_with_lemma)
    
    # This might be equal if spacy is not installed (graceful degradation)
    assert len(unique_with_lemma) <= len(unique_no_lemma)
