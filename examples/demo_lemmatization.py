#!/usr/bin/env python
"""
Demo script showing lemmatization feature in YAKE.

This demonstrates how lemmatization aggregates morphological variations
of keywords to reduce redundancy.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import yake


def demo_basic_lemmatization():
    """Basic lemmatization demo."""
    print("=" * 80)
    print("DEMO 1: Basic Lemmatization")
    print("=" * 80)
    
    text = """
    Trees are essential for our ecosystem. Many trees provide oxygen and shade.
    Tree conservation is crucial. Researchers study trees extensively.
    The researcher's work on tree biology is important.
    """
    
    print("\n📝 Text:", text.strip())
    print("\n" + "-" * 80)
    
    # Without lemmatization
    print("\n🔍 WITHOUT Lemmatization:")
    kw_no_lemma = yake.KeywordExtractor(lan="en", n=1, top=10, lemmatize=False)
    keywords_no_lemma = kw_no_lemma.extract_keywords(text)
    
    for i, (kw, score) in enumerate(keywords_no_lemma, 1):
        print(f"   {i:2d}. {kw:20s} (score: {score:.4f})")
    
    # With lemmatization
    print("\n✨ WITH Lemmatization (aggregation=min):")
    kw_with_lemma = yake.KeywordExtractor(
        lan="en", 
        n=1, 
        top=10, 
        lemmatize=True,
        lemma_aggregation="min"
    )
    keywords_with_lemma = kw_with_lemma.extract_keywords(text)
    
    for i, (kw, score) in enumerate(keywords_with_lemma, 1):
        print(f"   {i:2d}. {kw:20s} (score: {score:.4f})")
    
    print("\n💡 Notice: 'tree', 'trees' → consolidated into one entry")
    print("          'researcher', 'researchers' → consolidated")


def demo_aggregation_methods():
    """Demo different aggregation methods."""
    print("\n\n" + "=" * 80)
    print("DEMO 2: Aggregation Methods Comparison")
    print("=" * 80)
    
    text = """
    Running is healthy. Runners enjoy running. The runner runs every morning.
    Many runners participate in races. Running improves fitness.
    """
    
    print("\n📝 Text:", text.strip())
    
    methods = {
        "min": "Best (lowest) score",
        "mean": "Average score",
        "max": "Worst (highest) score",
        "harmonic": "Harmonic mean"
    }
    
    for method, description in methods.items():
        print(f"\n\n{'─' * 40}")
        print(f"Method: {method} ({description})")
        print(f"{'─' * 40}")
        
        kw_extractor = yake.KeywordExtractor(
            lan="en",
            n=1,
            top=5,
            lemmatize=True,
            lemma_aggregation=method
        )
        keywords = kw_extractor.extract_keywords(text)
        
        for i, (kw, score) in enumerate(keywords, 1):
            print(f"   {i}. {kw:15s} (score: {score:.4f})")


def demo_multiword_lemmatization():
    """Demo lemmatization with multi-word keywords."""
    print("\n\n" + "=" * 80)
    print("DEMO 3: Multi-word Keyword Lemmatization")
    print("=" * 80)
    
    text = """
    Machine learning algorithms are transforming industries. Deep learning models
    excel at pattern recognition. Natural language processing tasks have improved
    significantly. Machine learning techniques continue to evolve. Learning algorithms
    adapt to new data patterns.
    """
    
    print("\n📝 Text:", text.strip())
    print("\n" + "-" * 80)
    
    # Extract bigrams with lemmatization
    print("\n✨ Bigrams WITH Lemmatization:")
    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=2,
        top=10,
        lemmatize=True,
        lemma_aggregation="min"
    )
    keywords = kw_extractor.extract_keywords(text)
    
    for i, (kw, score) in enumerate(keywords, 1):
        print(f"   {i:2d}. {kw:30s} (score: {score:.4f})")
    
    print("\n💡 Notice: Multi-word phrases are also lemmatized")


def demo_performance_comparison():
    """Demo performance with and without lemmatization."""
    print("\n\n" + "=" * 80)
    print("DEMO 4: Performance Comparison")
    print("=" * 80)
    
    text = """
    Sources tell us that Google is acquiring Kaggle, a platform that hosts data science 
    and machine learning competitions. Details about the transaction remain somewhat vague, 
    but given that Google is hosting its Cloud Next conference in San Francisco this week, 
    the official announcement could come as early as tomorrow.
    """ * 5  # Repeat for more substantial text
    
    import time
    
    # Measure without lemmatization
    kw_no_lemma = yake.KeywordExtractor(lan="en", n=3, top=20, lemmatize=False)
    start = time.time()
    keywords_no_lemma = kw_no_lemma.extract_keywords(text)
    time_no_lemma = (time.time() - start) * 1000
    
    # Measure with lemmatization
    kw_with_lemma = yake.KeywordExtractor(lan="en", n=3, top=20, lemmatize=True)
    start = time.time()
    keywords_with_lemma = kw_with_lemma.extract_keywords(text)
    time_with_lemma = (time.time() - start) * 1000
    
    overhead = time_with_lemma - time_no_lemma
    overhead_pct = (overhead / time_no_lemma) * 100
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Text size:           {len(text)} characters")
    print(f"   Without lemmatization: {time_no_lemma:.2f}ms")
    print(f"   With lemmatization:    {time_with_lemma:.2f}ms")
    print(f"   Overhead:              +{overhead:.2f}ms (+{overhead_pct:.1f}%)")
    print(f"\n   Keywords extracted:")
    print(f"   Without: {len(keywords_no_lemma)} keywords")
    print(f"   With:    {len(keywords_with_lemma)} keywords")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "YAKE Lemmatization Feature Demo" + " " * 26 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        demo_basic_lemmatization()
        demo_aggregation_methods()
        demo_multiword_lemmatization()
        demo_performance_comparison()
        
        print("\n\n" + "=" * 80)
        print("✅ All demos completed successfully!")
        print("=" * 80)
        
        print("\n📚 For more information:")
        print("   - README: See 'Lemmatization' section")
        print("   - Docs: docs-site/content/docs/lemmatization.mdx")
        print("   - Tests: tests/test_lemmatization.py")
        print("   - Issue: https://github.com/LIAAD/yake/issues/45")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
