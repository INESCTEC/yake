"""
Feature calculation module for YAKE keyword extraction.

This module contains pure functions for calculating statistical features
used to score and rank keyword candidates. Separating feature calculations
from data structures improves testability and maintainability.

Based on the modular architecture from the reference YAKE implementation.
"""

import logging
import math
from typing import Any

import numpy as np  # pylint: disable=import-error

# Configure module logger
logger = logging.getLogger(__name__)


# pylint: disable=too-many-locals
def calculate_term_features(
    term: Any,
    max_tf: float,
    avg_tf: float,
    std_tf: float,
    number_of_sentences: int,
) -> dict[str, float]:
    """
    Calculate all statistical features for a single term.

    This function computes various statistical features that determine
    a term's importance as a potential keyword. Features include term
    relevance, frequency, spread, case information, and position.

    Args:
        term: SingleWord object containing term information
        max_tf: Maximum term frequency in the document
        avg_tf: Average term frequency across all terms
        std_tf: Standard deviation of term frequency
        number_of_sentences: Total number of sentences in document

    Returns:
        Calculated features including WRel, WFreq, WSpread, WCase, WPos, H
    """
    # Get graph metrics (cached in SingleWord)
    if hasattr(term, "get_graph_metrics"):
        metrics = term.get_graph_metrics()
    else:
        metrics = term.graph_metrics

    # Calculate WRel (term relevance based on graph connectivity)
    pwl = metrics["pwl"]
    pwr = metrics["pwr"]
    pl = metrics["wdl"] / max_tf if max_tf > 0 else 0
    pr = metrics["wdr"] / max_tf if max_tf > 0 else 0

    w_rel = (0.5 + (pwl * (term.tf / max_tf))) + (0.5 + (pwr * (term.tf / max_tf)))

    # Calculate WFreq (normalized term frequency)
    w_freq = term.tf / (avg_tf + std_tf) if (avg_tf + std_tf) > 0 else 0

    # Calculate WSpread (term spread across sentences)
    w_spread = len(term.sentence_ids) / number_of_sentences

    # Calculate WCase (capitalization pattern)
    w_case = max(term.tf_a, term.tf_n) / (1.0 + math.log(term.tf))

    # Calculate WPos (position feature using median)
    positions = list(term.occurs.keys())
    w_pos = math.log(math.log(3.0 + np.median(positions)))

    # Calculate H (overall importance score)
    h_score = (w_pos * w_rel) / (w_case + (w_freq / w_rel) + (w_spread / w_rel))

    return {
        "w_rel": w_rel,
        "w_freq": w_freq,
        "w_spread": w_spread,
        "w_case": w_case,
        "w_pos": w_pos,
        "pl": pl,
        "pr": pr,
        "h": h_score,
    }


def calculate_composed_features(
    composed_word: Any,
    stopword_weight: str = "bi",
) -> dict[str, float]:
    """
    Calculate features for multi-word expressions (n-grams).

    Combines features from individual terms to score the entire phrase,
    with special handling for stopwords based on the weighting method.

    Args:
        composed_word: ComposedWord object containing the n-gram
        stopword_weight: Method for handling stopwords ('bi', 'h', or 'none')

    Returns:
        Features including prod_h, sum_h, tf_used, and H score
    """
    sum_h = 0.0
    prod_h = 1.0

    # Process each term in the composed word
    for t, term in enumerate(composed_word.terms):
        if not term.stopword:
            # Non-stopwords: directly contribute their H scores
            sum_h += term.h
            prod_h *= term.h
        # Stopwords: weight by connection probability
        elif stopword_weight == "bi":
            prob_t1 = prob_t2 = 0.0

            # Probability from previous term to current stopword
            if t > 0 and term.g.has_edge(composed_word.terms[t - 1].id, term.id):
                edge_data = term.g[composed_word.terms[t - 1].id][term.id]
                prob_t1 = edge_data["tf"] / composed_word.terms[t - 1].tf

            # Probability from current stopword to next term
            if t < len(composed_word.terms) - 1 and term.g.has_edge(
                term.id,
                composed_word.terms[t + 1].id,
            ):
                edge_data = term.g[term.id][composed_word.terms[t + 1].id]
                prob_t2 = edge_data["tf"] / composed_word.terms[t + 1].tf

            # Combined probability affects the score
            prob = prob_t1 * prob_t2
            prod_h *= 1 + (1 - prob)
            sum_h -= 1 - prob

        elif stopword_weight == "h":
            # Alternative: include stopword's H value
            sum_h += term.h
            prod_h *= term.h
            # If 'none', stopwords are ignored (no contribution)

    # Use term frequency
    tf_used = composed_word.tf

    # Calculate final H score
    h_score = prod_h / ((sum_h + 1) * tf_used) if tf_used > 0 else 0

    return {"prod_h": prod_h, "sum_h": sum_h, "tf_used": tf_used, "h": h_score}


def get_feature_aggregation(
    composed_word: Any,
    feature_name: str,
    exclude_stopwords: bool = True,
) -> tuple[float, float, float]:
    """
    Aggregate a specific feature across all terms in a composed word.

    Computes sum, product, and ratio of feature values, optionally
    excluding stopwords.

    Args:
        composed_word: ComposedWord object
        feature_name: Name of the feature attribute to aggregate
        exclude_stopwords: Whether to skip stopwords (default: True)

    Returns:
        (sum, product, ratio) where ratio = product / (sum + 1)
    """
    feature_values = [
        getattr(term, feature_name)
        for term in composed_word.terms
        if not exclude_stopwords or not term.stopword
    ]

    if not feature_values:
        return (0.0, 0.0, 0.0)

    sum_f = sum(feature_values)
    prod_f = np.prod(feature_values)
    ratio = prod_f / (sum_f + 1)

    return (sum_f, prod_f, ratio)
