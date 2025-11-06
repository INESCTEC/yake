# pylint: skip-file
"""
Benchmark comparativo: YAKE v0.6.0 vs Versão Atual (v2.0)
Documenta o impacto de todas as otimizações aplicadas
"""

import sys
import time
import tracemalloc
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "yake"))

# Import current version
from yake import KeywordExtractor as KeywordExtractorCurrent

# Import v0.6.0
sys.path.insert(0, str(Path(__file__).parent.parent / "yake" / "yake_0.6.0" / "core"))
from yake import KeywordExtractor as KeywordExtractorV06


TEST_TEXTS = {
    'small': """
    Artificial intelligence and machine learning are transforming technology.
    Deep learning models can process natural language with high accuracy.
    Neural networks enable computer vision and speech recognition systems.
    """,
    
    'medium': """
    Artificial intelligence and machine learning are revolutionizing the modern 
    technology landscape. Deep learning neural networks have enabled breakthrough 
    advances in computer vision, natural language processing, and speech recognition. 
    These sophisticated algorithms can now analyze vast amounts of data to identify 
    complex patterns and make predictions with remarkable accuracy. Transfer learning 
    techniques allow models trained on one task to be adapted for related problems, 
    significantly reducing training time and data requirements. Reinforcement learning 
    agents learn optimal strategies through trial and error, mastering complex games 
    and real-world control tasks. The convergence of big data, powerful computing 
    infrastructure, and advanced algorithms has accelerated innovation across industries 
    including healthcare, finance, autonomous vehicles, and smart cities.
    """,
    
    'large': """
    Artificial intelligence and machine learning are transforming the technology 
    landscape in unprecedented ways. Deep learning neural networks, inspired by the 
    structure of the human brain, have enabled remarkable breakthroughs in computer 
    vision, natural language processing, and speech recognition systems. These 
    sophisticated algorithms can analyze massive datasets to identify intricate 
    patterns and generate highly accurate predictions across diverse domains.
    
    Convolutional neural networks excel at image classification and object detection 
    tasks, while recurrent architectures process sequential data for language modeling 
    and time series forecasting. Transformer models like GPT and BERT have revolutionized 
    natural language understanding by capturing long-range dependencies in text. Transfer 
    learning techniques enable models pre-trained on large corpora to be fine-tuned for 
    specific applications with limited labeled data, dramatically reducing development 
    time and computational requirements.
    
    Reinforcement learning agents learn optimal decision-making strategies through 
    iterative interaction with their environment, mastering complex games and real-world 
    control problems. Deep reinforcement learning combines neural networks with reward-based 
    learning to tackle previously intractable challenges in robotics, game playing, and 
    autonomous systems. Generative adversarial networks produce synthetic data 
    indistinguishable from real samples, enabling data augmentation and creative applications.
    
    The convergence of big data, distributed computing infrastructure, and algorithmic 
    innovations has accelerated AI adoption across industries. Healthcare systems use 
    machine learning for medical image analysis, drug discovery, and personalized treatment 
    recommendations. Financial institutions employ AI for fraud detection, algorithmic 
    trading, and risk assessment. Autonomous vehicles integrate computer vision, sensor 
    fusion, and decision-making algorithms to navigate complex environments. Smart city 
    initiatives leverage AI for traffic optimization, energy management, and public safety.
    
    However, the rapid advancement of AI also raises important ethical considerations 
    around bias, privacy, transparency, and accountability. Researchers and practitioners 
    must address these challenges to ensure AI systems are developed and deployed responsibly 
    for the benefit of society.
    """
}


def benchmark_version(extractor_class, text, version_name, iterations=10):
    """Benchmark a single version"""
    times = []
    memory_usages = []
    
    for _ in range(iterations):
        tracemalloc.start()
        start = time.perf_counter()
        
        extractor = extractor_class(lan="en", n=3, top=20)
        keywords = extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        times.append(elapsed * 1000)  # Convert to ms
        memory_usages.append(peak / 1024 / 1024)  # Convert to MB
    
    return {
        'version': version_name,
        'mean_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'mean_memory': sum(memory_usages) / len(memory_usages),
        'keywords_count': len(keywords)
    }


