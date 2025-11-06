"""
YAKE (Yet Another Keyword Extractor)
====================================

A light-weight unsupervised automatic keyword extraction method which rests on
text statistical features extracted from single documents to select the most
relevant keywords of a text.
"""
# pylint: skip-file

# Import the main KeywordExtractor class
from .core.yake import KeywordExtractor

# Import data structures (following reference implementation pattern)
from .data.core import DataCore
from .data.single_word import SingleWord
from .data.composed_word import ComposedWord

# Import feature calculation functions (modular approach from reference)
from .data.features import (
    calculate_term_features,
    calculate_composed_features,
    get_feature_aggregation
)

# Import utilities
from .data.utils import pre_filter

# Version information
__version__ = "0.7.1"
__author__ = "LIAAD"

# Default maximum n-gram size
MAX_NGRAM_SIZE = 3

# Public API (following reference implementation)
__all__ = [
    'KeywordExtractor',
    'DataCore',
    'SingleWord',
    'ComposedWord',
    'calculate_term_features',
    'calculate_composed_features',
    'get_feature_aggregation',
    'pre_filter',
    'MAX_NGRAM_SIZE',
]