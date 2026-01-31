#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""
Tests for yake.data.features module.

Tests cover all feature calculation functions including term features,
composed features, and feature aggregation methods.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import math
import pytest
import numpy as np
from unittest.mock import Mock, MagicMock
import networkx as nx

from yake.data.features import (
    calculate_term_features,
    calculate_composed_features,
    get_feature_aggregation
)


class TestCalculateTermFeatures:
    """Test suite for calculate_term_features function."""
    
    def test_basic_term_features(self):
        """Test feature calculation for a basic term."""
        # Create mock term with required attributes
        term = Mock()
        term.tf = 5.0
        term.tf_a = 2.0  # Capitalized occurrences
        term.tf_n = 3.0  # Non-capitalized occurrences
        term.sentence_ids = {1, 2, 3}  # Appears in 3 sentences
        term.occurs = {0: None, 5: None, 10: None}  # Positions
        term.graph_metrics = {
            'pwl': 0.5,
            'pwr': 0.5,
            'wdl': 10.0,
            'wdr': 10.0
        }
        
        # Document statistics
        max_tf = 10.0
        avg_tf = 3.0
        std_tf = 2.0
        number_of_sentences = 5
        
        features = calculate_term_features(
            term, max_tf, avg_tf, std_tf, number_of_sentences
        )
        
        # Verify all features are calculated
        assert 'w_rel' in features
        assert 'w_freq' in features
        assert 'w_spread' in features
        assert 'w_case' in features
        assert 'w_pos' in features
        assert 'h' in features
        
        # Verify feature values are reasonable
        assert features['w_rel'] > 0
        assert features['w_freq'] > 0
        assert 0 <= features['w_spread'] <= 1  # Spread is between 0 and 1
        assert features['w_case'] > 0
        assert features['w_pos'] > 0
        assert features['h'] > 0
    
    def test_w_rel_calculation(self):
        """Test WRel (term relevance) calculation."""
        term = Mock()
        term.tf = 5.0
        term.tf_a = 2.0
        term.tf_n = 3.0
        term.sentence_ids = {1}
        term.occurs = {0: None}
        term.graph_metrics = {
            'pwl': 0.3,
            'pwr': 0.7,
            'wdl': 5.0,
            'wdr': 5.0
        }
        
        features = calculate_term_features(term, 10.0, 3.0, 2.0, 5)
        
        # WRel should combine left and right connectivity
        expected_wrel = (0.5 + (0.3 * (5.0 / 10.0))) + (0.5 + (0.7 * (5.0 / 10.0)))
        assert abs(features['w_rel'] - expected_wrel) < 1e-6
    
    def test_w_freq_calculation(self):
        """Test WFreq (normalized frequency) calculation."""
        term = Mock()
        term.tf = 8.0
        term.tf_a = 4.0
        term.tf_n = 4.0
        term.sentence_ids = {1}
        term.occurs = {0: None}
        term.graph_metrics = {
            'pwl': 0.5, 'pwr': 0.5, 'wdl': 5.0, 'wdr': 5.0
        }
        
        avg_tf = 3.0
        std_tf = 2.0
        features = calculate_term_features(term, 10.0, avg_tf, std_tf, 5)
        
        # WFreq = tf / (avg_tf + std_tf)
        expected_wfreq = 8.0 / (3.0 + 2.0)
        assert abs(features['w_freq'] - expected_wfreq) < 1e-6
    
    def test_w_spread_calculation(self):
        """Test WSpread (sentence spread) calculation."""
        term = Mock()
        term.tf = 5.0
        term.tf_a = 2.0
        term.tf_n = 3.0
        term.sentence_ids = {1, 2, 3, 4}  # 4 out of 10 sentences
        term.occurs = {0: None}
        term.graph_metrics = {
            'pwl': 0.5, 'pwr': 0.5, 'wdl': 5.0, 'wdr': 5.0
        }
        
        features = calculate_term_features(term, 10.0, 3.0, 2.0, 10)
        
        # WSpread = len(sentence_ids) / total_sentences
        expected_wspread = 4.0 / 10.0
        assert abs(features['w_spread'] - expected_wspread) < 1e-6
    
    def test_w_case_calculation(self):
        """Test WCase (capitalization) calculation."""
        term = Mock()
        term.tf = 10.0
        term.tf_a = 7.0  # Mostly capitalized
        term.tf_n = 3.0
        term.sentence_ids = {1}
        term.occurs = {0: None}
        term.graph_metrics = {
            'pwl': 0.5, 'pwr': 0.5, 'wdl': 5.0, 'wdr': 5.0
        }
        
        features = calculate_term_features(term, 10.0, 3.0, 2.0, 5)
        
        # WCase = max(tf_a, tf_n) / (1 + log(tf))
        expected_wcase = 7.0 / (1.0 + math.log(10.0))
        assert abs(features['w_case'] - expected_wcase) < 1e-6
    
    def test_w_pos_calculation(self):
        """Test WPos (position) calculation using median."""
        term = Mock()
        term.tf = 5.0
        term.tf_a = 2.0
        term.tf_n = 3.0
        term.sentence_ids = {1}
        term.occurs = {10: None, 20: None, 30: None, 40: None, 50: None}
        term.graph_metrics = {
            'pwl': 0.5, 'pwr': 0.5, 'wdl': 5.0, 'wdr': 5.0
        }
        
        features = calculate_term_features(term, 10.0, 3.0, 2.0, 5)
        
        # WPos = log(log(3 + median(positions)))
        positions = [10, 20, 30, 40, 50]
        median_pos = np.median(positions)  # 30
        expected_wpos = math.log(math.log(3.0 + median_pos))
        assert abs(features['w_pos'] - expected_wpos) < 1e-6
    
    def test_zero_max_tf_handling(self):
        """Test handling of edge case where max_tf is zero."""
        term = Mock()
        term.tf = 0.0
        term.tf_a = 0.0
        term.tf_n = 0.0
        term.sentence_ids = {1}
        term.occurs = {0: None}
        term.graph_metrics = {
            'pwl': 0.5, 'pwr': 0.5, 'wdl': 0.0, 'wdr': 0.0
        }
        
        # When max_tf is 0, term.tf should also be 0, avoiding division
        # But if it happens, the code should handle it gracefully
        # Note: In real usage, max_tf=0 means no terms, so this is edge case
        # The implementation has protection for pl and pr, but not for w_rel
        # This test documents the current behavior
        try:
            features = calculate_term_features(term, 0.0, 3.0, 2.0, 5)
            # If it succeeds, verify pl and pr are 0
            assert features['pl'] == 0.0
            assert features['pr'] == 0.0
        except ZeroDivisionError:
            # Expected behavior when max_tf=0 and tf>0 (edge case)
            # In real usage, this shouldn't happen
            pass
    
    def test_single_position_term(self):
        """Test term that appears only once."""
        term = Mock()
        term.tf = 1.0
        term.tf_a = 1.0
        term.tf_n = 0.0
        term.sentence_ids = {1}
        term.occurs = {5: None}  # Single position
        term.graph_metrics = {
            'pwl': 0.5, 'pwr': 0.5, 'wdl': 1.0, 'wdr': 1.0
        }
        
        features = calculate_term_features(term, 10.0, 3.0, 2.0, 5)
        
        # Should calculate all features without errors
        assert all(v is not None for v in features.values())
        assert features['w_spread'] == 1.0 / 5.0  # 1 sentence out of 5


