#!/usr/bin/env python3
"""
🔍 PROFILING DO YAKE COM PY-INSTRUMENT
======================================
Script para fazer profiling detalhado do YAKE e identificar oportunidades de otimização.
"""

import cProfile
import pstats
import io
from pstats import SortKey
import yake
import time
from datetime import datetime

def profile_with_cprofile():
    """Profiling usando cProfile (built-in Python)"""
    
    print("🔍 PROFILING COM cProfile")
    print("=" * 60)
    
    # Texto de teste
    text = """
    Machine learning algorithms have revolutionized artificial intelligence by enabling 
    systems to learn from data without explicit programming. Deep learning neural networks, 
    particularly convolutional and recurrent architectures, have achieved remarkable success 
    in computer vision and natural language processing tasks. Researchers continue to develop 
    new techniques for training these models more efficiently and effectively.
    """ * 100  # Repetir para ter volume significativo
    
    # Configurar profiler
    profiler = cProfile.Profile()
    
    print(f"📝 Texto: {len(text)} caracteres")
    print("🚀 Iniciando profiling...")
    
    # Executar com profiling
    profiler.enable()
    
    kw_extractor = yake.KeywordExtractor(
        lan='en',
        n=3,
        dedupLim=0.7,
        top=20
    )
    keywords = kw_extractor.extract_keywords(text)
    
    profiler.disable()
    
    print(f"✅ Profiling concluído!")
    print(f"📊 Keywords extraídas: {len(keywords)}")
    print()
    
    # Análise dos resultados
    return profiler

def print_profiling_results(profiler, top_n=30):
    """Imprime resultados do profiling de forma legível"""
    
    print("=" * 60)
    print("📊 RESULTADOS DO PROFILING")
    print("=" * 60)
    print()
    
    # Criar StringIO para capturar output
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    
    # Ordenar por tempo total
    print(f"🏆 TOP {top_n} FUNÇÕES POR TEMPO TOTAL:")
    print("-" * 60)
    ps.sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(top_n)
    print(s.getvalue())
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    
    # Ordenar por tempo próprio (excluindo chamadas)
    print(f"\n⚡ TOP {top_n} FUNÇÕES POR TEMPO PRÓPRIO:")
    print("-" * 60)
    ps.sort_stats(SortKey.TIME)
    ps.print_stats(top_n)
    print(s.getvalue())
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    
    # Ordenar por número de chamadas
    print(f"\n🔁 TOP {top_n} FUNÇÕES POR NÚMERO DE CHAMADAS:")
    print("-" * 60)
    ps.sort_stats(SortKey.CALLS)
    ps.print_stats(top_n)
    print(s.getvalue())

