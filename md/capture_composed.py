#!/usr/bin/env python
# pylint: skip-file
"""Capture expected results for ComposedWord tests."""

import yake

# Test: test_composed_word_valid_candidates
text = "machine learning algorithms"
pyake = yake.KeywordExtractor(lan="en", n=2, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_valid_candidates:")
print(f"res = {result}")
print()

# Test: test_composed_word_with_digits
text = "machine learning 2024 algorithms"
pyake = yake.KeywordExtractor(lan="en", n=2, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_with_digits:")
print(f"res = {result}")
print()

# Test: test_composed_word_with_stopwords
text = "machine learning and deep learning"
pyake = yake.KeywordExtractor(lan="en", n=2, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_with_stopwords:")
print(f"res = {result}")
print()

# Test: test_composed_word_with_acronym
text = "AI machine learning algorithms"
pyake = yake.KeywordExtractor(lan="en", n=2, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_with_acronym:")
print(f"res = {result}")
print()

# Test: test_composed_word_consecutive_stopwords (Issue #17)
text = "machine learning in and of deep learning"
pyake = yake.KeywordExtractor(lan="en", n=3, top=5)
result = pyake.extract_keywords(text)
print("test_composed_word_consecutive_stopwords:")
print(f"res = {result}")
print()

# Test: test_composed_word_n1
text = "machine learning algorithms"
pyake = yake.KeywordExtractor(lan="en", n=1, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_n1:")
print(f"res = {result}")
print()

# Test: test_composed_word_n3
text = "machine learning deep learning"
pyake = yake.KeywordExtractor(lan="en", n=3, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_n3:")
print(f"res = {result}")
print()

# Test: test_composed_word_n5
text = "artificial intelligence machine learning deep learning neural networks algorithms"
pyake = yake.KeywordExtractor(lan="en", n=5, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_n5:")
print(f"res = {result}")
print()

# Test: test_composed_word_get_composed_feature
text = "machine learning algorithms"
pyake = yake.KeywordExtractor(lan="en", n=2, top=3)
result = pyake.extract_keywords(text)
print("test_composed_word_get_composed_feature:")
print(f"res = {result}")
print()

# Test: test_composed_word_build_features_sum
text = "machine learning"
pyake = yake.KeywordExtractor(lan="en", n=2, top=1)
result = pyake.extract_keywords(text)
print("test_composed_word_build_features_sum:")
print(f"res = {result}")
print()

# Test: test_composed_word_build_features_prod
text = "machine learning"
pyake = yake.KeywordExtractor(lan="en", n=2, top=1)
result = pyake.extract_keywords(text)
print("test_composed_word_build_features_prod:")
print(f"res = {result}")
print()
