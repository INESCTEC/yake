#!/usr/bin/env python3
# pylint: skip-file
"""
📊 COMPARAÇÃO DE VERSÕES DO YAKE
=================================
Script para comparar performance entre diferentes versões
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path

def benchmark_version(text, version_name="atual"):
    """Benchmark de uma versão específica"""
    
    import yake
    
    times = []
    keywords_list = []
    
    # 5 execuções para obter média mais precisa
    for i in range(5):
        start = time.perf_counter()
        
        kw_extractor = yake.KeywordExtractor(
            lan='en',
            n=3,
            dedupLim=0.7,
            top=50
        )
        keywords = kw_extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        keywords_list.append(len(keywords))
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = (sum((t - avg_time) ** 2 for t in times) / len(times)) ** 0.5
    
    return {
        'version': version_name,
        'times': times,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'std_dev': std_dev,
        'keywords_count': keywords_list[0],
        'text_size': len(text)
    }

def get_test_texts():
    """Retorna conjunto de textos de teste"""
    
    base_texts = [
        """Machine learning algorithms revolutionize artificial intelligence 
        by enabling systems to learn from data patterns.""",
        
        """Climate change causes rising temperatures and extreme weather 
        events threatening ecosystems worldwide.""",
        
        """Quantum computing uses quantum mechanics phenomena like 
        superposition for information processing.""",
    ]
    
    return {
        'pequeno': "\n\n".join(base_texts * 5),
        'médio': "\n\n".join(base_texts * 50),
        'grande': "\n\n".join(base_texts * 200),
    }

def compare_versions():
    """Compara múltiplas versões"""
    
    print("📊 COMPARAÇÃO DE VERSÕES DO YAKE")
    print("=" * 70)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    texts = get_test_texts()
    
    all_results = {}
    
    for text_name, text in texts.items():
        text_size_kb = len(text.encode('utf-8')) / 1024
        
        print(f"\n🔍 Testando com texto {text_name} ({text_size_kb:.1f}KB)")
        print("-" * 70)
        
        result = benchmark_version(text, "versão atual")
        all_results[text_name] = result
        
        print(f"⏱️  Tempo médio: {result['avg_time']:.4f}s")
        print(f"   Min: {result['min_time']:.4f}s | Max: {result['max_time']:.4f}s")
        print(f"   Desvio padrão: {result['std_dev']:.4f}s")
        print(f"   Variação: {((result['max_time'] - result['min_time']) / result['avg_time'] * 100):.1f}%")
        print(f"📊 Keywords extraídas: {result['keywords_count']}")
    
    return all_results

def display_comparison_table(results):
    """Exibe tabela comparativa"""
    
    print("\n" + "=" * 70)
    print("📊 TABELA COMPARATIVA")
    print("=" * 70)
    print()
    
    print("┌" + "─"*12 + "┬" + "─"*14 + "┬" + "─"*16 + "┬" + "─"*14 + "┐")
    print("│ Tamanho    │ Tamanho (KB) │ Tempo Médio (s) │ Keywords     │")
    print("├" + "─"*12 + "┼" + "─"*14 + "┼" + "─"*16 + "┼" + "─"*14 + "┤")
    
    for text_name, result in results.items():
        size_kb = result['text_size'] / 1024
        print(f"│ {text_name:<10} │ {size_kb:>11.1f}K │ {result['avg_time']:>14.4f} │ {result['keywords_count']:>12} │")
    
    print("└" + "─"*12 + "┴" + "─"*14 + "┴" + "─"*16 + "┴" + "─"*14 + "┘")

def analyze_scalability(results):
    """Analisa escalabilidade"""
    
    print("\n" + "=" * 70)
    print("📈 ANÁLISE DE ESCALABILIDADE")
    print("=" * 70)
    print()
    
    sizes = list(results.keys())
    
    for i in range(1, len(sizes)):
        prev_size = sizes[i-1]
        curr_size = sizes[i]
        
        prev = results[prev_size]
        curr = results[curr_size]
        
        size_ratio = curr['text_size'] / prev['text_size']
        time_ratio = curr['avg_time'] / prev['avg_time']
        
        print(f"🔍 {prev_size.capitalize()} → {curr_size.capitalize()}")
        print(f"   Aumento de tamanho: {size_ratio:.2f}x")
        print(f"   Aumento de tempo: {time_ratio:.2f}x")
        
        if time_ratio < size_ratio:
            efficiency = ((size_ratio - time_ratio) / size_ratio) * 100
            print(f"   ✅ Sub-linear! {efficiency:.1f}% mais eficiente que linear")
        elif time_ratio < size_ratio * 1.2:
            print(f"   ⚠️  Aproximadamente linear")
        else:
            overhead = ((time_ratio / size_ratio) - 1) * 100
            print(f"   ❌ Super-linear! {overhead:.1f}% overhead")
        print()

def save_benchmark_results(results):
    """Salva resultados em JSON para comparação futura"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_{timestamp}.json"
    
    # Preparar dados para JSON
    json_data = {
        'timestamp': timestamp,
        'date': datetime.now().isoformat(),
        'results': {}
    }
    
    for text_name, result in results.items():
        json_data['results'][text_name] = {
            'avg_time': result['avg_time'],
            'min_time': result['min_time'],
            'max_time': result['max_time'],
            'std_dev': result['std_dev'],
            'keywords_count': result['keywords_count'],
            'text_size_bytes': result['text_size'],
            'times': result['times']
        }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"\n💾 Resultados salvos em: {filename}")
    print(f"   Use este arquivo para comparar com futuras otimizações!")
    
    return filename

