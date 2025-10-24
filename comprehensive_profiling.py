#!/usr/bin/env python3
"""
🎯 PROFILING COMPLETO E COMPARATIVO
===================================
Usa múltiplas ferramentas de profiling e gera relatório unificado
"""

import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Verificar ferramentas disponíveis
AVAILABLE_TOOLS = {}

try:
    import cProfile
    import pstats
    AVAILABLE_TOOLS['cProfile'] = True
except ImportError:
    AVAILABLE_TOOLS['cProfile'] = False

try:
    import pyinstrument
    AVAILABLE_TOOLS['pyinstrument'] = True
except ImportError:
    AVAILABLE_TOOLS['pyinstrument'] = False

try:
    import line_profiler
    AVAILABLE_TOOLS['line_profiler'] = True
except ImportError:
    AVAILABLE_TOOLS['line_profiler'] = False

try:
    import memory_profiler
    AVAILABLE_TOOLS['memory_profiler'] = True
except ImportError:
    AVAILABLE_TOOLS['memory_profiler'] = False

import yake

def check_tools():
    """Verifica quais ferramentas estão disponíveis"""
    print("🔍 FERRAMENTAS DE PROFILING DISPONÍVEIS")
    print("=" * 60)
    
    for tool, available in AVAILABLE_TOOLS.items():
        status = "✅" if available else "❌"
        print(f"{status} {tool}")
    
    if not any(AVAILABLE_TOOLS.values()):
        print("\n⚠️  Nenhuma ferramenta de profiling instalada!")
        print("\n📦 Para instalar todas:")
        print("   pip install pyinstrument line-profiler memory-profiler")
        return False
    
    print()
    return True

def get_test_text(size='medium'):
    """Gera texto de teste de diferentes tamanhos"""
    
    base_texts = [
        """Machine learning algorithms are revolutionizing artificial intelligence 
        by enabling systems to learn from data patterns.""",
        
        """Climate change causes rising temperatures and extreme weather events 
        that threaten ecosystems and biodiversity worldwide.""",
        
        """Quantum computing uses quantum mechanics phenomena like superposition 
        and entanglement for information processing.""",
        
        """Biotechnology advances in gene editing open possibilities for treating 
        genetic diseases with novel therapies.""",
        
        """Renewable energy sources like solar and wind power are becoming 
        cost-effective alternatives to fossil fuels."""
    ]
    
    if size == 'small':
        return "\n\n".join(base_texts * 5)
    elif size == 'medium':
        return "\n\n".join(base_texts * 50)
    elif size == 'large':
        return "\n\n".join(base_texts * 200)
    else:
        return "\n\n".join(base_texts * 50)

def benchmark_basic(text):
    """Benchmark básico sem profiling detalhado"""
    
    start = time.perf_counter()
    
    kw_extractor = yake.KeywordExtractor(
        lan='en',
        n=3,
        dedupLim=0.7,
        top=50
    )
    keywords = kw_extractor.extract_keywords(text)
    
    elapsed = time.perf_counter() - start
    
    return elapsed, len(keywords)

def profile_with_cprofile(text):
    """Profiling com cProfile"""
    
    if not AVAILABLE_TOOLS['cProfile']:
        return None
    
    print("📊 Profiling com cProfile...")
    
    import cProfile
    import pstats
    from io import StringIO
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    kw_extractor = yake.KeywordExtractor(lan='en', n=3, dedupLim=0.7, top=50)
    keywords = kw_extractor.extract_keywords(text)
    
    profiler.disable()
    
    # Capturar estatísticas
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
    
    return {
        'tool': 'cProfile',
        'keywords': len(keywords),
        'output': stream.getvalue()
    }

def profile_with_pyinstrument(text):
    """Profiling com pyinstrument"""
    
    if not AVAILABLE_TOOLS['pyinstrument']:
        return None
    
    print("📊 Profiling com pyinstrument...")
    
    import pyinstrument
    
    profiler = pyinstrument.Profiler()
    profiler.start()
    
    kw_extractor = yake.KeywordExtractor(lan='en', n=3, dedupLim=0.7, top=50)
    keywords = kw_extractor.extract_keywords(text)
    
    profiler.stop()
    
    # Gerar HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = f"profile_pyinstrument_{timestamp}.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(profiler.output_html())
    
    return {
        'tool': 'pyinstrument',
        'keywords': len(keywords),
        'html_file': html_file,
        'output': profiler.output_text(unicode=True)
    }

def compare_performance():
    """Compara performance com diferentes tamanhos"""
    
    print("\n" + "=" * 60)
    print("📈 ANÁLISE COMPARATIVA DE PERFORMANCE")
    print("=" * 60)
    
    sizes = {
        'pequeno': 'small',
        'médio': 'medium',
        'grande': 'large'
    }
    
    results = []
    
    for name, size in sizes.items():
        text = get_test_text(size)
        text_size_kb = len(text.encode('utf-8')) / 1024
        
        print(f"\n🔍 Testando com texto {name} ({text_size_kb:.1f}KB)...")
        
        # Fazer 3 medições e tirar média
        times = []
        for i in range(3):
            elapsed, num_keywords = benchmark_basic(text)
            times.append(elapsed)
            print(f"   Execução {i+1}: {elapsed:.3f}s")
        
        avg_time = sum(times) / len(times)
        
        results.append({
            'name': name,
            'size_kb': text_size_kb,
            'avg_time': avg_time,
            'keywords': num_keywords
        })
        
        print(f"   ⏱️  Média: {avg_time:.3f}s")
        print(f"   📊 Keywords: {num_keywords}")
    
    # Tabela resumo
    print("\n📊 RESUMO COMPARATIVO:")
    print("┌" + "─"*12 + "┬" + "─"*14 + "┬" + "─"*14 + "┬" + "─"*12 + "┐")
    print("│ Tamanho    │ Tamanho (KB) │ Tempo Médio  │ Keywords   │")
    print("├" + "─"*12 + "┼" + "─"*14 + "┼" + "─"*14 + "┼" + "─"*12 + "┤")
    
    for r in results:
        name = f"{r['name']}"
        size = f"{r['size_kb']:.1f}KB"
        time_s = f"{r['avg_time']:.3f}s"
        kw = f"{r['keywords']}"
        print(f"│ {name:<10} │ {size:<12} │ {time_s:<12} │ {kw:<10} │")
    
    print("└" + "─"*12 + "┴" + "─"*14 + "┴" + "─"*14 + "┴" + "─"*12 + "┘")
    
    return results