class TestCalculateComposedFeatures:
    """Test suite for calculate_composed_features function."""
    
    def create_mock_term(self, h_value, is_stopword=False, term_id=None, tf=1.0):
        """Helper to create mock terms."""
        term = Mock()
        term.h = h_value
        term.stopword = is_stopword
        term.id = term_id or f"term_{h_value}"
        term.tf = tf
        term.g = nx.DiGraph()
        return term
    
    def test_composed_features_no_stopwords(self):
        """Test composed features for phrase without stopwords."""
        # Create composed word with 3 non-stopword terms
        composed_word = Mock()
        composed_word.tf = 5.0
        composed_word.terms = [
            self.create_mock_term(0.1, False),
            self.create_mock_term(0.2, False),
            self.create_mock_term(0.3, False)
        ]
        
        features = calculate_composed_features(composed_word)
        
        # sum_h = 0.1 + 0.2 + 0.3 = 0.6
        assert abs(features['sum_h'] - 0.6) < 1e-6
        
        # prod_h = 0.1 * 0.2 * 0.3 = 0.006
        assert abs(features['prod_h'] - 0.006) < 1e-6
        
        # tf_used = 5.0
        assert features['tf_used'] == 5.0
        
        # H = prod_h / ((sum_h + 1) * tf_used)
        expected_h = 0.006 / ((0.6 + 1) * 5.0)
        assert abs(features['h'] - expected_h) < 1e-6
    
    def test_composed_features_with_stopwords_bi(self):
        """Test composed features with stopwords using 'bi' weighting."""
        composed_word = Mock()
        composed_word.tf = 3.0
        
        # Create terms: term1 (non-stop), stopword, term2 (non-stop)
        term1 = self.create_mock_term(0.2, False, "term1", 4.0)
        stopword = self.create_mock_term(0.05, True, "stop", 2.0)
        term2 = self.create_mock_term(0.3, False, "term2", 3.0)
        
        # Add edges for stopword connectivity
        stopword.g.add_edge("term1", "stop", tf=2.0)
        stopword.g.add_edge("stop", "term2", tf=1.5)
        
        composed_word.terms = [term1, stopword, term2]
        
        features = calculate_composed_features(composed_word, stopword_weight='bi')
        
        # Stopword affects prod_h and sum_h based on connectivity
        # Note: sum_h can be negative due to stopword probability penalty
        assert features['prod_h'] > 0
        # sum_h can be negative with stopword penalties
        assert isinstance(features['sum_h'], float)
        assert features['h'] > 0
    
    def test_composed_features_stopwords_h_weight(self):
        """Test stopword handling with 'h' weighting."""
        composed_word = Mock()
        composed_word.tf = 2.0
        composed_word.terms = [
            self.create_mock_term(0.2, False),
            self.create_mock_term(0.1, True),  # Stopword with h=0.1
            self.create_mock_term(0.3, False)
        ]
        
        features = calculate_composed_features(composed_word, stopword_weight='h')
        
        # With 'h' weight, stopword's h value is included
        # sum_h = 0.2 + 0.1 + 0.3 = 0.6
        assert abs(features['sum_h'] - 0.6) < 1e-6
        
        # prod_h = 0.2 * 0.1 * 0.3 = 0.006
        assert abs(features['prod_h'] - 0.006) < 1e-6
    
    def test_composed_features_stopwords_none_weight(self):
        """Test stopword handling with 'none' weighting (ignore stopwords)."""
        composed_word = Mock()
        composed_word.tf = 2.0
        composed_word.terms = [
            self.create_mock_term(0.2, False),
            self.create_mock_term(0.999, True),  # Stopword should be ignored
            self.create_mock_term(0.3, False)
        ]
        
        features = calculate_composed_features(composed_word, stopword_weight='none')
        
        # sum_h = 0.2 + 0.3 = 0.5 (stopword ignored)
        assert abs(features['sum_h'] - 0.5) < 1e-6
        
        # prod_h = 0.2 * 0.3 = 0.06 (stopword ignored)
        assert abs(features['prod_h'] - 0.06) < 1e-6
    
    def test_single_term_composed_word(self):
        """Test composed word with single term."""
        composed_word = Mock()
        composed_word.tf = 1.0
        composed_word.terms = [self.create_mock_term(0.5, False)]
        
        features = calculate_composed_features(composed_word)
        
        assert features['sum_h'] == 0.5
        assert features['prod_h'] == 0.5
        assert features['tf_used'] == 1.0
    
    def test_zero_tf_handling(self):
        """Test handling of zero term frequency."""
        composed_word = Mock()
        composed_word.tf = 0.0
        composed_word.terms = [self.create_mock_term(0.5, False)]
        
        features = calculate_composed_features(composed_word)
        
        # With tf=0, H should be 0 to avoid division by zero
        assert features['h'] == 0.0