def print_comparison(results_v06, results_current, size_name):
    """Print formatted comparison"""
    improvement = ((results_v06['mean_time'] - results_current['mean_time']) 
                   / results_v06['mean_time'] * 100)
    speedup = results_v06['mean_time'] / results_current['mean_time']
    
    memory_improvement = ((results_v06['mean_memory'] - results_current['mean_memory']) 
                          / results_v06['mean_memory'] * 100)
    
    print(f"\n{'='*70}")
    print(f"  {size_name.upper()} TEXT")
    print(f"{'='*70}")
    print(f"\n  YAKE v0.6.0:")
    print(f"    Time:   {results_v06['mean_time']:7.2f}ms "
          f"(min: {results_v06['min_time']:.2f}ms, max: {results_v06['max_time']:.2f}ms)")
    print(f"    Memory: {results_v06['mean_memory']:7.2f} MB")
    print(f"    Keywords: {results_v06['keywords_count']}")
    
    print(f"\n  YAKE v2.0 (Current):")
    print(f"    Time:   {results_current['mean_time']:7.2f}ms "
          f"(min: {results_current['min_time']:.2f}ms, max: {results_current['max_time']:.2f}ms)")
    print(f"    Memory: {results_current['mean_memory']:7.2f} MB")
    print(f"    Keywords: {results_current['keywords_count']}")
    
    print(f"\n  IMPROVEMENT:")
    print(f"    Speed:  {improvement:+.1f}% faster ({speedup:.2f}x speedup)")
    print(f"    Memory: {memory_improvement:+.1f}% less memory")
    
    return {
        'size': size_name,
        'v06_time': results_v06['mean_time'],
        'current_time': results_current['mean_time'],
        'improvement_percent': improvement,
        'speedup': speedup,
        'v06_memory': results_v06['mean_memory'],
        'current_memory': results_current['mean_memory'],
        'memory_improvement': memory_improvement
    }


def main():
    print("="*70)
    print("  YAKE BENCHMARK: v0.6.0 vs v2.0 (Current)")
    print("="*70)
    print("\n  Otimizações Aplicadas na v2.0:")
    print("    ✅ 1. LRU Cache (@lru_cache para split_multi)")
    print("    ✅ 2. __slots__ (ComposedWord, SingleWord)")
    print("    ✅ 3. Regex Pré-compilado (_CAPITAL_LETTER_PATTERN)")
    print("    ✅ 4. Lazy Evaluation (@property para surface_form, unique_term)")
    print("    ✅ 5. defaultdict para Candidatos")
    print("    ✅ 6. List Comprehensions Otimizadas (all(), single-pass)")
    print("    ✅ 7. NumPy Optimization (nativo para listas pequenas)")
    print("    ✅ 8. Built-in Functions (truthiness, sem len())")
    print("    ✅ 9. Pré-filtering Adaptativo (pre_filter com early exit)")
    print("="*70)
    
    all_comparisons = []
    
    for size_name, text in TEST_TEXTS.items():
        print(f"\n\n🔍 Testando {size_name.upper()} text ({len(text.split())} palavras)...")
        
        print(f"  ⏳ Executando v0.6.0...")
        results_v06 = benchmark_version(KeywordExtractorV06, text, "v0.6.0", iterations=20)
        
        print(f"  ⚡ Executando v2.0...")
        results_current = benchmark_version(KeywordExtractorCurrent, text, "v2.0", iterations=20)
        
        comparison = print_comparison(results_v06, results_current, size_name)
        all_comparisons.append(comparison)
    
    # Summary
    print(f"\n\n{'='*70}")
    print("  RESUMO GERAL")
    print(f"{'='*70}")
    
    avg_v06_time = sum(c['v06_time'] for c in all_comparisons) / len(all_comparisons)
    avg_current_time = sum(c['current_time'] for c in all_comparisons) / len(all_comparisons)
    avg_improvement = sum(c['improvement_percent'] for c in all_comparisons) / len(all_comparisons)
    avg_speedup = sum(c['speedup'] for c in all_comparisons) / len(all_comparisons)
    
    avg_v06_memory = sum(c['v06_memory'] for c in all_comparisons) / len(all_comparisons)
    avg_current_memory = sum(c['current_memory'] for c in all_comparisons) / len(all_comparisons)
    avg_memory_improvement = sum(c['memory_improvement'] for c in all_comparisons) / len(all_comparisons)
    
    print(f"\n  Tempo Médio:")
    print(f"    v0.6.0: {avg_v06_time:.2f}ms")
    print(f"    v2.0:   {avg_current_time:.2f}ms")
    print(f"    Melhoria: {avg_improvement:+.1f}% ({avg_speedup:.2f}x mais rápido)")
    
    print(f"\n  Memória Média:")
    print(f"    v0.6.0: {avg_v06_memory:.2f} MB")
    print(f"    v2.0:   {avg_current_memory:.2f} MB")
    print(f"    Melhoria: {avg_memory_improvement:+.1f}%")
    
    print(f"\n{'='*70}")
    print("  🎯 RESULTADO FINAL")
    print(f"{'='*70}")
    print(f"\n  YAKE v2.0 é {avg_speedup:.1f}x MAIS RÁPIDO que v0.6.0")
    print(f"  Com {abs(avg_memory_improvement):.1f}% menos uso de memória")
    print(f"\n{'='*70}\n")
    
    # Export data for visualization
    return {
        'comparisons': all_comparisons,
        'averages': {
            'v06_time': avg_v06_time,
            'current_time': avg_current_time,
            'improvement_percent': avg_improvement,
            'speedup': avg_speedup,
            'v06_memory': avg_v06_memory,
            'current_memory': avg_current_memory,
            'memory_improvement': avg_memory_improvement
        }
    }


if __name__ == "__main__":
    results = main()
    
    # Save results for dashboard
    import json
    output_file = Path(__file__).parent / "benchmark_v06_vs_v20_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Resultados salvos em: {output_file}")
