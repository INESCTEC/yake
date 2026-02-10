"""
Module providing optimized Levenshtein distance and ratio calculations.

This module implements an optimized version of the Levenshtein (edit distance)
algorithm for measuring the difference between two strings. It provides both
a raw distance calculation and a normalized similarity ratio, which are useful
for comparing text strings and identifying potential matches with slight variations.

Optimizations include:
- Memory-efficient two-row approach instead of full matrix
- Early termination for highly dissimilar strings
- LRU caching for repeated calculations
- Optimized algorithms for short strings
"""

import functools


class Levenshtein:
    """
    Optimized class for computing Levenshtein distance and similarity ratio.

    This class provides static methods to calculate the edit distance between
    strings (how many insertions, deletions, or substitutions are needed to
    transform one string into another) and to determine a normalized similarity
    ratio between them, with significant performance optimizations.

    These metrics are widely used in fuzzy string matching, spell checking,
    and approximate text similarity measurements.
    """

    @staticmethod
    def __ratio(distance: float, str_length: int) -> float:
        """
        Calculate the similarity ratio based on distance and string length.

        This method normalizes the Levenshtein distance into a similarity ratio
        between 0 and 1, where 1 represents identical strings and 0 represents
        completely different strings.

        Args:
            distance (float): The Levenshtein distance between two strings.
            str_length (int): The length of the longer string.

        Returns:
            float: The similarity ratio, where higher values indicate greater similarity.
                  The range is [0.0, 1.0] where 1.0 means identical strings.
        """
        return 1 - float(distance) / float(str_length) if str_length > 0 else 1.0

    @staticmethod
    @functools.lru_cache(maxsize=20000)
    def ratio(seq1: str, seq2: str) -> float:
        """
        Compute the similarity ratio between two strings with caching.

        This is the main method for determining string similarity. It calculates
        the Levenshtein distance and then converts it to a ratio representing
        how similar the strings are. Results are cached for performance.

        Args:
            seq1 (str): The first string to compare.
            seq2 (str): The second string to compare.

        Returns:
            float: The similarity ratio between the two strings, ranging from 0.0
                  (completely different) to 1.0 (identical).
        """
        str_distance = Levenshtein.distance(seq1, seq2)
        str_length = max(len(seq1), len(seq2))
        return Levenshtein.__ratio(str_distance, str_length)

    @staticmethod
    @functools.lru_cache(maxsize=20000)
    def distance(seq1: str, seq2: str) -> int:
        """
        Calculate the optimized Levenshtein distance between two strings.

        This method implements an optimized Levenshtein algorithm with:
        - Early termination for very different strings
        - Memory-efficient two-row approach
        - Special handling for short strings
        - Result caching

        Args:
            seq1 (str): The first string to compare.
            seq2 (str): The second string to compare.

        Returns:
            int: The Levenshtein distance - the minimum number of edit operations
                 required to transform seq1 into seq2.
        """
        len1, len2 = len(seq1), len(seq2)

        # Handle empty strings
        if len1 == 0:
            return len2
        if len2 == 0:
            return len1

        # Early termination: if difference in length is too large
        if abs(len1 - len2) > max(len1, len2) * 0.7:
            return max(len1, len2)

        # Ensure seq1 is the shorter string for memory efficiency
        if len1 > len2:
            seq1, seq2 = seq2, seq1
            len1, len2 = len2, len1

        # For very short strings, use simple recursive approach
        if len1 <= 3:
            return Levenshtein._simple_distance(seq1, seq2)

        previous_row = list(range(len2 + 1))
        current_row = [0] * (len2 + 1)

        for i in range(1, len1 + 1):
            current_row[0] = i
            for j in range(1, len2 + 1):
                cost = 0 if seq1[i - 1] == seq2[j - 1] else 1
                current_row[j] = min(
                    current_row[j - 1] + 1,  # insertion
                    previous_row[j] + 1,  # deletion
                    previous_row[j - 1] + cost,  # substitution
                )
            previous_row, current_row = current_row, previous_row

        return previous_row[len2]

    @staticmethod
    def _simple_distance(seq1: str, seq2: str) -> int:
        """
        Simple recursive distance calculation for very short strings.

        More efficient than the matrix approach for strings with length <= 3.
        """
        if not seq1:
            return len(seq2)
        if not seq2:
            return len(seq1)

        if seq1[0] == seq2[0]:
            return Levenshtein._simple_distance(seq1[1:], seq2[1:])

        return (
            1
            + min(
                Levenshtein._simple_distance(seq1[1:], seq2),  # deletion
                Levenshtein._simple_distance(seq1, seq2[1:]),  # insertion
                Levenshtein._simple_distance(seq1[1:], seq2[1:]),  # substitution
            )
        )
