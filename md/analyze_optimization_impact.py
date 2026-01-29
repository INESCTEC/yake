#!/usr/bin/env python3
# pylint: skip-file
"""
🔍 ANÁLISE DETALHADA DO IMPACTO DAS OTIMIZAÇÕES
===============================================
Script para medir o impacto individual de cada otimização
e identificar possíveis regressões.
"""

import sys
import time
import functools
from pathlib import Path

# Adicionar diretório yake ao path
sys.path.insert(0, str(Path(__file__).parent))

def measure_function_time(func, iterations=1000):
    """Mede tempo de execução de uma função"""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    return elapsed / iterations

def analyze_cache_impact():
    """Analisa impacto do cache LRU em get_tag()"""
    print("\n" + "="*70)
    print("1️⃣  ANÁLISE: Cache LRU em get_tag()")
    print("="*70)
    
    from yake.data.utils import get_tag
    import string
    
    exclude = frozenset(string.punctuation)
    
    # Teste 1: Palavras únicas (pior caso - sem cache hits)
    unique_words = [f"word{i}" for i in range(100)]
    
    def test_unique():
        for i, word in enumerate(unique_words):
            get_tag(word, i, exclude)
    
    # Teste 2: Palavras repetidas (melhor caso - muitos cache hits)
    repeated_words = ["python", "machine", "learning", "data"] * 25
    
    def test_repeated():
        for i, word in enumerate(repeated_words):
            get_tag(word, i, exclude)
    
    # Medir
    time_unique = measure_function_time(test_unique, iterations=100)
    time_repeated = measure_function_time(test_repeated, iterations=100)
    
    # Verificar cache info
    cache_info = get_tag.cache_info()
    
    print(f"\n📊 Resultados:")
    print(f"   Palavras únicas (100 palavras):    {time_unique*1000:.4f}ms")
    print(f"   Palavras repetidas (100 palavras): {time_repeated*1000:.4f}ms")
    print(f"   Melhoria com cache: {((time_unique - time_repeated) / time_unique * 100):.1f}%")
    
    print(f"\n💾 Cache Stats:")
    print(f"   Hits: {cache_info.hits:,}")
    print(f"   Misses: {cache_info.misses:,}")
    print(f"   Hit Rate: {(cache_info.hits / (cache_info.hits + cache_info.misses) * 100) if cache_info.hits + cache_info.misses > 0 else 0:.1f}%")
    print(f"   Tamanho atual: {cache_info.currsize:,}")
    print(f"   Tamanho máximo: {cache_info.maxsize:,}")
    
    # Análise
    if time_repeated < time_unique * 0.5:
        print("\n✅ CONCLUSÃO: Cache LRU é MUITO EFETIVO (>50% melhoria)")
        return "MANTÉM"
    elif time_repeated < time_unique * 0.8:
        print("\n⚠️  CONCLUSÃO: Cache LRU tem benefício moderado (20-50% melhoria)")
        return "MANTÉM"
    else:
        print("\n❌ CONCLUSÃO: Cache LRU tem benefício MÍNIMO (<20% melhoria)")
        return "QUESTIONÁVEL"

def analyze_slots_impact():
    """Analisa impacto do __slots__ em ComposedWord"""
    print("\n" + "="*70)
    print("2️⃣  ANÁLISE: __slots__ em ComposedWord")
    print("="*70)
    
    from yake.data.composed_word import ComposedWord
    import sys
    
    # Criar instâncias de teste
    test_data = [
        ('p', 'word1', None),
        ('n', 'Word2', None),
    ]
    
    print(f"\n📊 Análise de Memória:")
    
    # Criar objetos
    objects = []
    for i in range(100):
        obj = ComposedWord(test_data)
        objects.append(obj)
    
    # Medir tamanho
    single_size = sys.getsizeof(objects[0])
    
    print(f"   Tamanho de 1 objeto: {single_size} bytes")
    print(f"   Tamanho de 100 objetos: {single_size * 100 / 1024:.2f} KB")
    print(f"   Tamanho de 1000 objetos: {single_size * 1000 / 1024:.2f} KB")
    
    # Teste de acesso
    def test_access():
        for obj in objects[:10]:
            _ = obj.kw
            _ = obj.tags
            _ = obj.unique_kw
            _ = obj.tf
            _ = obj.h
    
    access_time = measure_function_time(test_access, iterations=1000)
    
    print(f"\n⏱️  Tempo de Acesso:")
    print(f"   50 acessos a atributos: {access_time*1000:.4f}ms")
    
    # Análise
    if single_size < 250:
        print(f"\n✅ CONCLUSÃO: __slots__ EFETIVO (objeto com {single_size} bytes)")
        return "MANTÉM"
    else:
        print(f"\n⚠️  CONCLUSÃO: __slots__ pode não ser ideal (objeto com {single_size} bytes)")
        return "REVISAR"

