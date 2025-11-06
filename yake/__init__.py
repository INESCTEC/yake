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

# Version information
__version__ = "0.7.1"
__author__ = "LIAAD"

# Default maximum n-gram size
MAX_NGRAM_SIZE = 3

# Make the main class available at package level
__all__ = ['KeywordExtractor', 'MAX_NGRAM_SIZE']