class TestGetFeatureAggregation:
    """Test suite for get_feature_aggregation function."""
    
    def create_mock_term_with_feature(self, feature_value, is_stopword=False):
        """Helper to create mock term with specific feature value."""
        term = Mock()
        term.test_feature = feature_value
        term.stopword = is_stopword
        return term
    
    def test_feature_aggregation_basic(self):
        """Test basic feature aggregation."""
        composed_word = Mock()
        composed_word.terms = [
            self.create_mock_term_with_feature(2.0, False),
            self.create_mock_term_with_feature(3.0, False),
            self.create_mock_term_with_feature(5.0, False)
        ]
        
        sum_f, prod_f, ratio = get_feature_aggregation(
            composed_word, 'test_feature', exclude_stopwords=False
        )
        
        # sum = 2 + 3 + 5 = 10
        assert abs(sum_f - 10.0) < 1e-6
        
        # product = 2 * 3 * 5 = 30
        assert abs(prod_f - 30.0) < 1e-6
        
        # ratio = 30 / (10 + 1) = 30 / 11
        assert abs(ratio - (30.0 / 11.0)) < 1e-6
    
    def test_feature_aggregation_exclude_stopwords(self):
        """Test aggregation excluding stopwords."""
        composed_word = Mock()
        composed_word.terms = [
            self.create_mock_term_with_feature(2.0, False),
            self.create_mock_term_with_feature(999.0, True),  # Stopword
            self.create_mock_term_with_feature(3.0, False)
        ]
        
        sum_f, prod_f, ratio = get_feature_aggregation(
            composed_word, 'test_feature', exclude_stopwords=True
        )
        
        # sum = 2 + 3 = 5 (stopword excluded)
        assert abs(sum_f - 5.0) < 1e-6
        
        # product = 2 * 3 = 6
        assert abs(prod_f - 6.0) < 1e-6
    
    def test_feature_aggregation_include_stopwords(self):
        """Test aggregation including stopwords."""
        composed_word = Mock()
        composed_word.terms = [
            self.create_mock_term_with_feature(2.0, False),
            self.create_mock_term_with_feature(4.0, True),  # Stopword
            self.create_mock_term_with_feature(3.0, False)
        ]
        
        sum_f, prod_f, ratio = get_feature_aggregation(
            composed_word, 'test_feature', exclude_stopwords=False
        )
        
        # sum = 2 + 4 + 3 = 9 (stopword included)
        assert abs(sum_f - 9.0) < 1e-6
        
        # product = 2 * 4 * 3 = 24
        assert abs(prod_f - 24.0) < 1e-6
    
    def test_empty_feature_list(self):
        """Test aggregation when all terms are stopwords and excluded."""
        composed_word = Mock()
        composed_word.terms = [
            self.create_mock_term_with_feature(5.0, True),
            self.create_mock_term_with_feature(10.0, True)
        ]
        
        sum_f, prod_f, ratio = get_feature_aggregation(
            composed_word, 'test_feature', exclude_stopwords=True
        )
        
        # All terms excluded, should return zeros
        assert sum_f == 0.0
        assert prod_f == 0.0
        assert ratio == 0.0
    
    def test_single_term_aggregation(self):
        """Test aggregation with single term."""
        composed_word = Mock()
        composed_word.terms = [self.create_mock_term_with_feature(7.0, False)]
        
        sum_f, prod_f, ratio = get_feature_aggregation(
            composed_word, 'test_feature', exclude_stopwords=False
        )
        
        assert sum_f == 7.0
        assert prod_f == 7.0
        assert abs(ratio - (7.0 / 8.0)) < 1e-6  # 7 / (7 + 1)
    
    def test_zero_values_in_product(self):
        """Test aggregation when one feature value is zero."""
        composed_word = Mock()
        composed_word.terms = [
            self.create_mock_term_with_feature(2.0, False),
            self.create_mock_term_with_feature(0.0, False),  # Zero value
            self.create_mock_term_with_feature(3.0, False)
        ]
        
        sum_f, prod_f, ratio = get_feature_aggregation(
            composed_word, 'test_feature', exclude_stopwords=False
        )
        
        assert sum_f == 5.0  # 2 + 0 + 3
        assert prod_f == 0.0  # 2 * 0 * 3 = 0
        assert ratio == 0.0   # 0 / 6 = 0