def analyze_regex_precompilation():
    """Analisa impacto da pré-compilação de regex"""
    print("\n" + "="*70)
    print("3️⃣  ANÁLISE: Pré-compilação de Regex")
    print("="*70)
    
    import re
    
    pattern_string = "[A-Z]"
    test_words = ["Python", "java", "JavaScript", "c++", "Ruby"] * 20
    
    # Teste 1: Compilando toda vez
    def test_without_precompile():
        for word in test_words:
            pattern = re.compile(pattern_string)
            pattern.match(word[0])
    
    # Teste 2: Com pré-compilação (como temos agora)
    precompiled = re.compile(pattern_string)
    
    def test_with_precompile():
        for word in test_words:
            precompiled.match(word[0])
    
    time_without = measure_function_time(test_without_precompile, iterations=100)
    time_with = measure_function_time(test_with_precompile, iterations=100)
    
    improvement = ((time_without - time_with) / time_without * 100)
    
    print(f"\n📊 Resultados:")
    print(f"   Sem pré-compilação: {time_without*1000:.4f}ms")
    print(f"   Com pré-compilação: {time_with*1000:.4f}ms")
    print(f"   Melhoria: {improvement:.1f}%")
    
    if improvement > 20:
        print(f"\n✅ CONCLUSÃO: Pré-compilação MUITO EFETIVA ({improvement:.1f}% melhoria)")
        return "MANTÉM"
    elif improvement > 5:
        print(f"\n⚠️  CONCLUSÃO: Pré-compilação tem benefício moderado ({improvement:.1f}% melhoria)")
        return "MANTÉM"
    else:
        print(f"\n❌ CONCLUSÃO: Pré-compilação tem benefício MÍNIMO ({improvement:.1f}% melhoria)")
        return "QUESTIONÁVEL"

def analyze_frozenset_conversion():
    """Analisa custo da conversão frozenset"""
    print("\n" + "="*70)
    print("4️⃣  ANÁLISE: Conversão Frozenset (Bug Corrigido)")
    print("="*70)
    
    import string
    
    exclude_set = set(string.punctuation)
    
    # Simulação: converter toda vez (BUG)
    def test_repeated_conversion():
        for _ in range(3600):  # Número típico de chamadas
            _ = frozenset(exclude_set)
    
    # Simulação: converter uma vez (CORRETO)
    exclude_frozen = frozenset(exclude_set)
    
    def test_single_conversion():
        for _ in range(3600):
            _ = exclude_frozen  # Apenas referência
    
    time_repeated = measure_function_time(test_repeated_conversion, iterations=10)
    time_single = measure_function_time(test_single_conversion, iterations=10)
    
    overhead = ((time_repeated - time_single) / time_single * 100)
    
    print(f"\n📊 Resultados:")
    print(f"   Conversão repetida (3600×): {time_repeated*1000:.4f}ms")
    print(f"   Conversão única (1×):       {time_single*1000:.4f}ms")
    print(f"   Overhead evitado: {overhead:.1f}%")
    print(f"   Tempo economizado: {(time_repeated - time_single)*1000:.4f}ms por execução")
    
    if overhead > 100:
        print(f"\n✅ CONCLUSÃO: Correção CRÍTICA ({overhead:.0f}% overhead eliminado)")
        return "MANTÉM (CRÍTICO)"
    else:
        print(f"\n⚠️  CONCLUSÃO: Correção importante mas não crítica ({overhead:.1f}% overhead)")
        return "MANTÉM"

