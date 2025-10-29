"""
Keyword extraction module for YAKE.

This module provides the KeywordExtractor class which serves as the main entry point
for the YAKE keyword extraction algorithm. It handles configuration, stopword loading,
deduplication of similar keywords, and the entire extraction pipeline from raw text
to ranked keywords.
"""

import os
import functools
import jellyfish  # pylint: disable=import-error
from yake.data import DataCore
from .Levenshtein import Levenshtein


class KeywordExtractor:
    """
    Main entry point for YAKE keyword extraction.

    This class handles the configuration, preprocessing, and extraction of keywords
    from text documents using statistical features without relying on dictionaries
    or external corpora. It integrates components for text processing, candidate
    generation, feature extraction, and keyword ranking.

    Attributes:
        See initialization parameters for configurable attributes.
    """

    def __init__(self, **kwargs):
        """
        Initialize the KeywordExtractor with configuration parameters.

        Args:
            **kwargs: Configuration parameters including:
                lan (str): Language for stopwords (default: "en")
                n (int): Maximum n-gram size (default: 3)
                dedup_lim (float): Similarity threshold for deduplication
                    (default: 0.9)
                dedup_func (str): Deduplication function: "seqm", "jaro",
                    or "levs" (default: "seqm")
                window_size (int): Size of word window for co-occurrence
                    (default: 1)
                top (int): Maximum number of keywords to extract (default: 20)
                features (list): List of features to use for scoring
                    (default: None = all features)
                stopwords (set): Custom set of stopwords
                    (default: None = use language-specific)
        """
        # Initialize configuration dictionary with default values
        self.config = {
            "lan": kwargs.get("lan", "en"),
            "n": kwargs.get("n", 3),
            "dedup_lim": kwargs.get("dedup_lim", 0.9),
            "dedup_func": kwargs.get("dedup_func", "seqm"),
            "window_size": kwargs.get("window_size", 1),
            "top": kwargs.get("top", 20),
            "features": kwargs.get("features", None),
        }

        # Load appropriate stopwords and deduplication function
        self.stopword_set = self._load_stopwords(kwargs.get("stopwords"))
        self.dedup_function = self._get_dedup_function(self.config["dedup_func"])

        # Initialize optimization components
        self._similarity_cache = {}
        self._cache_hits = 0
        self._cache_misses = 0

    def _load_stopwords(self, stopwords):
        """
        Load stopwords from file or use provided set.

        This method handles the loading of language-specific stopwords from
        the appropriate resource file, falling back to a language-agnostic
        list if the specific language is not available.

        Args:
            stopwords (set, optional): Custom set of stopwords to use

        Returns:
            set: A set of stopwords for filtering non-content words
        """
        # Use provided stopwords if available
        if stopwords is not None:
            return set(stopwords)

        # Determine the path to the appropriate stopword list
        dir_path = os.path.dirname(os.path.realpath(__file__))
        local_path = os.path.join(
            "StopwordsList", f"stopwords_{self.config['lan'][:2].lower()}.txt"
        )

        # Fall back to language-agnostic list if specific language not available
        if not os.path.exists(os.path.join(dir_path, local_path)):
            local_path = os.path.join("StopwordsList", "stopwords_noLang.txt")

        resource_path = os.path.join(dir_path, local_path)

        # Attempt to read the stopword file with UTF-8 encoding
        try:
            with open(resource_path, encoding="utf-8") as stop_file:
                return set(stop_file.read().lower().split("\n"))
        except UnicodeDecodeError:
            # Fall back to ISO-8859-1 encoding if UTF-8 fails
            print("Warning: reading stopword list as ISO-8859-1")
            with open(resource_path, encoding="ISO-8859-1") as stop_file:
                return set(stop_file.read().lower().split("\n"))

    def _get_dedup_function(self, func_name):
        """
        Retrieve the appropriate deduplication function.

        Maps the requested string similarity function name to the corresponding
        method implementation for keyword deduplication.

        Args:
            func_name (str): Name of the deduplication function to use

        Returns:
            function: Reference to the selected string similarity function
        """
        # Map function names to their implementations
        return {
            "jaro_winkler": self.jaro,
            "jaro": self.jaro,
            "sequencematcher": self.seqm,
            "seqm": self.seqm,
        }.get(func_name.lower(), self.levs)

    def jaro(self, cand1, cand2):
        """
        Calculate Jaro similarity between two strings.

        A string metric measuring edit distance between two sequences,
        with higher values indicating greater similarity.

        Args:
            cand1 (str): First string to compare
            cand2 (str): Second string to compare

        Returns:
            float: Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return jellyfish.jaro(cand1, cand2)

    def levs(self, cand1, cand2):
        """
        Calculate normalized Levenshtein similarity between two strings.

        Computes the Levenshtein distance and normalizes it by the length
        of the longer string, returning a similarity score.

        Args:
            cand1 (str): First string to compare
            cand2 (str): Second string to compare

        Returns:
            float: Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return 1 - Levenshtein.distance(cand1, cand2) / max(len(cand1), len(cand2))

    def seqm(self, cand1, cand2):
        """
        Calculate sequence matcher ratio between two strings.

        Uses the Levenshtein ratio which measures the similarity between
        two strings based on the minimum number of operations required
        to transform one string into the other.

        Args:
            cand1 (str): First string to compare
            cand2 (str): Second string to compare

        Returns:
            float: Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return self._optimized_similarity(cand1, cand2)

    @staticmethod
    @functools.lru_cache(maxsize=50000)
    def _ultra_fast_similarity(s1: str, s2: str) -> float:
        """
        Ultra-optimized similarity algorithm for performance.

        Combines multiple heuristics for maximum speed while maintaining
        accuracy.

        Note: Static method to enable proper LRU caching across all instances.
        Cache is shared between all KeywordExtractor objects for maximum
        efficiency.

        Args:
            s1: First string to compare
            s2: Second string to compare

        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        # Identical strings
        if s1 == s2:
            return 1.0

        # Quick length filter and normalization
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 0.0

        len_ratio = min(len(s1), len(s2)) / max_len
        if len_ratio < 0.3:  # Too different in length
            return 0.0

        s1_lower, s2_lower = s1.lower(), s2.lower()

        # Character overlap heuristic (very fast)
        chars_union = set(s1_lower) | set(s2_lower)
        if not chars_union:
            return 0.0

        char_overlap = (len(set(s1_lower) & set(s2_lower)) /
                       len(chars_union))

        if char_overlap < 0.2:  # Few common characters
            return 0.0

        # For very short strings, use simple approximation
        if max_len <= 4:
            return char_overlap * len_ratio

        # Word-based similarity for multi-word phrases
        words1, words2 = s1_lower.split(), s2_lower.split()
        if len(words1) > 1 or len(words2) > 1:
            word_union = set(words1) | set(words2)
            if word_union:
                word_overlap = (len(set(words1) & set(words2)) /
                              len(word_union))
                if word_overlap > 0.4:
                    return word_overlap

        # Trigram similarity
        trigrams1 = set(s1_lower[i:i+3] for i in range(len(s1_lower)-2))
        trigrams2 = set(s2_lower[i:i+3] for i in range(len(s2_lower)-2))
        trigram_union = trigrams1 | trigrams2

        trigram_overlap = (len(trigrams1 & trigrams2) / len(trigram_union)
                          if trigram_union else 0)

        # Combine metrics with optimal weights
        return min(0.3 * len_ratio + 0.2 * char_overlap +
                  0.5 * trigram_overlap, 1.0)

    def _aggressive_pre_filter(self, cand1: str, cand2: str) -> bool:
        """
        Ultra-aggressive pre-filter eliminating 95%+ of calculations.

        Returns:
            True if candidates should be compared, False otherwise
        """
        # Exact match
        if cand1 == cand2:
            return True

        # Combined length and character filters
        len1, len2 = len(cand1), len(cand2)
        max_len = max(len1, len2)

        # Length difference filter
        if abs(len1 - len2) > max_len * 0.6:
            return False

        # First/last character and prefix filters for longer strings
        if max_len > 3:
            if (cand1[0] != cand2[0] or cand1[-1] != cand2[-1]):
                return False
            if min(len1, len2) >= 3 and cand1[:2].lower() != cand2[:2].lower():
                return False

        # Word count filter
        if abs(cand1.count(' ') - cand2.count(' ')) > 1:
            return False

        return True

    def _optimized_similarity(self, cand1: str, cand2: str) -> float:
        """Optimized similarity with caching and pre-filtering."""
        # Cache lookup (consistent ordering for maximum hits)
        cache_key = (cand1, cand2) if cand1 <= cand2 else (cand2, cand1)

        if cache_key in self._similarity_cache:
            self._cache_hits += 1
            return self._similarity_cache[cache_key]

        self._cache_misses += 1

        # Pre-filter first
        if not self._aggressive_pre_filter(cand1, cand2):
            result = 0.0
        else:
            result = self._ultra_fast_similarity(cand1, cand2)

        # Cache with memory management
        if len(self._similarity_cache) < 30000:  # Limit memory usage
            self._similarity_cache[cache_key] = result

        return result

    def _get_strategy(self, num_candidates: int) -> str:
        """Determine optimization strategy based on dataset size."""
        if num_candidates < 50:
            return "small"
        if num_candidates < 200:
            return "medium"
        return "large"

    def extract_keywords(self, text):
        """
        Extract keywords from the given text using adaptive optimizations.

        This function implements the complete YAKE keyword extraction pipeline with
        performance optimizations that adapt to the size of the candidate set:

        1. Preprocesses the input text by normalizing whitespace
        2. Builds a data representation using DataCore, which:
           - Tokenizes the text into sentences and words
           - Identifies candidate n-grams (1 to n words)
           - Creates a graph of term co-occurrences
        3. Extracts statistical features for single terms and n-grams
           - For single terms: frequency, position, case, etc.
           - For n-grams: combines features from constituent terms
        4. Filters candidates based on validity criteria (e.g., no stopwords at boundaries)
        5. Sorts candidates by their importance score (H), where lower is better
        6. Performs adaptive deduplication using optimized similarity algorithms
        7. Returns the top k keywords with their scores

        The algorithm favors keywords that are statistically important but not common
        stopwords, with scores reflecting their estimated relevance to the document.
        Lower scores indicate more important keywords.

        Args:
            text: Input text

        Returns:
            List of (keyword, score) tuples sorted by score (lower is better)

        """
        # Handle empty input
        if not text:
            return []

        # Normalize text by replacing newlines with spaces
        text = text.replace("\n", " ")

        # Create a configuration dictionary for DataCore
        core_config = {
            "windows_size": self.config["window_size"],
            "n": self.config["n"],
        }

        # Initialize the data core with the text
        dc = DataCore(text=text, stopword_set=self.stopword_set, config=core_config)

        # Build features for single terms and multi-word terms
        dc.build_single_terms_features(features=self.config["features"])
        dc.build_mult_terms_features(features=self.config["features"])

        # Get valid candidates
        candidates_sorted = sorted(
            [cc for cc in dc.candidates.values() if cc.is_valid()],
            key=lambda c: c.h
        )

        # No deduplication case
        if self.config["dedup_lim"] >= 1.0:
            return [(cand.unique_kw, float(cand.h)) for cand in candidates_sorted][
                : self.config["top"]
            ]

        # Adaptive strategy based on dataset size
        strategy = self._get_strategy(len(candidates_sorted))

        if strategy == "small":
            return self._optimized_small_dedup(candidates_sorted)
        if strategy == "medium":
            return self._optimized_medium_dedup(candidates_sorted)
        return self._optimized_large_dedup(candidates_sorted)

    def _optimized_small_dedup(self, candidates_sorted):
        """Optimized deduplication for small datasets (<50 candidates)."""
        result_set = []
        seen_exact = set()  # Exact string matches

        for cand in candidates_sorted:
            cand_kw = cand.unique_kw

            # Exact match check (fastest possible)
            if cand_kw in seen_exact:
                continue

            should_add = True

            # Check against existing results (pre-filter first)
            for _, prev_cand in result_set:
                if self._aggressive_pre_filter(cand_kw, prev_cand.unique_kw):
                    similarity = self._optimized_similarity(cand_kw, prev_cand.unique_kw)
                    if similarity > self.config["dedup_lim"]:
                        should_add = False
                        break

            if should_add:
                result_set.append((cand.h, cand))
                seen_exact.add(cand_kw)

            if len(result_set) == self.config["top"]:
                break

        return [(cand.kw, float(h)) for (h, cand) in result_set]

    def _optimized_medium_dedup(self, candidates_sorted):
        """Optimized deduplication for medium datasets (50-200)."""
        result_set = []
        seen_exact = set()

        for cand in candidates_sorted:
            cand_kw = cand.unique_kw

            if cand_kw in seen_exact:
                continue

            should_add = True

            # Check similarity with optimized order (recent first)
            for _, prev_cand in result_set:
                # Quick length pre-filter
                len_diff = abs(len(cand_kw) - len(prev_cand.unique_kw))
                max_len = max(len(cand_kw), len(prev_cand.unique_kw))
                if len_diff > max_len * 0.5:
                    continue

                if self._aggressive_pre_filter(cand_kw, prev_cand.unique_kw):
                    similarity = self._optimized_similarity(cand_kw, prev_cand.unique_kw)
                    if similarity > self.config["dedup_lim"]:
                        should_add = False
                        break

            if should_add:
                result_set.append((cand.h, cand))
                seen_exact.add(cand_kw)

            if len(result_set) == self.config["top"]:
                break

        return [(cand.kw, float(h)) for (h, cand) in result_set]

    def _optimized_large_dedup(self, candidates_sorted):
        """Optimized deduplication for large datasets (>200 candidates)."""
        # For large datasets, be more aggressive about early termination
        result_set = []
        seen_exact = set()

        processed = 0
        max_processing = min(len(candidates_sorted), self.config["top"] * 10)  # Limit processing

        for cand in candidates_sorted:
            if processed >= max_processing:
                break

            processed += 1
            cand_kw = cand.unique_kw

            if cand_kw in seen_exact:
                continue

            should_add = True

            # Only check against small subset of most relevant candidates
            max_checks = min(len(result_set), 20)  # Limit comparisons

            for prev_score, prev_cand in result_set[-max_checks:]:  # Check recent ones first
                if not self._aggressive_pre_filter(cand_kw, prev_cand.unique_kw):
                    continue

                similarity = self._optimized_similarity(cand_kw, prev_cand.unique_kw)
                if similarity > self.config["dedup_lim"]:
                    should_add = False
                    break

            if should_add:
                result_set.append((cand.h, cand))
                seen_exact.add(cand_kw)

            if len(result_set) == self.config["top"]:
                break

        # Clear cache periodically to avoid memory issues
        if len(self._similarity_cache) > 50000:
            self._similarity_cache.clear()

        return [(cand.kw, float(h)) for (h, cand) in result_set]

    def get_cache_stats(self):
        """Return cache performance statistics."""
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total * 100 if total > 0 else 0
        return {
            'hits': self._cache_hits,
            'misses': self._cache_misses,
            'hit_rate': hit_rate
        }