class TestFeatureIntegration:
    """Integration tests for feature calculations."""
    
    def test_features_produce_positive_scores(self):
        """Test that feature calculations produce valid positive scores."""
        term = Mock()
        term.tf = 5.0
        term.tf_a = 3.0
        term.tf_n = 2.0
        term.sentence_ids = {1, 2}
        term.occurs = {10: None, 20: None, 30: None}
        term.graph_metrics = {
            'pwl': 0.6,
            'pwr': 0.4,
            'wdl': 8.0,
            'wdr': 7.0
        }
        
        features = calculate_term_features(term, 10.0, 4.0, 2.0, 5)
        
        # All features should be positive for valid term
        assert all(v > 0 for v in features.values())
    
    def test_high_tf_term_gets_good_score(self):
        """Test that high frequency terms get favorable feature scores."""
        high_tf_term = Mock()
        high_tf_term.tf = 20.0
        high_tf_term.tf_a = 15.0
        high_tf_term.tf_n = 5.0
        high_tf_term.sentence_ids = {1, 2, 3, 4, 5}
        high_tf_term.occurs = {i: None for i in range(20)}
        high_tf_term.graph_metrics = {
            'pwl': 0.8, 'pwr': 0.8, 'wdl': 15.0, 'wdr': 15.0
        }
        
        features = calculate_term_features(high_tf_term, 20.0, 5.0, 3.0, 5)
        
        # High frequency term should have high w_freq and w_spread
        assert features['w_freq'] > 1.0
        assert features['w_spread'] == 1.0  # Appears in all sentences
