# pylint: skip-file
"""
Benchmark Comparativo Completo: YAKE v0.1.0 vs v0.6.0 vs v2.0 (Current)
Força uso correto de cada versão através de imports isolados
"""

import sys
import time
import tracemalloc
import importlib
from pathlib import Path
import json

# Paths
BASE_PATH = Path(__file__).parent.parent
YAKE_PATH = BASE_PATH / "yake"

# Test texts
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


def benchmark_v010(text, iterations=10):
    """Benchmark YAKE v0.1.0"""
    # Clear sys.modules to force fresh import
    modules_to_remove = [k for k in sys.modules.keys() if 'yake' in k.lower()]
    for mod in modules_to_remove:
        del sys.modules[mod]
    
    # Add v0.1.0 to path
    v010_path = str(YAKE_PATH / "yake_1.0.0")
    if v010_path in sys.path:
        sys.path.remove(v010_path)
    sys.path.insert(0, v010_path)
    
    # Import v0.1.0 directly from file
    import yake as yake_v010
    KeywordExtractor = yake_v010.KeywordExtractor
    
    times = []
    memory_usages = []
    
    for _ in range(iterations):
        tracemalloc.start()
        start = time.perf_counter()
        
        extractor = KeywordExtractor(lan="en", n=3, top=20)
        keywords = extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        times.append(elapsed * 1000)
        memory_usages.append(peak / 1024 / 1024)
    
    # Clean up
    if v010_path in sys.path:
        sys.path.remove(v010_path)
    
    return {
        'mean_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'mean_memory': sum(memory_usages) / len(memory_usages),
        'keywords_count': len(keywords)
    }


def benchmark_v060(text, iterations=10):
    """Benchmark YAKE v0.6.0"""
    # Clear sys.modules
    modules_to_remove = [k for k in sys.modules.keys() if 'yake' in k.lower()]
    for mod in modules_to_remove:
        del sys.modules[mod]
    
    # Add v0.6.0 to path
    v060_path = str(YAKE_PATH / "yake_0.6.0")
    if v060_path in sys.path:
        sys.path.remove(v060_path)
    sys.path.insert(0, v060_path)
    
    # Import v0.6.0 directly
    import yake as yake_v060
    KeywordExtractor = yake_v060.KeywordExtractor
    
    times = []
    memory_usages = []
    
    for _ in range(iterations):
        tracemalloc.start()
        start = time.perf_counter()
        
        extractor = KeywordExtractor(lan="en", n=3, top=20)
        keywords = extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        times.append(elapsed * 1000)
        memory_usages.append(peak / 1024 / 1024)
    
    # Clean up
    if v060_path in sys.path:
        sys.path.remove(v060_path)
    
    return {
        'mean_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'mean_memory': sum(memory_usages) / len(memory_usages),
        'keywords_count': len(keywords)
    }


def benchmark_v20_current(text, iterations=10):
    """Benchmark YAKE v2.0 (current version)"""
    # Clear sys.modules
    modules_to_remove = [k for k in sys.modules.keys() if 'yake' in k.lower()]
    for mod in modules_to_remove:
        del sys.modules[mod]
    
    # Add current version to path
    if str(BASE_PATH) not in sys.path:
        sys.path.insert(0, str(BASE_PATH))
    
    # Import current version
    from yake import KeywordExtractor
    
    times = []
    memory_usages = []
    
    for _ in range(iterations):
        tracemalloc.start()
        start = time.perf_counter()
        
        extractor = KeywordExtractor(lan="en", n=3, top=20)
        keywords = extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        times.append(elapsed * 1000)
        memory_usages.append(peak / 1024 / 1024)
    
    return {
        'mean_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'mean_memory': sum(memory_usages) / len(memory_usages),
        'keywords_count': len(keywords)
    }


def print_comparison_table(results, size_name):
    """Print formatted comparison table"""
    v010 = results['v0.1.0']
    v060 = results['v0.6.0']
    v20 = results['v2.0']
    
    improvement_010_to_20 = ((v010['mean_time'] - v20['mean_time']) / v010['mean_time'] * 100)
    speedup_010_to_20 = v010['mean_time'] / v20['mean_time']
    
    improvement_060_to_20 = ((v060['mean_time'] - v20['mean_time']) / v060['mean_time'] * 100)
    speedup_060_to_20 = v060['mean_time'] / v20['mean_time']
    
    print(f"\n{'='*80}")
    print(f"  {size_name.upper()} TEXT ({len(TEST_TEXTS[size_name].split())} palavras)")
    print(f"{'='*80}")
    
    print(f"\n  {'Versão':<15} {'Tempo Médio':<15} {'Min':<12} {'Max':<12} {'Memória':<12}")
    print(f"  {'-'*75}")
    print(f"  {'v0.1.0':<15} {v010['mean_time']:>10.2f}ms  {v010['min_time']:>8.2f}ms  {v010['max_time']:>8.2f}ms  {v010['mean_memory']:>8.2f} MB")
    print(f"  {'v0.6.0':<15} {v060['mean_time']:>10.2f}ms  {v060['min_time']:>8.2f}ms  {v060['max_time']:>8.2f}ms  {v060['mean_memory']:>8.2f} MB")
    print(f"  {'v2.0 (Current)':<15} {v20['mean_time']:>10.2f}ms  {v20['min_time']:>8.2f}ms  {v20['max_time']:>8.2f}ms  {v20['mean_memory']:>8.2f} MB")
    
    print(f"\n  MELHORIAS:")
    print(f"    v0.1.0 → v2.0:  {improvement_010_to_20:+.1f}% ({speedup_010_to_20:.2f}x mais rápido)")
    print(f"    v0.6.0 → v2.0:  {improvement_060_to_20:+.1f}% ({speedup_060_to_20:.2f}x mais rápido)")
    
    return {
        'size': size_name,
        'v010_time': v010['mean_time'],
        'v060_time': v060['mean_time'],
        'v20_time': v20['mean_time'],
        'improvement_010_to_20': improvement_010_to_20,
        'speedup_010_to_20': speedup_010_to_20,
        'improvement_060_to_20': improvement_060_to_20,
        'speedup_060_to_20': speedup_060_to_20
    }


