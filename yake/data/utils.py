"""
Text processing utility module for YAKE keyword extraction.

This module provides essential text preprocessing functions for the YAKE algorithm,
including text normalization, sentence segmentation, tokenization, and word
categorization. These utilities form the foundation for clean and consistent
text analysis throughout the keyword extraction pipeline.
"""

import re
from functools import lru_cache
from segtok.segmenter import split_multi  # pylint: disable=import-error
from segtok.tokenizer import web_tokenizer, split_contractions  # pylint: disable=import-error

# Pre-compiled regex patterns for better performance
_CAPITAL_LETTER_PATTERN = re.compile(r"^(\s*([A-Z]))")

# Stopword weighting method for multi-word term scoring:
# - "bi": Use bi-directional weighting (default, considers term connections)
# - "h": Use direct term scores (treat stopwords like normal words)
# - "none": Ignore stopwords completely
STOPWORD_WEIGHT = "bi"


def pre_filter(text: str) -> str:
    """Pre-filter text before processing.

    This function prepares raw text for keyword extraction by normalizing its format.
    It performs several transformations:

    1. Splits the text into parts based on newline characters
    2. Detects if a part starts with a capital letter (potentially a new paragraph)
    3. Adds appropriate spacing between parts:
       - Double newlines for parts starting with capital letters (likely new paragraphs)
       - Single spaces for other parts (likely continuing text)
    4. Replaces all tab characters with spaces for consistent formatting

    This preprocessing helps maintain paragraph structure while normalizing
    whitespace, which improves the accuracy of subsequent text analysis steps
    like sentence boundary detection and keyword extraction.

    Args:
        text: Raw input text to be pre-filtered

    Returns:
        Normalized text with consistent spacing and paragraph structure
    """
    # Split the text into lines
    parts = text.split("\n")
    buffer = ""

    # Process each line
    for part in parts:
        # Determine separator: preserve paragraph breaks for lines starting with capital letters
        sep = " "
        if _CAPITAL_LETTER_PATTERN.match(part):
            sep = "\n\n"

        # Append the processed line to the buffer, replacing tabs with spaces
        buffer += sep + part.replace("\t", " ")

    return buffer


def tokenize_sentences(text: str) -> list:
    """
    Split text into sentences and tokenize into words.

    Performs two-level tokenization: dividing text into sentences,
    then tokenizing each sentence into individual words.

    Args:
        text: The input text to be tokenized

    Returns:
        A nested list where each inner list contains tokens for one sentence
    """
    return [
        # Inner list: tokenize each sentence into words
        [
            w  # Keep only valid word tokens
            for w in split_contractions(web_tokenizer(s))
            # Filter out standalone apostrophes and empty tokens
            if not (w.startswith("'") and len(w) > 1) and len(w) > 0
        ]
        # Outer list: iterate through sentences
        for s in list(split_multi(text))
        # Skip empty sentences
        if len(s.strip()) > 0
    ]


@lru_cache(maxsize=10000)
def get_tag(word: str, i: int, exclude: frozenset) -> str:
    """
    Determine the linguistic tag of a word.

    Categorizes words based on orthographic features (capitalization, digits,
    special characters) to identify proper nouns, acronyms, numbers, and
    unusual patterns.

    Args:
        word: The word to classify
        i: Position of the word within its sentence (0 = first word)
        exclude: Frozenset of characters to consider as punctuation/special chars

    Returns:
        A single character tag:
            - "d": Digit or numeric value
            - "u": Unusual word (mixed alphanumeric or special characters)
            - "a": Acronym (all uppercase)
            - "n": Proper noun (capitalized, not at start of sentence)
            - "p": Plain word (default)
    """
    # Check if word is numeric (with possible commas and a decimal point)
    if (
        word.replace(",", "").isdigit()
        or word.replace(",", "").replace(".", "", 1).isdigit()
    ):
        return "d"

    # Count character types for classification
    # Optimized: single pass through word instead of multiple
    cdigit = calpha = cexclude = 0
    for c in word:
        if c.isdigit():
            cdigit += 1
        if c.isalpha():
            calpha += 1
        if c in exclude:
            cexclude += 1

    # Classify unusual tokens: mixed alphanumeric, special chars, or multiple punctuation
    if (cdigit > 0 and calpha > 0) or (cdigit == 0 and calpha == 0) or cexclude > 1:
        return "u"

    # Identify acronyms (all uppercase words)
    if word.isupper() and len(word) > 0:
        return "a"

    # Identify proper nouns (capitalized words not at sentence beginning)
    if len(word) > 1 and word[0].isupper() and i > 0:
        # Check that only the first letter is uppercase (not an all-caps word)
        if sum(c.isupper() for c in word) == 1:
            return "n"

    # Default case: plain word
    return "p"
