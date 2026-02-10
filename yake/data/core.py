"""
Core data representation module for YAKE keyword extraction.

This module contains the DataCore class which serves as the foundation for
processing and analyzing text documents to extract keywords. It handles text
preprocessing, term identification, co-occurrence analysis, and candidate
keyword generation.
"""

import logging
import string
from typing import Any

import networkx as nx  # pylint: disable=import-error
import numpy as np  # pylint: disable=import-error
from segtok.tokenizer import split_contractions, web_tokenizer  # pylint: disable=import-error

from .composed_word import ComposedWord
from .single_word import SingleWord
from .utils import get_tag, pre_filter, tokenize_sentences

# Configure module logger
logger = logging.getLogger(__name__)


class DataCore:
    """
    Core data representation for document analysis and keyword extraction.

    This class processes text documents to identify potential keywords based on
    statistical features and contextual relationships between terms. It maintains
    the document's structure, processes individual terms, and generates candidate
    keywords.

    Attributes:
        See property accessors below for available attributes.
    """

    def __init__(
        self,
        text: str,
        stopword_set: set[str],
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize the data core for keyword extraction.

        Args:
            text: Input text to process
            stopword_set: Set of stopwords to ignore
            config: Configuration options including:
                - windows_size (int): Size of window for co-occurrence matrix (default: 2)
                - n (int): Maximum n-gram size (default: 3)
                - tags_to_discard (set): Tags to discard during processing (default: {"u", "d"})
                - exclude (set): Set of characters to exclude (default: string.punctuation)
        """
        # Initialize default configuration if none provided
        if config is None:
            config = {}

        # Extract configuration values with appropriate defaults
        windows_size = config.get("windows_size", 2)
        n = config.get("n", 3)
        tags_to_discard = config.get("tags_to_discard", set(["u", "d"]))
        exclude = config.get("exclude", set(string.punctuation))

        # Convert exclude to frozenset once for efficient caching in get_tag()
        exclude = frozenset(exclude)

        # Initialize the state dictionary containing all component data structures
        self._state = {
            # Configuration settings
            "config": {
                "exclude": exclude,  # Punctuation and other characters to exclude (as frozenset)
                "tags_to_discard": tags_to_discard,  # POS tags to ignore during analysis
                "stopword_set": stopword_set,  # Set of stopwords for filtering
            },
            # Text corpus statistics
            "text_stats": {
                "number_of_sentences": 0,  # Total count of sentences
                "number_of_words": 0,  # Total count of processed words
            },
            # Core data collections for analysis
            "collections": {
                "terms": {},  # Dictionary mapping terms to SingleWord objects
                "candidates": {},  # Dictionary mapping unique keywords to ComposedWord objects
                "sentences_obj": [],  # Nested list of processed sentence objects
                "sentences_str": [],  # List of raw sentence strings
                "freq_ns": {},  # Frequency distribution of n-grams by length
            },
            # Graph for term co-occurrence analysis
            # Directed graph where nodes are terms and edges represent
            # co-occurrences
            "g": nx.DiGraph(),
        }

        # Initialize n-gram frequencies with zero counts for each length 1 to n
        for i in range(n):
            self._state["collections"]["freq_ns"][i + 1] = 0.0

        # Process the text and build all data structures
        self._build(text, windows_size, n)

    # --- Property accessors for backward compatibility ---

    # Configuration properties
    @property
    def exclude(self):
        """Get the set of characters to exclude from processing."""
        return self._state["config"]["exclude"]

    @property
    def tags_to_discard(self):
        """Get the set of part-of-speech tags to ignore during analysis."""
        return self._state["config"]["tags_to_discard"]

    @property
    def stopword_set(self):
        """Get the set of stopwords used for filtering."""
        return self._state["config"]["stopword_set"]

    @property
    def g(self):
        """Get the directed graph representing term co-occurrences."""
        return self._state["g"]

    # Text statistics properties
    @property
    def number_of_sentences(self):
        """Get the total number of sentences in the document."""
        return self._state["text_stats"]["number_of_sentences"]

    @number_of_sentences.setter
    def number_of_sentences(self, value):
        """Set the total number of sentences in the document."""
        self._state["text_stats"]["number_of_sentences"] = value

    @property
    def number_of_words(self):
        """Get the total number of words processed in the document."""
        return self._state["text_stats"]["number_of_words"]

    @number_of_words.setter
    def number_of_words(self, value):
        """Set the total number of words processed in the document."""
        self._state["text_stats"]["number_of_words"] = value

    # Collection properties
    @property
    def terms(self):
        """Get the dictionary of SingleWord objects representing individual terms."""
        return self._state["collections"]["terms"]

    @property
    def candidates(self):
        """Get the dictionary of ComposedWord objects representing keyword candidates."""
        return self._state["collections"]["candidates"]

    @property
    def sentences_obj(self):
        """Get the nested list of processed sentence objects."""
        return self._state["collections"]["sentences_obj"]

    @property
    def sentences_str(self):
        """Get the list of raw sentence strings."""
        return self._state["collections"]["sentences_str"]

    @sentences_str.setter
    def sentences_str(self, value):
        """Set the list of raw sentence strings."""
        self._state["collections"]["sentences_str"] = value

    @property
    def freq_ns(self):
        """Get the frequency distribution of n-grams by length."""
        return self._state["collections"]["freq_ns"]

    # --- Internal utility methods ---
    def _build(self, text: str, windows_size: int, n: int) -> None:
        """
        Build the datacore features.

        This method processes the input text to extract terms, build the co-occurrence graph,
        and generate candidate keyphrases. It performs the following steps:
        1. Pre-filters and tokenizes the text into sentences and words
        2. Processes each word to create term objects
        3. Builds a co-occurrence matrix based on the window size
        4. Generates candidate keyphrases of various n-gram sizes
        5. Updates internal data structures with the extracted information

        Args:
            text: Input text to process
            windows_size: Size of window for co-occurrence matrix calculation
            n: Maximum n-gram size to consider for candidate keyphrases
        """
        # Pre-process text for normalization
        text = pre_filter(text)

        # Split text into sentences and tokenize
        self.sentences_str = tokenize_sentences(text)
        self.number_of_sentences = len(self.sentences_str)

        # Initialize position counter for global word positions
        pos_text = 0

        # Create a processing context dictionary to pass fewer arguments
        context = {"windows_size": windows_size, "n": n}

        # Process each sentence individually
        for sentence_id, sentence in enumerate(self.sentences_str):
            pos_text = self._process_sentence(sentence, sentence_id, pos_text, context)

        # Store the total number of processed words
        self.number_of_words = pos_text

    def _process_sentence(
        self,
        sentence: list[str],
        sentence_id: int,
        pos_text: int,
        context: dict[str, Any],
    ) -> int:
        """
        Process a single sentence from the document.

        Handles the tokenization of a sentence, identifies words and punctuation,
        and processes each meaningful word.

        Args:
            sentence: List of word tokens in the sentence
            sentence_id: Unique identifier for this sentence
            pos_text: Current global position in the text
            context: Processing context with configuration parameters

        Returns:
            Updated global position counter
        """
        # Initialize lists to store processed sentence components
        sentence_obj_aux = []  # Blocks of words within the sentence
        block_of_word_obj = []  # Current block of continuous words (separated by punctuation)

        # Extend the context with sentence information for word processing
        processing_context = context.copy()
        processing_context["sentence_id"] = sentence_id

        # Process each word in the sentence
        for pos_sent, word in enumerate(sentence):
            # Check if the word is just punctuation (all characters are excluded)
            if all(c in self.exclude for c in word):
                # If we have a block of words, save it and start a new block
                if block_of_word_obj:
                    sentence_obj_aux.append(block_of_word_obj)
                    block_of_word_obj = []
            else:
                # Process meaningful words
                word_context = {
                    "pos_sent": pos_sent,  # Position within the sentence
                    "block_of_word_obj": block_of_word_obj,  # Current word block
                }
                # Process this word and update position counter
                pos_text = self._process_word(
                    word,
                    pos_text,
                    processing_context,
                    word_context,
                )

        # Save any remaining word block
        if block_of_word_obj:
            sentence_obj_aux.append(block_of_word_obj)

        # Add processed sentence to collection if not empty
        if sentence_obj_aux:
            self.sentences_obj.append(sentence_obj_aux)

        return pos_text

    def _process_word(self, word, pos_text, context, word_context):
        """
        Process a single word within a sentence.

        Creates or retrieves the term object, updates its occurrences,
        analyzes co-occurrences with nearby words, and generates candidate keywords.

        Args:
            word (str): The word to process
            pos_text (int): Current global position in the text
            context (dict): Processing context with configuration parameters
            word_context (dict): Word-specific context information

        Returns:
            int: Updated global position counter
        """
        # Extract necessary context variables
        sentence_id = context["sentence_id"]
        windows_size = context["windows_size"]
        n = context["n"]
        pos_sent = word_context["pos_sent"]
        block_of_word_obj = word_context["block_of_word_obj"]

        # Get the part-of-speech tag for this word
        tag = self.get_tag(word, pos_sent)

        # Get or create the term object for this word
        term_obj = self.get_term(word)

        # Add this occurrence to the term's record
        term_obj.add_occur(tag, sentence_id, pos_sent, pos_text)

        # Increment global position counter
        pos_text += 1

        # Update co-occurrence information for valid tags
        if tag not in self.tags_to_discard:
            self._update_cooccurrence(block_of_word_obj, term_obj, windows_size)

        # Generate keyword candidates involving this term
        self._generate_candidates((tag, word), term_obj, block_of_word_obj, n)

        # Add this word to the current block
        block_of_word_obj.append((tag, word, term_obj))

        return pos_text

    def _update_cooccurrence(self, block_of_word_obj, term_obj, windows_size):
        """
        Update co-occurrence information between terms.

        Records relationships between the current term and previous terms
        within the specified window size.

        Args:
            block_of_word_obj (list): Current block of words
            term_obj (SingleWord): Term object for the current word
            windows_size (int): Size of co-occurrence window to consider
        """
        # Calculate the window of previous words to consider for co-occurrence
        word_windows = list(
            range(
                max(0, len(block_of_word_obj) - windows_size), len(block_of_word_obj)
            ),
        )

        # For each word in the window, update co-occurrence if it's a valid term
        for w in word_windows:
            if block_of_word_obj[w][0] not in self.tags_to_discard:
                # Add co-occurrence edge from previous term to current term
                self.add_cooccur(block_of_word_obj[w][2], term_obj)

    def _generate_candidates(self, term, term_obj, block_of_word_obj, n):
        """
        Generate keyword candidates from terms.

        Creates single-term candidates and multi-term candidates up to length n,
        combining the current term with previous terms.

        Args:
            term (tuple): Current term as (tag, word) tuple
            term_obj (SingleWord): Term object for the current word
            block_of_word_obj (list): Current block of words
            n (int): Maximum candidate length to generate
        """
        # Create single-term candidate
        candidate = [term + (term_obj,)]
        cand = ComposedWord(candidate)
        self.add_or_update_composedword(cand)

        # Calculate window of previous words to consider for multi-term candidates
        word_windows = list(
            range(max(0, len(block_of_word_obj) - (n - 1)), len(block_of_word_obj))
        )[::-1]  # Reverse to build phrases from right to left

        # Generate multi-term candidates with increasing length
        for w in word_windows:
            # Add previous term to candidate
            candidate.append(block_of_word_obj[w])

            # Update frequency count for this n-gram length
            self.freq_ns[len(candidate)] += 1.0

            # Create and register the composed word candidate
            # (reverse to maintain correct word order)
            cand = ComposedWord(candidate[::-1])
            self.add_or_update_composedword(cand)

    # --- Public API methods ---

    def get_tag(self, word, i):
        """
        Get tag for a word.

        Determines the type of word based on its characteristics:
        - 'd': Digit (numeric value)
        - 'u': Unknown (mixed alphanumeric or special characters)
        - 'a': All caps (acronym)
        - 'n': Proper noun (capitalized word not at sentence start)
        - 'p': Regular word

        Args:
            word: Word to tag
            i: Position in sentence (used to identify proper nouns)

        Returns:
            Tag as string representing the word type
        """
        return get_tag(word, i, self.exclude)

    def build_candidate(self, candidate_string: str) -> ComposedWord:
        """
        Build a candidate from a string.

        This function processes a candidate string by tokenizing it, tagging each word,
        and creating a ComposedWord object from the resulting terms. It's used to
        convert external strings into the internal candidate representation.

        Args:
            candidate_string: String to build candidate from

        Returns:
            A ComposedWord instance representing the candidate, or an invalid
            ComposedWord if no valid terms were found
        """

        # Tokenize the candidate string
        tokenized_words = [
            w
            for w in split_contractions(web_tokenizer(candidate_string.lower()))
            if not (w.startswith("'") and len(w) > 1) and len(w) > 0
        ]

        # Process each word in the candidate
        candidate_terms = []
        for index, word in enumerate(tokenized_words):
            # Get the tag and term object
            tag = self.get_tag(word, index)
            term_obj = self.get_term(word, save_non_seen=False)

            # Skip terms with zero term frequency (not in the original document)
            if term_obj.tf == 0:
                term_obj = None

            candidate_terms.append((tag, word, term_obj))

        # Check if the candidate has any valid terms
        if not any(term[2] for term in candidate_terms):
            # Return an invalid composed word if no valid terms
            return ComposedWord(None)

        # Create and return the composed word
        return ComposedWord(candidate_terms)

    def build_single_terms_features(self, features: list[str] | None = None) -> None:
        """
        Calculates and updates statistical features for all single terms in the text.
        This includes term frequency statistics and other features specified in the
        features parameter. Only non-stopword terms are considered for statistics
        calculation.

        Args:
            features: Specific features to calculate. If None, all available features will be built.
        """
        # Filter to valid terms (non-stopwords)
        valid_terms = [term for term in self.terms.values() if not term.stopword]
        valid_tfs = np.array([x.tf for x in valid_terms])

        # Skip if no valid terms
        if not valid_tfs.size:
            return

        # Calculate frequency statistics
        avg_tf = valid_tfs.mean()
        std_tf = valid_tfs.std()
        max_tf = max(x.tf for x in self.terms.values())

        # Prepare statistics dictionary for updating terms
        stats = {
            "max_tf": max_tf,
            "avg_tf": avg_tf,
            "std_tf": std_tf,
            "number_of_sentences": self.number_of_sentences,
        }

        # Update all terms with the calculated statistics
        for term in self.terms.values():
            term.update_h(stats, features=features)

    def build_mult_terms_features(self, features: list[str] | None = None) -> None:
        """
        Build features for multi-word terms.

        Updates the features for all valid multi-word candidate terms (n-grams).
        Only candidates that pass the validity check will have their features
        updated.

        Args:
            features: List of features to build. If None, all
                available features will be built.
        """
        # Update only valid candidates using single pass generator expression
        # This is more efficient than separate filter + map operations
        for cand in self.candidates.values():
            if cand.is_valid():
                cand.update_h(features=features)

    def get_term(self, str_word: str, save_non_seen: bool = True) -> SingleWord:
        """
        Get or create a term object for a word.

        Retrieves an existing term object for a word or creates a new one.
        The function also:
        1. Normalizes the word (lowercase, handles plural forms)
        2. Determines if the word is a stopword
        3. Creates a new term object if needed and adds it to the graph

        Args:
            str_word: Word to get term for
            save_non_seen: Whether to save new terms to the internal dictionary.
                          If False, creates a temporary term without saving it.

        Returns:
            SingleWord instance representing the term
        """
        # Normalize the term (convert to lowercase)
        unique_term = str_word.lower()

        # Check if it's a stopword in original form
        simples_sto = unique_term in self.stopword_set

        # Handle plural forms by removing trailing 's'
        if unique_term.endswith("s") and len(unique_term) > 3:
            unique_term = unique_term[:-1]

        # Return existing term if already processed
        if unique_term in self.terms:
            return self.terms[unique_term]

        # Remove punctuation for further analysis
        simples_unique_term = unique_term
        for pontuation in self.exclude:
            simples_unique_term = simples_unique_term.replace(pontuation, "")

        # Determine if this is a stopword (original form, normalized form, or too short)
        isstopword = (
            simples_sto
            or unique_term in self.stopword_set
            or len(simples_unique_term) < 3
        )

        # Create the term object
        term_id = len(self.terms)
        term_obj = SingleWord(unique_term, term_id, self.g)
        term_obj.stopword = isstopword

        # Save the term to the collection if requested
        if save_non_seen:
            self.g.add_node(term_id)
            self.terms[unique_term] = term_obj

        return term_obj

    def add_cooccur(self, left_term, right_term):
        """
        Add co-occurrence between terms.

        Updates the co-occurrence graph by adding or incrementing an edge between
        two terms. This information is used to calculate term relatedness and
        importance in the text.

        Args:
            left_term: Left term in the co-occurrence relationship
            right_term: Right term in the co-occurrence relationship
        """
        # Check if the edge already exists
        if right_term.id not in self.g[left_term.id]:
            # Create a new edge with initial weight
            self.g.add_edge(left_term.id, right_term.id, tf=0.0)

        # Increment the co-occurrence frequency
        self.g[left_term.id][right_term.id]["tf"] += 1.0

        # Invalidate graph metrics cache for affected terms
        left_term.invalidate_graph_cache()
        right_term.invalidate_graph_cache()

    def add_or_update_composedword(self, cand):
        """
        Add or update a composed word.

        Adds a new candidate composed word (n-gram) to the candidates dictionary
        or updates an existing one by incrementing its frequency. This is used to
        track potential keyphrases in the text.

        Args:
            cand: ComposedWord instance to add or update in the candidates dictionary
        """
        # Check if this candidate already exists
        if cand.unique_kw not in self.candidates:
            # Add new candidate
            self.candidates[cand.unique_kw] = cand
        else:
            # Update existing candidate with new information
            self.candidates[cand.unique_kw].update_cand(cand)

        # Increment the frequency counter for this candidate
        self.candidates[cand.unique_kw].tf += 1.0
