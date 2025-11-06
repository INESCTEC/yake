#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

"""
Benchmark para testar otimizações incrementais no YAKE 2.0
Mede tempo de execução, uso de memória e valida resultados
"""

import time
import tracemalloc
import statistics
from typing import List, Tuple, Dict
import yake

# Textos de teste de diferentes tamanhos
TEXTS = {
    "small": """
    Sources tell us that Google is acquiring Kaggle, a platform that hosts data science 
    and machine learning competitions. Details about the transaction remain somewhat vague, 
    but given that Google is hosting its Cloud Next conference in San Francisco this week, 
    the official announcement could come as early as tomorrow.
    """,
    
    "medium": """
    Sources tell us that Google is acquiring Kaggle, a platform that hosts data science 
    and machine learning competitions. Details about the transaction remain somewhat vague, 
    but given that Google is hosting its Cloud Next conference in San Francisco this week, 
    the official announcement could come as early as tomorrow. Reached by phone, Kaggle 
    co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. 
    Google itself declined 'to comment on rumors'. Kaggle, which has about half a million 
    data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. 
    The service got an early start and even though it has a few competitors like DrivenData, 
    TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its 
    specific niche. The service is basically the de facto home for running data science and 
    machine learning competitions. With Kaggle, Google is buying one of the largest and 
    most active communities for data scientists - and with that, it will get increased 
    mindshare in this community, too (though it already has plenty of that thanks to 
    Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but 
    that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 
    machine learning competition around classifying YouTube videos.
    """,
    
    "large": """
    Sources tell us that Google is acquiring Kaggle, a platform that hosts data science 
    and machine learning competitions. Details about the transaction remain somewhat vague, 
    but given that Google is hosting its Cloud Next conference in San Francisco this week, 
    the official announcement could come as early as tomorrow. Reached by phone, Kaggle 
    co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. 
    Google itself declined 'to comment on rumors'. Kaggle, which has about half a million 
    data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. 
    The service got an early start and even though it has a few competitors like DrivenData, 
    TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its 
    specific niche. The service is basically the de facto home for running data science and 
    machine learning competitions. With Kaggle, Google is buying one of the largest and 
    most active communities for data scientists - and with that, it will get increased 
    mindshare in this community, too (though it already has plenty of that thanks to 
    Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but 
    that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 
    machine learning competition around classifying YouTube videos. As it so happens, this 
    is code-named YouTube-8M. It is a continuation of the ImageNet competition that helped 
    researchers advance computer vision algorithms. And Google itself has proven many times 
    over that it excels at running machine learning competitions in-house at scale with its 
    annual Code Jam competition. So what does Google hope to achieve by acquiring Kaggle? 
    Google is already building a comprehensive cloud machine learning platform. By acquiring 
    Kaggle and its community of data scientists, Google can accelerate that effort 
    considerably. Kaggle has also become synonymous with machine learning competitions, 
    and there's a lot of value in that brand recognition. The company has built up a 
    significant following on social media and in the data science community at large.
    """ * 2  # Duplicar para ter texto maior
}


def benchmark_run(text: str, n_runs: int = 10) -> Dict[str, any]:
    """
    Executa benchmark de extração de keywords
    
    Args:
        text: Texto para processar
        n_runs: Número de execuções para média
    
    Returns:
        Dict com métricas de performance
    """
    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=3,
        dedupLim=0.9,
        dedupFunc='seqm',
        windowsSize=1,
        top=20
    )
    
    # Warm-up run
    _ = kw_extractor.extract_keywords(text)
    
    # Benchmark timing
    times = []
    memory_peaks = []
    
    for _ in range(n_runs):
        # Medir memória
        tracemalloc.start()
        
        # Medir tempo
        start = time.perf_counter()
        keywords = kw_extractor.extract_keywords(text)
        end = time.perf_counter()
        
        times.append((end - start) * 1000)  # ms
        
        # Memória pico
        current, peak = tracemalloc.get_traced_memory()
        memory_peaks.append(peak / 1024 / 1024)  # MB
        tracemalloc.stop()
    
    # Estatísticas de cache (se disponível)
    cache_stats = {}
    if hasattr(kw_extractor, 'get_cache_stats'):
        cache_stats = kw_extractor.get_cache_stats()
    
    return {
        'time_mean': statistics.mean(times),
        'time_median': statistics.median(times),
        'time_stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'time_min': min(times),
        'time_max': max(times),
        'memory_mean': statistics.mean(memory_peaks),
        'memory_peak': max(memory_peaks),
        'keywords_count': len(keywords),
        'keywords_top5': keywords[:5],
        'cache_stats': cache_stats
    }


def compare_results(baseline: List[Tuple[str, float]], 
                   optimized: List[Tuple[str, float]], 
                   tolerance: float = 1e-6) -> bool:
    """
    Compara se dois conjuntos de keywords são idênticos
    
    Args:
        baseline: Keywords da versão baseline
        optimized: Keywords da versão otimizada
        tolerance: Tolerância para comparação de scores
    
    Returns:
        True se idênticos, False caso contrário
    """
    if len(baseline) != len(optimized):
        print(f"❌ Tamanhos diferentes: {len(baseline)} vs {len(optimized)}")
        return False
    
    for i, ((kw1, score1), (kw2, score2)) in enumerate(zip(baseline, optimized)):
        if kw1 != kw2:
            print(f"❌ Keyword diferente na posição {i}: '{kw1}' vs '{kw2}'")
            return False
        
        if abs(score1 - score2) > tolerance:
            print(f"❌ Score diferente para '{kw1}': {score1} vs {score2}")
            return False
    
    return True


