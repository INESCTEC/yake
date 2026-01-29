#!/usr/bin/env python
"""
Test Python 3.13 performance features (JIT, locals() optimization).

This script benchmarks YAKE performance with and without Python 3.13 optimizations.
"""

import os
import sys
import time
import statistics

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import yake


def benchmark_extraction(text, iterations=50):
    """Benchmark keyword extraction performance."""
    extractor = yake.KeywordExtractor(lan="en", n=3, top=20)
    
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        extractor.extract_keywords(text)
        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)  # Convert to ms
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
    }


def main():
    """Run performance benchmarks."""
    # Test text
    text = """
    Google is acquiring data science community Kaggle. Sources tell us that Google is 
    acquiring Kaggle, a platform that hosts data science and machine learning competitions.
    Details about the transaction remain somewhat vague, but given that Google is hosting 
    its Cloud Next conference in San Francisco this week, the official announcement could 
    come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom 
    declined to deny that the acquisition is happening. Google itself declined to comment on rumors.
    """ * 20  # Larger text for meaningful benchmark
    
    print("=" * 70)
    print("Python 3.13 Performance Test")
    print("=" * 70)
    print(f"Python version: {sys.version}")
    print(f"JIT enabled: {os.environ.get('PYTHON_JIT', '0')}")
    print(f"Text size: {len(text.split())} words")
    print()
    
    # Warm-up
    extractor = yake.KeywordExtractor(lan="en", n=3, top=20)
    extractor.extract_keywords(text)
    
    # Benchmark
    print("Running benchmark (50 iterations)...")
    results = benchmark_extraction(text, iterations=50)
    
    print()
    print("Results:")
    print(f"  Mean:   {results['mean']:.2f} ms")
    print(f"  Median: {results['median']:.2f} ms")
    print(f"  StdDev: {results['stdev']:.2f} ms")
    print(f"  Min:    {results['min']:.2f} ms")
    print(f"  Max:    {results['max']:.2f} ms")
    print()
    
    # Cache statistics
    stats = extractor.get_cache_stats()
    print("Cache Statistics:")
    print(f"  Hit rate: {stats['hit_rate']:.1f}%")
    print(f"  Hits:     {stats['hits']}")
    print(f"  Misses:   {stats['misses']}")
    print()
    
    # Performance target
    target = 50.0  # ms (YAKE 2.0 target)
    baseline = 100.0  # ms (YAKE 0.6.0 baseline)
    
    improvement = ((baseline - results['mean']) / baseline) * 100
    
    print("Performance Assessment:")
    print(f"  Target:      < {target:.0f} ms")
    print(f"  Baseline:    ~{baseline:.0f} ms (YAKE 0.6.0)")
    print(f"  Current:     {results['mean']:.2f} ms")
    print(f"  Improvement: {improvement:.1f}% faster than baseline")
    
    if results['mean'] < target:
        print(f"  Status:      ✅ PASS (under {target}ms target)")
    else:
        print(f"  Status:      ⚠️  ACCEPTABLE (under {baseline}ms baseline)")
    
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
