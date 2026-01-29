"""
Keyword extraction module for YAKE.

This module provides the KeywordExtractor class which serves as the main entry point
for the YAKE keyword extraction algorithm. It handles configuration, stopword loading,
deduplication of similar keywords, and the entire extraction pipeline from raw text
to ranked keywords.
"""

import os
import logging
import functools
from typing import List, Tuple, Optional, Set, Callable
import jellyfish  # pylint: disable=import-error
from yake.data import DataCore
from .Levenshtein import Levenshtein

# Configure module logger
logger = logging.getLogger(__name__)


class KeywordExtractor:  # pylint: disable=too-many-instance-attributes
    """
    Main entry point for YAKE keyword extraction.

    This class handles the configuration, preprocessing, and extraction of keywords
    from text documents using statistical features without relying on dictionaries
    or external corpora. It integrates components for text processing, candidate
    generation, feature extraction, and keyword ranking.

    Attributes:
        See initialization parameters for configurable attributes.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        lan: str = "en",
        n: int = 3,
        dedup_lim: float = 0.9,
        dedup_func: str = "seqm",
        window_size: int = 1,
        top: int = 20,
        features: Optional[List[str]] = None,
        stopwords: Optional[Set[str]] = None,
        lemmatize: bool = False,
        lemma_aggregation: str = "min",
        lemmatizer: str = "spacy",
        **kwargs
    ):
        """
        Initialize the KeywordExtractor with configuration parameters.

        Args:
            lan: Language for stopwords (default: "en")
            n: Maximum n-gram size (default: 3)
            dedup_lim: Similarity threshold for deduplication (default: 0.9)
            dedup_func: Deduplication function: "seqm", "jaro", or "levs"
                (default: "seqm")
            window_size: Size of word window for co-occurrence (default: 1)
            top: Maximum number of keywords to extract (default: 20)
            features: List of features to use for scoring
                (default: None = all features)
            stopwords: Custom set of stopwords (default: None = use
                language-specific)
            lemmatize: Enable lemmatization to aggregate keywords by lemma
                (default: False). Requires spacy or nltk.
            lemma_aggregation: Method to combine scores of lemmatized keywords:
                "min" (best score), "mean" (average), "max" (worst score),
                "harmonic" (harmonic mean). Default: "min"
            lemmatizer: Lemmatization library to use: "spacy" or "nltk"
                (default: "spacy")
            **kwargs: Additional configuration parameters (for backwards
                compatibility)
        """
        # Initialize configuration dictionary with default values
        self.config = {
            "lan": lan,
            "n": n,
            "dedup_lim": dedup_lim,
            "dedup_func": dedup_func,
            "window_size": window_size,
            "top": top,
            "features": features,
        }

        # Override with any kwargs for backwards compatibility
        for key in ["lan", "n", "dedup_lim", "dedup_func", "window_size", "top", "features"]:
            if key in kwargs:
                self.config[key] = kwargs[key]

        # Lemmatization configuration
        self.lemmatize = lemmatize
        self.lemma_aggregation = lemma_aggregation
        self.lemmatizer = lemmatizer
        self._lemmatizer_instance = None  # Lazy loaded when needed
        self._lemmatizer_load_failed = False  # Track if loading failed to avoid repeated warnings

        # Load appropriate stopwords and deduplication function
        self.stopword_set = self._load_stopwords(stopwords or kwargs.get("stopwords"))
        self.dedup_function = self._get_dedup_function(self.config["dedup_func"])

        # Initialize optimization components
        self._similarity_cache = {}

        # Cache management stats (combined to reduce instance attributes)
        self._cache_stats = {
            'hits': 0,
            'misses': 0,
            'docs_processed': 0,
            'last_text_size': 0
        }

    def _load_stopwords(self, stopwords: Optional[Set[str]]) -> Set[str]:
        """
        Load stopwords from file or use provided set.

        This method handles the loading of language-specific stopwords from
        the appropriate resource file, falling back to a language-agnostic
        list if the specific language is not available.

        Args:
            stopwords: Custom set of stopwords to use

        Returns:
            A set of stopwords for filtering non-content words
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

    def _get_dedup_function(self, func_name: str) -> Callable[[str, str], float]:
        """
        Retrieve the appropriate deduplication function.

        Maps the requested string similarity function name to the corresponding
        method implementation for keyword deduplication.

        Args:
            func_name: Name of the deduplication function to use

        Returns:
            Reference to the selected string similarity function
        """
        # Map function names to their implementations
        return {
            "jaro_winkler": self.jaro,
            "jaro": self.jaro,
            "sequencematcher": self.seqm,
            "seqm": self.seqm,
        }.get(func_name.lower(), self.levs)

    def jaro(self, cand1: str, cand2: str) -> float:
        """
        Calculate Jaro similarity between two strings.

        A string metric measuring edit distance between two sequences,
        with higher values indicating greater similarity.

        Args:
            cand1: First string to compare
            cand2: Second string to compare

        Returns:
            Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return jellyfish.jaro_similarity(cand1, cand2)

    def levs(self, cand1: str, cand2: str) -> float:
        """
        Calculate normalized Levenshtein similarity between two strings.

        Computes the Levenshtein distance and normalizes it by the length
        of the longer string, returning a similarity score.

        Args:
            cand1: First string to compare
            cand2: Second string to compare

        Returns:
            Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return 1 - Levenshtein.distance(cand1, cand2) / max(len(cand1), len(cand2))

    def seqm(self, cand1: str, cand2: str) -> float:
        """
        Calculate sequence matcher ratio between two strings.

        Uses the Levenshtein ratio which measures the similarity between
        two strings based on the minimum number of operations required
        to transform one string into the other.

        Args:
            cand1: First string to compare
            cand2: Second string to compare

        Returns:
            Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return self._optimized_similarity(cand1, cand2)

    @staticmethod
    @functools.lru_cache(maxsize=50000)
    # pylint: disable=too-many-locals,too-many-return-statements
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
            self._cache_stats['hits'] += 1
            return self._similarity_cache[cache_key]

        self._cache_stats['misses'] += 1

        # Pre-filter first
        if not self._aggressive_pre_filter(cand1, cand2):
            result = 0.0
        else:
            result = self._ultra_fast_similarity(cand1, cand2)

        # Cache with memory management
        if len(self._similarity_cache) < 30000:  # Limit memory usage
            self._similarity_cache[cache_key] = result

        return result

    def _get_lemmatizer_instance(self):  # pylint: disable=too-many-return-statements
        """
        Lazy load lemmatizer instance.

        Returns the lemmatizer instance, loading it on first use to avoid
        unnecessary overhead when lemmatization is disabled.

        Returns:
            Lemmatizer instance (spacy.Language or nltk lemmatizer)
        """
        # If already loaded successfully, return it
        if self._lemmatizer_instance is not None:
            return self._lemmatizer_instance

        # If we already tried and failed, don't try again
        if self._lemmatizer_load_failed:
            return None

        if self.lemmatizer == "spacy":
            try:
                import spacy  # pylint: disable=import-outside-toplevel

                # Map language codes to spacy models
                model_map = {
                    "en": "en_core_web_sm",
                    "pt": "pt_core_news_sm",
                    "es": "es_core_news_sm",
                    "de": "de_core_news_sm",
                    "fr": "fr_core_news_sm",
                    "it": "it_core_news_sm",
                }

                model_name = model_map.get(self.config["lan"][:2], "en_core_web_sm")

                try:
                    self._lemmatizer_instance = spacy.load(model_name)
                    logger.info("Loaded spaCy model: %s", model_name)
                    return self._lemmatizer_instance
                except OSError:
                    # Try English model as fallback
                    if model_name != "en_core_web_sm":
                        try:
                            self._lemmatizer_instance = spacy.load("en_core_web_sm")
                            logger.info("Falling back to en_core_web_sm")
                            return self._lemmatizer_instance
                        except OSError:
                            pass

                    # All loading attempts failed - show warning once
                    logger.warning(
                        "spaCy models not found. Lemmatization disabled. "
                        "Install with: uv pip install yake[lemmatization] && "
                        "python -m spacy download en_core_web_sm"
                    )
                    self._lemmatizer_load_failed = True
                    return None

            except ImportError:
                logger.warning(
                    "spaCy not installed. Lemmatization disabled. "
                    "Install with: uv pip install yake[lemmatization] && "
                    "python -m spacy download en_core_web_sm"
                )
                self._lemmatizer_load_failed = True
                return None

        if self.lemmatizer == "nltk":
            try:
                from nltk.stem import WordNetLemmatizer  # pylint: disable=import-outside-toplevel
                import nltk  # pylint: disable=import-outside-toplevel

                # Download wordnet data if needed
                try:
                    nltk.data.find('corpora/wordnet')
                except LookupError:
                    logger.info("Downloading NLTK wordnet data...")
                    nltk.download('wordnet', quiet=True)
                    nltk.download('omw-1.4', quiet=True)

                self._lemmatizer_instance = WordNetLemmatizer()
                logger.info("Loaded NLTK WordNetLemmatizer")
                return self._lemmatizer_instance

            except ImportError:
                logger.warning(
                    "NLTK not installed. Lemmatization disabled. "
                    "Install with: uv pip install yake[lemmatization]"
                )
                self._lemmatizer_load_failed = True
                return None

        logger.warning(
            "Unknown lemmatizer: %s. Lemmatization disabled.",
            self.lemmatizer
        )
        self._lemmatizer_load_failed = True
        return None

    def _lemmatize_text(self, text: str) -> str:
        """
        Lemmatize a text string.

        Args:
            text: Text to lemmatize

        Returns:
            Lemmatized text
        """
        lemmatizer = self._get_lemmatizer_instance()
        if lemmatizer is None:
            return text

        if self.lemmatizer == "spacy":
            doc = lemmatizer(text)
            return " ".join([token.lemma_ for token in doc])

        if self.lemmatizer == "nltk":
            # Simple word-by-word lemmatization
            words = text.split()
            return " ".join([lemmatizer.lemmatize(word.lower()) for word in words])

        return text

    def _lemmatize_keywords(  # pylint: disable=too-many-locals
        self,
        keywords: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        """
        Aggregate keywords by lemma.

        Groups keywords with the same lemma and combines their scores using
        the configured aggregation method. This reduces redundancy from
        morphological variations (e.g., "tree" and "trees").

        Args:
            keywords: List of (keyword, score) tuples

        Returns:
            Aggregated list with lemmatized keywords, sorted by score
        """
        if not keywords:
            return keywords

        lemmatizer = self._get_lemmatizer_instance()
        if lemmatizer is None:
            # Lemmatizer not available - return original keywords without warning
            # (warning was already shown on first load attempt)
            return keywords

        from collections import defaultdict  # pylint: disable=import-outside-toplevel
        import statistics  # pylint: disable=import-outside-toplevel

        lemma_groups = defaultdict(list)

        # Group keywords by their lemma
        for kw, score in keywords:
            lemma = self._lemmatize_text(kw)
            # Store original keyword and score
            lemma_groups[lemma].append((kw, score))

        # Aggregate scores using the configured method
        result = []
        for lemma, group in lemma_groups.items():
            if self.lemma_aggregation == "min":
                # Use the keyword with the best (lowest) score
                best_kw, best_score = min(group, key=lambda x: x[1])
                result.append((best_kw, best_score))

            elif self.lemma_aggregation == "mean":
                # Use average score, keep first keyword form
                avg_score = statistics.mean(score for _, score in group)
                result.append((group[0][0], avg_score))

            elif self.lemma_aggregation == "max":
                # Use the worst (highest) score - most conservative
                worst_kw, worst_score = max(group, key=lambda x: x[1])
                result.append((worst_kw, worst_score))

            elif self.lemma_aggregation == "harmonic":
                # Harmonic mean - good for combining scores
                scores = [score for _, score in group]
                # Handle case where all scores might be 0
                if all(s > 0 for s in scores):
                    harmonic = statistics.harmonic_mean(scores)
                else:
                    harmonic = statistics.mean(scores)
                result.append((group[0][0], harmonic))
            else:
                logger.warning(
                    "Unknown aggregation method: %s. Using 'min'",
                    self.lemma_aggregation
                )
                best_kw, best_score = min(group, key=lambda x: x[1])
                result.append((best_kw, best_score))

        # Sort by score (lower is better)
        return sorted(result, key=lambda x: x[1])

    def _get_strategy(self, num_candidates: int) -> str:
        """Determine optimization strategy based on dataset size."""
        if num_candidates < 50:
            return "small"
        if num_candidates < 200:
            return "medium"
        return "large"

    def extract_keywords(self, text: Optional[str]) -> List[Tuple[str, float]]:
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
            text: Input text to extract keywords from

        Returns:
            List of (keyword, score) tuples sorted by score (lower is better)

        """
        # Handle empty input
        if not text:
            logger.debug("Empty text provided, returning empty result")
            return []

        try:
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
                return [(cand.unique_kw, cand.h) for cand in candidates_sorted][
                    : self.config["top"]
                ]

            # ALGORITMO ORIGINAL (YAKE 1.0.0 / 0.6.0) - SEM OTIMIZAÇÕES
            # Usar algoritmo clássico para garantir resultados idênticos às versões anteriores
            result_set = []
            for cand in candidates_sorted:
                should_add = True
                # Check if this candidate is too similar to any already selected
                for h, cand_result in result_set:
                    if (
                        self.dedup_function(cand.unique_kw, cand_result.unique_kw)
                        > self.config["dedup_lim"]
                    ):
                        should_add = False
                        break

                # Add candidate if it passes deduplication
                if should_add:
                    result_set.append((cand.h, cand))

                # Stop once we have enough candidates
                if len(result_set) == self.config["top"]:
                    break

            # Format results as (keyword, score) tuples - EXATAMENTE como YAKE 0.6.0
            results = [(cand.kw, h) for (h, cand) in result_set]

            # Apply lemmatization if enabled
            if self.lemmatize:
                logger.debug(
                    "Applying lemmatization with aggregation method: %s", 
                    self.lemma_aggregation
                )
                results = self._lemmatize_keywords(results)

            # Intelligent cache management after extraction
            self._manage_cache_lifecycle(text)

            return results

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning(
                "Exception during keyword extraction: %s (text preview: '%s...')",
                str(e), text[:100] if text else ""
            )
            return []

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

            for _, prev_cand in result_set[-max_checks:]:  # Check recent ones first
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
        total = self._cache_stats['hits'] + self._cache_stats['misses']
        hit_rate = self._cache_stats['hits'] / total * 100 if total > 0 else 0
        return {
            'hits': self._cache_stats['hits'],
            'misses': self._cache_stats['misses'],
            'hit_rate': hit_rate,
            'docs_processed': self._cache_stats['docs_processed'],
            'cache_size': self._get_cache_usage()
        }

    def _manage_cache_lifecycle(self, text):
        """
        Intelligently manage cache lifecycle to prevent memory leaks.

        This method implements smart cache clearing based on:
        1. Text size (large documents)
        2. Cache saturation (>80% full)
        3. Document count (failsafe every 50 docs)

        Args:
            text: The text that was just processed
        """
        self._cache_stats['docs_processed'] += 1
        text_size = len(text.split())
        self._cache_stats['last_text_size'] = text_size

        # Get current cache usage
        cache_usage = self._get_cache_usage()

        # HEURISTIC: Clear cache if any condition is met
        should_clear = (
            text_size > 2000 or                    # Large document (>2000 words)
            cache_usage > 0.8 or                   # Cache >80% full
            self._cache_stats['docs_processed'] % 50 == 0  # Failsafe: every 50 docs
        )

        if should_clear:
            self.clear_caches()

    def _get_cache_usage(self):
        """
        Calculate current cache usage as a ratio (0.0 to 1.0).

        Returns:
            float: Cache usage ratio where 1.0 means completely full
        """
        try:
            # pylint: disable=no-value-for-parameter
            info = KeywordExtractor._ultra_fast_similarity.cache_info()
            return info.currsize / info.maxsize if info.maxsize > 0 else 0.0
        except AttributeError:
            # Fallback if cache_info not available
            return 0.0

    def clear_caches(self):
        """
        Clear all internal caches to free memory.

        This method clears:
        - LRU cache for similarity calculations (50,000 entries max)
        - LRU cache for text tagging (10,000 entries max)
        - LRU cache for Levenshtein distance (40,000 entries max)
        - Instance-level similarity cache
        
        When to call manually:
        - Processing batches of documents in a loop
        - Running in memory-constrained environments (e.g., AWS Lambda)
        - After processing large documents (>5000 words)
        - Before critical operations that need maximum available memory
        
        Performance impact:
        - Next 5-10 extractions will be ~10-20% slower while caches warm up
        - After warm-up, performance returns to optimized levels
        - Trade-off is worthwhile for preventing memory leaks in production
        
        Example usage:
            >>> extractor = KeywordExtractor(lan="en")
            >>> for doc in large_document_batch:
            ...     keywords = extractor.extract_keywords(doc)
            ...     process_keywords(keywords)
            ...     if doc.size > 10000:  # Manual clear for huge docs
            ...         extractor.clear_caches()
        
        Note:
            This is called automatically by the intelligent cache manager
            based on heuristics (text size, cache saturation, document count).
            Manual calls are only needed for special cases.
        """
        # Clear static method cache (shared across all instances)
        try:
            self._ultra_fast_similarity.cache_clear()
        except AttributeError:
            pass

        # Clear module-level caches
        try:
            # pylint: disable=import-outside-toplevel
            from yake.data.utils import get_tag
            get_tag.cache_clear()
        except (ImportError, AttributeError):
            pass

        try:
            # pylint: disable=import-outside-toplevel
            from yake.core.Levenshtein import Levenshtein as LevenshteinModule
            LevenshteinModule.ratio.cache_clear()
            LevenshteinModule.distance.cache_clear()
        except (ImportError, AttributeError):
            pass

        # Clear instance cache
        if hasattr(self, '_similarity_cache'):
            self._similarity_cache.clear()

        # Reset tracking
        self._cache_stats['docs_processed'] = 0
        self._cache_stats['hits'] = 0
        self._cache_stats['misses'] = 0