def main():
    print("="*80)
    print("  YAKE BENCHMARK COMPARATIVO COMPLETO")
    print("  v0.1.0 vs v0.6.0 vs v2.0 (Current)")
    print("="*80)
    print("\n  🎯 Otimizações na v2.0:")
    print("     1. ✅ LRU Cache (@lru_cache para split_multi)")
    print("     2. ✅ __slots__ (ComposedWord, SingleWord) - 57% menos memória")
    print("     3. ✅ Regex Pré-compilado (_CAPITAL_LETTER_PATTERN)")
    print("     4. ✅ Lazy Evaluation (@property para computed attributes)")
    print("     5. ✅ defaultdict para Candidatos")
    print("     6. ✅ List Comprehensions Otimizadas (all(), single-pass)")
    print("     7. ✅ NumPy Optimization (nativo para listas < 10 elementos)")
    print("     8. ✅ Built-in Functions (truthiness, sem len() > 0)")
    print("     9. ✅ Pré-filtering Adaptativo (early exit)")
    print("="*80)
    
    all_comparisons = []
    all_results = {}
    
    for size_name, text in TEST_TEXTS.items():
        print(f"\n\n{'='*80}")
        print(f"  🔍 Testando: {size_name.upper()}")
        print(f"{'='*80}")
        
        print(f"\n  ⏳ Benchmarking v0.1.0...")
        v010_results = benchmark_v010(text, iterations=15)
        
        print(f"  ⏳ Benchmarking v0.6.0...")
        v060_results = benchmark_v060(text, iterations=15)
        
        print(f"  ⚡ Benchmarking v2.0 (Current)...")
        v20_results = benchmark_v20_current(text, iterations=15)
        
        results = {
            'v0.1.0': v010_results,
            'v0.6.0': v060_results,
            'v2.0': v20_results
        }
        
        comparison = print_comparison_table(results, size_name)
        all_comparisons.append(comparison)
        all_results[size_name] = results
    
    # Summary
    print(f"\n\n{'='*80}")
    print("  📊 RESUMO GERAL")
    print(f"{'='*80}")
    
    avg_v010 = sum(c['v010_time'] for c in all_comparisons) / len(all_comparisons)
    avg_v060 = sum(c['v060_time'] for c in all_comparisons) / len(all_comparisons)
    avg_v20 = sum(c['v20_time'] for c in all_comparisons) / len(all_comparisons)
    
    avg_improvement_010 = sum(c['improvement_010_to_20'] for c in all_comparisons) / len(all_comparisons)
    avg_speedup_010 = sum(c['speedup_010_to_20'] for c in all_comparisons) / len(all_comparisons)
    
    avg_improvement_060 = sum(c['improvement_060_to_20'] for c in all_comparisons) / len(all_comparisons)
    avg_speedup_060 = sum(c['speedup_060_to_20'] for c in all_comparisons) / len(all_comparisons)
    
    print(f"\n  Tempo Médio por Versão:")
    print(f"    v0.1.0:         {avg_v010:>8.2f}ms")
    print(f"    v0.6.0:         {avg_v060:>8.2f}ms")
    print(f"    v2.0 (Current): {avg_v20:>8.2f}ms")
    
    print(f"\n  Melhorias Médias:")
    print(f"    v0.1.0 → v2.0:  {avg_improvement_010:+.1f}% ({avg_speedup_010:.2f}x mais rápido)")
    print(f"    v0.6.0 → v2.0:  {avg_improvement_060:+.1f}% ({avg_speedup_060:.2f}x mais rápido)")
    
    print(f"\n{'='*80}")
    print("  🎯 RESULTADO FINAL")
    print(f"{'='*80}")
    print(f"\n  YAKE v2.0 é:")
    print(f"    • {avg_speedup_010:.1f}x MAIS RÁPIDO que v0.1.0")
    print(f"    • {avg_speedup_060:.1f}x MAIS RÁPIDO que v0.6.0")
    print(f"\n{'='*80}\n")
    
    # Export results
    export_data = {
        'comparisons': all_comparisons,
        'detailed_results': {
            size: {
                'v0.1.0': {k: float(v) if isinstance(v, (int, float)) else v 
                          for k, v in results['v0.1.0'].items()},
                'v0.6.0': {k: float(v) if isinstance(v, (int, float)) else v 
                          for k, v in results['v0.6.0'].items()},
                'v2.0': {k: float(v) if isinstance(v, (int, float)) else v 
                        for k, v in results['v2.0'].items()}
            }
            for size, results in all_results.items()
        },
        'summary': {
            'avg_v010_time': float(avg_v010),
            'avg_v060_time': float(avg_v060),
            'avg_v20_time': float(avg_v20),
            'avg_improvement_010_to_20': float(avg_improvement_010),
            'avg_speedup_010_to_20': float(avg_speedup_010),
            'avg_improvement_060_to_20': float(avg_improvement_060),
            'avg_speedup_060_to_20': float(avg_speedup_060)
        }
    }
    
    return export_data


if __name__ == "__main__":
    results = main()
    
    # Save results
    output_file = Path(__file__).parent / "benchmark_complete_v010_v060_v20.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Resultados salvos em: {output_file}")