def save_profiling_data(profiler):
    """Salva dados de profiling para análise posterior"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"yake_profile_{timestamp}.prof"
    
    profiler.dump_stats(filename)
    print(f"\n💾 Dados de profiling salvos em: {filename}")
    print(f"   Para visualizar: python -m pstats {filename}")
    print(f"   Ou use: snakeviz {filename} (requer: pip install snakeviz)")
    
    return filename

def analyze_hotspots(profiler):
    """Analisa e identifica hotspots críticos"""
    
    print("\n" + "=" * 60)
    print("🔥 ANÁLISE DE HOTSPOTS (Pontos Críticos)")
    print("=" * 60)
    
    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.CUMULATIVE)
    
    # Pegar estatísticas
    total_time = 0
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        total_time += tt
    
    print(f"\n⏱️  Tempo total de execução: {total_time:.3f}s")
    print(f"\n🎯 Funções que consomem >5% do tempo total:\n")
    
    hotspots = []
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        percentage = (tt / total_time) * 100
        if percentage > 5:
            func_name = f"{func[0]}:{func[1]}({func[2]})"
            hotspots.append({
                'function': func_name,
                'time': tt,
                'percentage': percentage,
                'calls': nc
            })
    
    # Ordenar por percentage
    hotspots.sort(key=lambda x: x['percentage'], reverse=True)
    
    for i, hotspot in enumerate(hotspots, 1):
        print(f"{i}. {hotspot['function']}")
        print(f"   ⏱️  Tempo: {hotspot['time']:.3f}s ({hotspot['percentage']:.1f}%)")
        print(f"   🔁 Chamadas: {hotspot['calls']:,}")
        print()
    
    return hotspots

def profile_specific_operation():
    """Profiling de operações específicas"""
    
    print("\n" + "=" * 60)
    print("🔬 PROFILING DE OPERAÇÕES ESPECÍFICAS")
    print("=" * 60)
    
    text = "Machine learning algorithms are used in artificial intelligence." * 50
    
    operations = {
        'Criação do extractor': lambda: yake.KeywordExtractor(lan='en', n=3, top=20),
        'Extração completa': lambda: yake.KeywordExtractor(lan='en', n=3, top=20).extract_keywords(text),
    }
    
    for op_name, op_func in operations.items():
        print(f"\n🔍 {op_name}:")
        
        # Executar 10 vezes para média
        times = []
        for _ in range(10):
            start = time.perf_counter()
            op_func()
            times.append(time.perf_counter() - start)
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"   📊 Média: {avg_time*1000:.2f}ms")
        print(f"   ⚡ Mínimo: {min_time*1000:.2f}ms")
        print(f"   🐌 Máximo: {max_time*1000:.2f}ms")

def generate_recommendations(hotspots):
    """Gera recomendações de otimização baseadas nos hotspots"""
    
    print("\n" + "=" * 60)
    print("💡 RECOMENDAÇÕES DE OTIMIZAÇÃO")
    print("=" * 60)
    print()
    
    recommendations = []
    
    for hotspot in hotspots[:5]:  # Top 5
        func = hotspot['function']
        
        # Análise baseada no nome da função
        if 'extract_keywords' in func.lower():
            recommendations.append({
                'area': 'Extração de Keywords',
                'priority': 'ALTA',
                'suggestion': 'Considere cachear resultados intermediários ou paralelizar operações'
            })
        
        elif 'stopword' in func.lower():
            recommendations.append({
                'area': 'Processamento de Stopwords',
                'priority': 'MÉDIA',
                'suggestion': 'Implemente cache para lookup de stopwords ou use estruturas mais eficientes (frozenset)'
            })
        
        elif 'graph' in func.lower() or 'edge' in func.lower():
            recommendations.append({
                'area': 'Operações de Grafo',
                'priority': 'ALTA',
                'suggestion': 'Otimize estruturas de dados do grafo ou use bibliotecas especializadas'
            })
        
        elif '__init__' in func:
            recommendations.append({
                'area': 'Inicialização de Objetos',
                'priority': 'MÉDIA',
                'suggestion': 'Use __slots__ para reduzir overhead de memória'
            })
        
        elif 'loop' in func.lower() or 'iter' in func.lower():
            recommendations.append({
                'area': 'Loops e Iterações',
                'priority': 'ALTA',
                'suggestion': 'Considere list comprehensions, NumPy ou Cython para loops críticos'
            })
    
    # Remover duplicatas
    unique_recommendations = {r['area']: r for r in recommendations}.values()
    
    for rec in sorted(unique_recommendations, key=lambda x: x['priority'], reverse=True):
        priority_emoji = '🔴' if rec['priority'] == 'ALTA' else '🟡'
        print(f"{priority_emoji} {rec['area']} (Prioridade {rec['priority']})")
        print(f"   💡 {rec['suggestion']}")
        print()

def main():
    """Função principal"""
    
    print("🔍 PROFILING COMPLETO DO YAKE")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 1. Executar profiling
        profiler = profile_with_cprofile()
        
        # 2. Imprimir resultados
        print_profiling_results(profiler)
        
        # 3. Salvar dados
        filename = save_profiling_data(profiler)
        
        # 4. Analisar hotspots
        hotspots = analyze_hotspots(profiler)
        
        # 5. Profiling de operações específicas
        profile_specific_operation()
        
        # 6. Gerar recomendações
        generate_recommendations(hotspots)
        
        print("\n" + "=" * 60)
        print("✅ PROFILING CONCLUÍDO!")
        print("=" * 60)
        print(f"\n📊 Para análise visual interativa:")
        print(f"   pip install snakeviz")
        print(f"   snakeviz {filename}")
        print()
        
    except Exception as e:
        print(f"\n❌ Erro durante profiling: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
