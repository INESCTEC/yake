"""
Benchmark script to measure performance impact of lemmatization.

This script compares YAKE performance with and without lemmatization.
"""

import sys
import os
from pathlib import Path

# Add project root to path to use local yake
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import time
import yake

# Test text
TEXT = """
Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning 
competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud 
Next conference in San Francisco this week, the official announcement could come as early as tomorrow. 
Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. 
Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its 
platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it 
has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by 
focusing on its specific niche. The service is basically the de facto home for running data science and machine 
learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data 
scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty 
of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's 
pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition 
around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. 
Our understanding is that Google will keep the service running - likely under its current name. While the 
acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools 
for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing 
data sets and developers can share this code on the platform (the company previously called them 'scripts'). 
Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with 
that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) 
since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, 
Google chief economist Hal Varian, Khosla Ventures and Yuri Milner.
""" * 3  # Triple the text for more substantial benchmark


def benchmark_no_lemmatization(n_runs=10):
    """Benchmark without lemmatization."""
    extractor = yake.KeywordExtractor(lan="en", n=3, top=20, lemmatize=False)
    
    times = []
    for _ in range(n_runs):
        start = time.time()
        keywords = extractor.extract_keywords(TEXT)
        end = time.time()
        times.append((end - start) * 1000)  # Convert to milliseconds
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    return {
        "avg_ms": avg_time,
        "min_ms": min_time,
        "max_ms": max_time,
        "keywords_count": len(keywords)
    }


def benchmark_with_lemmatization(aggregation="min", n_runs=10):
    """Benchmark with lemmatization."""
    extractor = yake.KeywordExtractor(
        lan="en", 
        n=3, 
        top=20, 
        lemmatize=True, 
        lemma_aggregation=aggregation
    )
    
    times = []
    for _ in range(n_runs):
        start = time.time()
        keywords = extractor.extract_keywords(TEXT)
        end = time.time()
        times.append((end - start) * 1000)  # Convert to milliseconds
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    return {
        "avg_ms": avg_time,
        "min_ms": min_time,
        "max_ms": max_time,
        "keywords_count": len(keywords)
    }


def main():
    """Run benchmarks and display results."""
    print("=" * 80)
    print("YAKE Lemmatization Performance Benchmark")
    print("=" * 80)
    print(f"\nText size: {len(TEXT)} characters")
    print(f"Test runs: 10 iterations each\n")
    
    # Baseline: No lemmatization
    print("Running baseline (no lemmatization)...")
    baseline = benchmark_no_lemmatization()
    print(f"✓ Baseline: {baseline['avg_ms']:.2f}ms avg "
          f"(min: {baseline['min_ms']:.2f}ms, max: {baseline['max_ms']:.2f}ms)")
    print(f"  Keywords extracted: {baseline['keywords_count']}\n")
    
    # Test each aggregation method
    aggregation_methods = ["min", "mean", "max", "harmonic"]
    
    for method in aggregation_methods:
        print(f"Running with lemmatization (aggregation={method})...")
        result = benchmark_with_lemmatization(method)
        overhead = result['avg_ms'] - baseline['avg_ms']
        overhead_pct = (overhead / baseline['avg_ms']) * 100
        
        print(f"✓ With lemmatization ({method}): {result['avg_ms']:.2f}ms avg "
              f"(min: {result['min_ms']:.2f}ms, max: {result['max_ms']:.2f}ms)")
        print(f"  Keywords extracted: {result['keywords_count']}")
        print(f"  Overhead: +{overhead:.2f}ms (+{overhead_pct:.1f}%)\n")
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Baseline (no lemmatization): {baseline['avg_ms']:.2f}ms")
    
    min_result = benchmark_with_lemmatization("min")
    overhead = min_result['avg_ms'] - baseline['avg_ms']
    overhead_pct = (overhead / baseline['avg_ms']) * 100
    
    print(f"With lemmatization (min):     {min_result['avg_ms']:.2f}ms "
          f"(+{overhead:.2f}ms, +{overhead_pct:.1f}%)")
    print(f"\nRecommendation: Lemmatization adds ~{overhead_pct:.0f}% overhead")
    print("                Use when keyword consolidation is more important than speed")
    print("=" * 80)


if __name__ == "__main__":
    main()