def generate_recommendations(results):
    """Gera recomendações baseadas nos resultados"""
    
    print("\n" + "=" * 60)
    print("💡 RECOMENDAÇÕES DE OTIMIZAÇÃO")
    print("=" * 60)
    print()
    
    print("🎯 Áreas para investigar:")
    print()
    print("1. 🔍 Hotspots Principais:")
    print("   • Verifique funções que aparecem no topo do perfil")
    print("   • Procure por operações repetidas em loops")
    print("   • Identifique acessos frequentes a estruturas de dados")
    print()
    
    print("2. 📊 Estruturas de Dados:")
    print("   • Avalie se dicionários/listas são acessados eficientemente")
    print("   • Considere usar sets para operações de busca/pertencimento")
    print("   • Verifique se há cópias desnecessárias de dados")
    print()
    
    print("3. 🔄 Algoritmos:")
    print("   • Identifique algoritmos com complexidade quadrática (O(n²))")
    print("   • Procure por oportunidades de cache/memoização")
    print("   • Verifique se há cálculos redundantes")
    print()
    
    print("4. 🧪 Próximos Passos:")
    print("   • Use line_profiler para análise linha-a-linha das funções lentas")
    print("   • Use memory_profiler para identificar uso excessivo de memória")
    print("   • Compare com versões anteriores do código")
    print("   • Teste otimizações isoladamente")
    print()

def save_report(results, profiling_results):
    """Salva relatório completo em arquivo"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"profiling_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RELATÓRIO DE PROFILING DO YAKE\n")
        f.write("=" * 60 + "\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")
        
        f.write("FERRAMENTAS USADAS:\n")
        for tool, available in AVAILABLE_TOOLS.items():
            status = "SIM" if available else "NÃO"
            f.write(f"  - {tool}: {status}\n")
        f.write("\n")
        
        f.write("RESULTADOS DE PERFORMANCE:\n")
        for r in results:
            f.write(f"\n{r['name'].upper()}:\n")
            f.write(f"  Tamanho: {r['size_kb']:.1f}KB\n")
            f.write(f"  Tempo: {r['avg_time']:.3f}s\n")
            f.write(f"  Keywords: {r['keywords']}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("RESULTADOS DETALHADOS DO PROFILING:\n")
        f.write("=" * 60 + "\n\n")
        
        for pr in profiling_results:
            if pr:
                f.write(f"\n--- {pr['tool']} ---\n\n")
                f.write(pr['output'])
                f.write("\n\n")
    
    print(f"\n💾 Relatório completo salvo em: {report_file}")
    return report_file

def main():
    """Função principal"""
    
    print("🎯 PROFILING COMPLETO DO YAKE")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar ferramentas
    if not check_tools():
        sys.exit(1)
    
    try:
        # 1. Análise comparativa de performance
        print("\n🚀 Iniciando análise comparativa...")
        performance_results = compare_performance()
        
        # 2. Profiling detalhado com texto médio
        print("\n" + "=" * 60)
        print("🔬 PROFILING DETALHADO (texto médio)")
        print("=" * 60)
        
        text = get_test_text('medium')
        print(f"\n📝 Texto: {len(text):,} caracteres\n")
        
        profiling_results = []
        
        # cProfile
        result = profile_with_cprofile(text)
        if result:
            profiling_results.append(result)
            print("✅ cProfile concluído")
        
        # pyinstrument
        result = profile_with_pyinstrument(text)
        if result:
            profiling_results.append(result)
            print(f"✅ pyinstrument concluído")
            if 'html_file' in result:
                print(f"   📄 HTML: {result['html_file']}")
        
        # 3. Gerar recomendações
        generate_recommendations(performance_results)
        
        # 4. Salvar relatório
        report_file = save_report(performance_results, profiling_results)
        
        # 5. Resumo final
        print("\n" + "=" * 60)
        print("✅ PROFILING CONCLUÍDO!")
        print("=" * 60)
        print(f"\n📄 Arquivos gerados:")
        print(f"   • {report_file}")
        
        for pr in profiling_results:
            if 'html_file' in pr:
                print(f"   • {pr['html_file']}")
        
        print("\n💡 Próximos passos:")
        print("   1. Revise os hotspots identificados")
        print("   2. Analise as funções mais lentas linha a linha")
        print("   3. Implemente otimizações incrementais")
        print("   4. Re-execute este script para validar melhorias")
        print()
        
    except Exception as e:
        print(f"\n❌ Erro durante profiling: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