def benchmark_full_pipeline():
    """Benchmark completo do pipeline YAKE"""
    print("\n" + "="*70)
    print("5️⃣  BENCHMARK: Pipeline Completo")
    print("="*70)
    
    import yake
    
    # Textos de teste de diferentes tamanhos
    small_text = """Machine learning algorithms revolutionize artificial intelligence 
    by enabling systems to learn from data patterns."""
    
    medium_text = small_text * 50
    large_text = small_text * 200
    
    texts = {
        'Pequeno (0.2KB)': small_text,
        'Médio (10KB)': medium_text,
        'Grande (40KB)': large_text
    }
    
    print(f"\n📊 Resultados de Performance:")
    
    results = {}
    for name, text in texts.items():
        times = []
        for _ in range(5):
            start = time.perf_counter()
            kw_extractor = yake.KeywordExtractor(lan='en', n=3, top=20)
            keywords = kw_extractor.extract_keywords(text)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        std_dev = (sum((t - avg_time) ** 2 for t in times) / len(times)) ** 0.5
        
        results[name] = {
            'avg': avg_time,
            'std': std_dev,
            'keywords': len(keywords)
        }
        
        print(f"\n   {name}:")
        print(f"      Tempo médio: {avg_time:.4f}s (±{std_dev:.4f}s)")
        print(f"      Keywords: {len(keywords)}")
    
    # Análise de escalabilidade
    print(f"\n📈 Análise de Escalabilidade:")
    small_avg = results['Pequeno (0.2KB)']['avg']
    medium_avg = results['Médio (10KB)']['avg']
    large_avg = results['Grande (40KB)']['avg']
    
    # Crescimento pequeno -> médio
    text_growth_1 = 50  # 50x maior
    time_growth_1 = medium_avg / small_avg
    efficiency_1 = (text_growth_1 / time_growth_1 - 1) * 100
    
    # Crescimento médio -> grande
    text_growth_2 = 4  # 4x maior
    time_growth_2 = large_avg / medium_avg
    efficiency_2 = (text_growth_2 / time_growth_2 - 1) * 100
    
    print(f"   Pequeno → Médio:")
    print(f"      Texto cresceu: {text_growth_1}x")
    print(f"      Tempo cresceu: {time_growth_1:.1f}x")
    print(f"      Eficiência: {efficiency_1:+.1f}% vs linear")
    
    print(f"   Médio → Grande:")
    print(f"      Texto cresceu: {text_growth_2}x")
    print(f"      Tempo cresceu: {time_growth_2:.1f}x")
    print(f"      Eficiência: {efficiency_2:+.1f}% vs linear")
    
    if time_growth_1 < text_growth_1 and time_growth_2 < text_growth_2:
        print(f"\n✅ CONCLUSÃO: Escalabilidade SUB-LINEAR (excelente)")
    else:
        print(f"\n⚠️  CONCLUSÃO: Escalabilidade pode ser melhorada")
    
    return results

def main():
    """Executa análise completa"""
    
    print("\n" + "🔍" * 35)
    print("🔍  ANÁLISE DETALHADA DO IMPACTO DAS OTIMIZAÇÕES")
    print("🔍" * 35)
    
    recommendations = {}
    
    try:
        # 1. Análise de Cache
        recommendations['cache_lru'] = analyze_cache_impact()
    except Exception as e:
        print(f"\n❌ Erro ao analisar cache: {e}")
        recommendations['cache_lru'] = "ERRO"
    
    try:
        # 2. Análise de __slots__
        recommendations['slots'] = analyze_slots_impact()
    except Exception as e:
        print(f"\n❌ Erro ao analisar __slots__: {e}")
        recommendations['slots'] = "ERRO"
    
    try:
        # 3. Análise de Regex
        recommendations['regex'] = analyze_regex_precompilation()
    except Exception as e:
        print(f"\n❌ Erro ao analisar regex: {e}")
        recommendations['regex'] = "ERRO"
    
    try:
        # 4. Análise de Frozenset
        recommendations['frozenset'] = analyze_frozenset_conversion()
    except Exception as e:
        print(f"\n❌ Erro ao analisar frozenset: {e}")
        recommendations['frozenset'] = "ERRO"
    
    try:
        # 5. Benchmark completo
        benchmark_results = benchmark_full_pipeline()
    except Exception as e:
        print(f"\n❌ Erro no benchmark: {e}")
        benchmark_results = None
    
    # Resumo Final
    print("\n" + "="*70)
    print("📋 RESUMO DAS RECOMENDAÇÕES")
    print("="*70)
    
    for optimization, recommendation in recommendations.items():
        status_icon = "✅" if recommendation == "MANTÉM" else "⚠️" if recommendation == "REVISAR" else "❌"
        print(f"{status_icon} {optimization.upper()}: {recommendation}")
    
    # Contagem
    keep_count = sum(1 for r in recommendations.values() if "MANTÉM" in r)
    total_count = len(recommendations)
    
    print(f"\n📊 Resultado: {keep_count}/{total_count} otimizações recomendadas para manter")
    
    if keep_count == total_count:
        print("\n🎉 CONCLUSÃO FINAL: TODAS as otimizações são benéficas!")
        print("   Recomendação: Manter TODAS as otimizações implementadas.")
    elif keep_count >= total_count * 0.75:
        print("\n👍 CONCLUSÃO FINAL: MAIORIA das otimizações são benéficas")
        print("   Recomendação: Revisar apenas as marcadas como QUESTIONÁVEL/REVISAR.")
    else:
        print("\n⚠️  CONCLUSÃO FINAL: Várias otimizações precisam de revisão")
        print("   Recomendação: Revisar cuidadosamente cada otimização.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
