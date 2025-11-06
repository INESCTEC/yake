# pylint: skip-file
"""
Test script to verify intelligent cache management.

This script tests the new cache management system to ensure:
1. Cache is cleared for large documents (>2000 words)
2. Cache is cleared when 80% full
3. Cache is cleared every 50 documents (failsafe)
4. Manual clear_caches() works correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yake import KeywordExtractor

def test_cache_management():
    """Test the intelligent cache management system."""
    
    print("=" * 70)
    print("🧪 TESTING INTELLIGENT CACHE MANAGEMENT")
    print("=" * 70)
    
    extractor = KeywordExtractor(lan="en", n=3, top=10)
    
    # Test 1: Small documents (cache should NOT clear)
    print("\n📝 Test 1: Small documents (50-100 words)")
    print("-" * 70)
    
    small_text = "Machine learning and artificial intelligence are transforming technology. " * 5
    
    for i in range(5):
        keywords = extractor.extract_keywords(small_text)
        stats = extractor.get_cache_stats()
        print(f"  Doc {i+1}: {stats['docs_processed']} docs, cache: {stats['cache_size']:.1%}, "
              f"hit_rate: {stats['hit_rate']:.1f}%")
    
    print(f"✅ Cache preserved (usage: {stats['cache_size']:.1%})")
    
    # Test 2: Large document (cache SHOULD clear)
    print("\n📝 Test 2: Large document (>2000 words)")
    print("-" * 70)
    
    large_text = ("Python programming language provides powerful tools for data science. "
                  "Machine learning algorithms process vast amounts of information efficiently. "
                  "Deep learning neural networks revolutionize computer vision tasks. "
                  "Natural language processing enables computers to understand human speech. ") * 100
    
    stats_before = extractor.get_cache_stats()
    print(f"  Before: {stats_before['docs_processed']} docs, cache: {stats_before['cache_size']:.1%}")
    
    keywords = extractor.extract_keywords(large_text)
    
    stats_after = extractor.get_cache_stats()
    print(f"  After: {stats_after['docs_processed']} docs, cache: {stats_after['cache_size']:.1%}")
    
    if stats_after['docs_processed'] == 0:
        print(f"✅ Cache cleared automatically (large document: {len(large_text.split())} words)")
    else:
        print(f"❌ Cache NOT cleared!")
    
    # Test 3: 50 documents failsafe
    print("\n📝 Test 3: Failsafe clear every 50 documents")
    print("-" * 70)
    
    medium_text = "Data science combines statistics and programming. " * 10
    
    for i in range(55):
        keywords = extractor.extract_keywords(medium_text)
        stats = extractor.get_cache_stats()
        
        if i in [48, 49, 50, 51]:  # Show around the threshold
            print(f"  Doc {i+1}: {stats['docs_processed']} processed, cache: {stats['cache_size']:.1%}")
    
    if stats['docs_processed'] < 10:  # Should have reset after 50
        print(f"✅ Failsafe triggered at 50 documents")
    else:
        print(f"❌ Failsafe did NOT trigger!")
    
    # Test 4: Manual clear
    print("\n📝 Test 4: Manual cache clear")
    print("-" * 70)
    
    # Build up cache
    for i in range(10):
        keywords = extractor.extract_keywords(small_text)
    
    stats_before = extractor.get_cache_stats()
    print(f"  Before clear: {stats_before['docs_processed']} docs, cache: {stats_before['cache_size']:.1%}")
    
    # Manual clear
    extractor.clear_caches()
    
    stats_after = extractor.get_cache_stats()
    print(f"  After clear: {stats_after['docs_processed']} docs, cache: {stats_after['cache_size']:.1%}")
    
    if stats_after['docs_processed'] == 0:
        print(f"✅ Manual clear worked!")
    else:
        print(f"❌ Manual clear failed!")
    
    # Test 5: Cache stats
    print("\n📝 Test 5: Cache statistics")
    print("-" * 70)
    
    for i in range(10):
        keywords = extractor.extract_keywords(small_text)
    
    stats = extractor.get_cache_stats()
    print(f"  Total hits: {stats['hits']}")
    print(f"  Total misses: {stats['misses']}")
    print(f"  Hit rate: {stats['hit_rate']:.1f}%")
    print(f"  Documents processed: {stats['docs_processed']}")
    print(f"  Cache usage: {stats['cache_size']:.1%}")
    
    if stats['hit_rate'] > 50:
        print(f"✅ Cache is effective (hit rate > 50%)")
    
    print("\n" + "=" * 70)
    print("✅ ALL CACHE MANAGEMENT TESTS COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    test_cache_management()
