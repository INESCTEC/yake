"""
YAKE (Yet Another Keyword Extractor)
====================================

A light-weight unsupervised automatic keyword extraction method which rests on
text statistical features extracted from single documents to select the most
relevant keywords of a text.
"""
# pylint: skip-file

from .core.yake import KeywordExtractor
from .data.composed_word import ComposedWord
from .data.core import DataCore
from .data.features import (
    calculate_composed_features,
    calculate_term_features,
    get_feature_aggregation,
)
from .data.single_word import SingleWord
from .data.utils import pre_filter

# Version information
__version__ = "0.7.1"
__author__ = "INESCTEC"

# Default maximum n-gram size
MAX_NGRAM_SIZE = 3

# Public API (following reference implementation)
__all__ = [
    "KeywordExtractor",
    "DataCore",
    "SingleWord",
    "ComposedWord",
    "calculate_term_features",
    "calculate_composed_features",
    "get_feature_aggregation",
    "pre_filter",
    "MAX_NGRAM_SIZE",
]