def compare_with_previous(current_results):
    """Compara com benchmark anterior se existir"""
    
    print("\n" + "=" * 70)
    print("🔄 COMPARAÇÃO COM BENCHMARKS ANTERIORES")
    print("=" * 70)
    print()
    
    # Procurar arquivos de benchmark anteriores
    benchmark_files = sorted(Path('.').glob('benchmark_*.json'))
    
    if len(benchmark_files) < 2:
        print("ℹ️  Nenhum benchmark anterior encontrado para comparação")
        print("   Execute este script novamente após fazer otimizações!")
        return
    
    # Pegar penúltimo arquivo (anterior ao que acabamos de criar)
    previous_file = benchmark_files[-2]
    
    print(f"📄 Comparando com: {previous_file.name}")
    print()
    
    with open(previous_file, 'r', encoding='utf-8') as f:
        previous_data = json.load(f)
    
    previous_results = previous_data['results']
    
    print("┌" + "─"*12 + "┬" + "─"*16 + "┬" + "─"*16 + "┬" + "─"*14 + "┐")
    print("│ Tamanho    │ Tempo Anterior  │ Tempo Atual     │ Mudança      │")
    print("├" + "─"*12 + "┼" + "─"*16 + "┼" + "─"*16 + "┼" + "─"*14 + "┤")
    
    improvements = []
    
    for text_name in current_results.keys():
        if text_name in previous_results:
            prev_time = previous_results[text_name]['avg_time']
            curr_time = current_results[text_name]['avg_time']
            
            diff = curr_time - prev_time
            diff_pct = (diff / prev_time) * 100
            
            improvements.append(diff_pct)
            
            # Emoji baseado na mudança
            if diff_pct < -5:
                emoji = "✅"
            elif diff_pct < 5:
                emoji = "➖"
            else:
                emoji = "❌"
            
            print(f"│ {text_name:<10} │ {prev_time:>13.4f}s │ {curr_time:>13.4f}s │ {emoji} {diff_pct:>+7.1f}% │")
    
    print("└" + "─"*12 + "┴" + "─"*16 + "┴" + "─"*16 + "┴" + "─"*14 + "┘")
    
    if improvements:
        avg_improvement = sum(improvements) / len(improvements)
        
        print()
        if avg_improvement < -5:
            print(f"🎉 Ótimo! Melhoria média de {-avg_improvement:.1f}%")
        elif avg_improvement < 5:
            print(f"➖ Sem mudança significativa ({avg_improvement:+.1f}%)")
        else:
            print(f"⚠️  Regressão! Piora média de {avg_improvement:.1f}%")

def main():
    """Função principal"""
    
    try:
        # 1. Executar benchmarks
        results = compare_versions()
        
        # 2. Exibir tabela comparativa
        display_comparison_table(results)
        
        # 3. Analisar escalabilidade
        analyze_scalability(results)
        
        # 4. Salvar resultados
        benchmark_file = save_benchmark_results(results)
        
        # 5. Comparar com anterior
        compare_with_previous(results)
        
        print("\n" + "=" * 70)
        print("✅ BENCHMARK CONCLUÍDO!")
        print("=" * 70)
        print()
        print("💡 Próximos passos:")
        print("   1. Implemente uma otimização")
        print("   2. Execute este script novamente")
        print("   3. Compare os resultados automaticamente")
        print("   4. Valide se a otimização funcionou!")
        print()
        
    except Exception as e:
        print(f"\n❌ Erro durante benchmark: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