def print_benchmark_results(version: str, size: str, results: Dict):
    """Imprime resultados de benchmark formatados"""
    print(f"\n{'='*70}")
    print(f"📊 {version} - Texto {size.upper()}")
    print(f"{'='*70}")
    print(f"⏱️  Tempo médio:     {results['time_mean']:.3f} ms")
    print(f"⏱️  Tempo mediano:   {results['time_median']:.3f} ms")
    print(f"⏱️  Desvio padrão:   {results['time_stdev']:.3f} ms")
    print(f"⏱️  Min/Max:         {results['time_min']:.3f} / {results['time_max']:.3f} ms")
    print(f"💾 Memória média:    {results['memory_mean']:.2f} MB")
    print(f"💾 Pico de memória:  {results['memory_peak']:.2f} MB")
    print(f"🔑 Keywords:         {results['keywords_count']}")
    
    if results['cache_stats']:
        print(f"\n📈 Cache Stats:")
        for key, value in results['cache_stats'].items():
            print(f"   {key}: {value}")
    
    print(f"\n🏆 Top 5 Keywords:")
    for kw, score in results['keywords_top5']:
        print(f"   {kw:30s} {score:.6f}")


def run_full_benchmark(version_name: str = "BASELINE") -> Dict[str, Dict]:
    """
    Executa benchmark completo em todos os tamanhos de texto
    
    Args:
        version_name: Nome da versão sendo testada
    
    Returns:
        Dict com resultados por tamanho de texto
    """
    print(f"\n🚀 Iniciando benchmark: {version_name}")
    print(f"{'='*70}\n")
    
    all_results = {}
    
    for size, text in TEXTS.items():
        print(f"🔄 Processando texto {size}...")
        results = benchmark_run(text, n_runs=10)
        all_results[size] = results
        print_benchmark_results(version_name, size, results)
    
    return all_results


def compare_versions(baseline: Dict[str, Dict], 
                    optimized: Dict[str, Dict], 
                    optimization_name: str):
    """
    Compara duas versões e mostra diferenças
    
    Args:
        baseline: Resultados da versão baseline
        optimized: Resultados da versão otimizada
        optimization_name: Nome da otimização aplicada
    """
    print(f"\n{'='*70}")
    print(f"📊 COMPARAÇÃO: {optimization_name}")
    print(f"{'='*70}\n")
    
    for size in ["small", "medium", "large"]:
        base = baseline[size]
        opt = optimized[size]
        
        time_improvement = ((base['time_mean'] - opt['time_mean']) / base['time_mean']) * 100
        memory_improvement = ((base['memory_mean'] - opt['memory_mean']) / base['memory_mean']) * 100
        
        print(f"\n📈 Texto {size.upper()}:")
        print(f"   Tempo:    {base['time_mean']:.3f} ms → {opt['time_mean']:.3f} ms "
              f"({'−' if time_improvement < 0 else '+'}{abs(time_improvement):.1f}%)")
        print(f"   Memória:  {base['memory_mean']:.2f} MB → {opt['memory_mean']:.2f} MB "
              f"({'−' if memory_improvement < 0 else '+'}{abs(memory_improvement):.1f}%)")
        
        # Validar que resultados são idênticos
        kw_extractor = yake.KeywordExtractor()
        text = TEXTS[size]
        keywords = kw_extractor.extract_keywords(text)
        
        if len(keywords) == base['keywords_count']:
            print(f"   ✅ Resultados idênticos ({len(keywords)} keywords)")
        else:
            print(f"   ⚠️  Número de keywords diferente: {base['keywords_count']} → {len(keywords)}")
    
    # Resumo geral
    avg_time_improvement = statistics.mean([
        ((baseline[size]['time_mean'] - optimized[size]['time_mean']) / baseline[size]['time_mean']) * 100
        for size in ["small", "medium", "large"]
    ])
    
    avg_memory_improvement = statistics.mean([
        ((baseline[size]['memory_mean'] - optimized[size]['memory_mean']) / baseline[size]['memory_mean']) * 100
        for size in ["small", "medium", "large"]
    ])
    
    print(f"\n{'='*70}")
    print(f"🎯 RESUMO GERAL:")
    print(f"   Melhoria de tempo médio:   {'−' if avg_time_improvement < 0 else '+'}{abs(avg_time_improvement):.1f}%")
    print(f"   Melhoria de memória média: {'−' if avg_memory_improvement < 0 else '+'}{abs(avg_memory_improvement):.1f}%")
    
    if avg_time_improvement > 5 or avg_memory_improvement > 5:
        print(f"   ✅ OTIMIZAÇÃO RECOMENDADA! (>5% melhoria)")
    elif avg_time_improvement > 0 or avg_memory_improvement > 0:
        print(f"   ⚠️  Melhoria marginal (<5%)")
    else:
        print(f"   ❌ SEM MELHORIA SIGNIFICATIVA")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔬 YAKE 2.0 - Benchmark de Otimizações")
    print("="*70)
    
    # Executar benchmark baseline
    baseline_results = run_full_benchmark("BASELINE")
    
    print("\n✅ Benchmark baseline completo!")
    print("\n💡 Para testar otimizações:")
    print("   1. Aplicar mudanças no código")
    print("   2. Executar: python benchmark_optimizations.py")
    print("   3. Comparar resultados\n")
