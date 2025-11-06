#!/usr/bin/env python
# pylint: skip-file
"""Capture expected results for multiple tests."""

import yake

# Test: test_deduplication_functions
text_content = "machine learning machine learning deep learning"
pyake = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=5)
result = pyake.extract_keywords(text_content)
print("test_deduplication_functions:")
print(f"res = {result}")
print()

# Test: test_no_deduplication
pyake = yake.KeywordExtractor(lan="en", n=2, dedupLim=1.0, top=5)
result = pyake.extract_keywords(text_content)
print("test_no_deduplication:")
print(f"res = {result}")
print()

# Test: test_custom_stopwords
text_content = "learning algorithms and machine learning are powerful"
custom = ["powerful"]
pyake = yake.KeywordExtractor(lan="en", n=2, stopwords=custom, top=5)
result = pyake.extract_keywords(text_content)
print("test_custom_stopwords:")
print(f"res = {result}")
print()

# Test: test_window_size_parameter
text_content = "data science and machine learning"
pyake = yake.KeywordExtractor(lan="en", n=2, windowsSize=2, top=5)
result = pyake.extract_keywords(text_content)
print("test_window_size_parameter:")
print(f"res = {result}")
print()

# Test: test_multilingual_support (German)
text_de = "Maschinelles Lernen und künstliche Intelligenz sind wichtige Technologien"
pyake = yake.KeywordExtractor(lan="de", n=2, top=5)
result = pyake.extract_keywords(text_de)
print("test_multilingual_support (German):")
print(f"res_de = {result}")
print()

# Test: test_multilingual_support (French)
text_fr = "L'apprentissage automatique et l'intelligence artificielle transforment le monde"
pyake = yake.KeywordExtractor(lan="fr", n=2, top=5)
result = pyake.extract_keywords(text_fr)
print("test_multilingual_support (French):")
print(f"res_fr = {result}")
print()

# Test: test_large_dataset_strategy
text_large = " ".join(["data science machine learning"] * 1000)
pyake = yake.KeywordExtractor(lan="en", n=2, top=5)
result = pyake.extract_keywords(text_large)
print("test_large_dataset_strategy:")
print(f"res = {result}")
print()

# Test: test_medium_dataset_strategy
text_medium = " ".join(["data science machine learning"] * 100)
pyake = yake.KeywordExtractor(lan="en", n=2, top=5)
result = pyake.extract_keywords(text_medium)
print("test_medium_dataset_strategy:")
print(f"res = {result}")
print()

# Test: test_small_dataset_strategy
text_small = "data science machine learning"
pyake = yake.KeywordExtractor(lan="en", n=2, top=5)
result = pyake.extract_keywords(text_small)
print("test_small_dataset_strategy:")
print(f"res = {result}")
print()
