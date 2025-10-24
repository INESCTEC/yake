#!/usr/bin/env python3
"""
🎯 PROFILING COM PY-INSTRUMENT
==============================
Script para profiling avançado usando py-instrument
"""

import sys
import time
from datetime import datetime

# Verificar se py-instrument está instalado
try:
    import pyinstrument
    HAS_PYINSTRUMENT = True
except ImportError:
    HAS_PYINSTRUMENT = False
    print("⚠️  py-instrument não está instalado!")
    print("   Instale com: pip install pyinstrument")
    print()

import yake

def profile_with_pyinstrument():
    """Profiling usando pyinstrument (mais moderno e visual)"""
    
    if not HAS_PYINSTRUMENT:
        print("❌ Não é possível executar sem pyinstrument")
        return None
    
    print("🎯 PROFILING COM PYINSTRUMENT")
    print("=" * 60)
    
    # Texto de teste mais substancial
    texts = [
        """Machine learning algorithms have revolutionized artificial intelligence by enabling 
        systems to learn from data without explicit programming. Deep learning neural networks, 
        particularly convolutional and recurrent architectures, have achieved remarkable success.""",
        
        """Climate change represents one of the most pressing challenges, with rising global 
        temperatures causing melting ice caps and extreme weather events that threaten biodiversity.""",
        
        """Quantum computing leverages quantum mechanical phenomena such as superposition and 
        entanglement to process information in ways that classical computers cannot achieve.""",
        
        """Biotechnology advances in gene editing, particularly CRISPR-Cas9 technology, have 
        opened new possibilities for treating genetic diseases and developing novel therapies.""",
        
        """Renewable energy sources including solar photovoltaic panels and wind turbines are 
        becoming cost-effective alternatives to fossil fuels in the global energy transition."""
    ]
    
    # Criar texto maior
    test_text = "\n\n".join(texts * 50)
    
    print(f"📝 Texto: {len(test_text):,} caracteres")
    print(f"📊 Configuração: n=3, top=50")
    print("🚀 Iniciando profiling...\n")
    
    # Criar profiler
    profiler = pyinstrument.Profiler()
    
    # Iniciar profiling
    profiler.start()
    
    # Código a ser perfilado
    kw_extractor = yake.KeywordExtractor(
        lan='en',
        n=3,
        dedupLim=0.7,
        top=50
    )
    keywords = kw_extractor.extract_keywords(test_text)
    
    # Parar profiling
    profiler.stop()
    
    print(f"✅ Profiling concluído!")
    print(f"📊 Keywords extraídas: {len(keywords)}\n")
    
    return profiler

def display_pyinstrument_results(profiler):
    """Exibe resultados do pyinstrument"""
    
    if profiler is None:
        return
    
    print("=" * 60)
    print("📊 RESULTADOS DO PROFILING (Console)")
    print("=" * 60)
    print()
    
    # Mostrar no console (unicode para melhor visualização)
    print(profiler.output_text(unicode=True, color=True))

def save_pyinstrument_html(profiler):
    """Salva relatório HTML interativo"""
    
    if profiler is None:
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_filename = f"yake_profile_{timestamp}.html"
    
    # Gerar HTML
    html_output = profiler.output_html()
    
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"\n💾 Relatório HTML salvo em: {html_filename}")
    print(f"   Abra no navegador para visualização interativa!")
    
    return html_filename

def profile_incremental_sizes():
    """Profiling com diferentes tamanhos de texto"""
    
    if not HAS_PYINSTRUMENT:
        return
    
    print("\n" + "=" * 60)
    print("📈 PROFILING COM TAMANHOS INCREMENTAIS")
    print("=" * 60)
    
    base_text = """Machine learning algorithms are used in artificial intelligence 
    systems for data processing and pattern recognition tasks."""
    
    sizes = [100, 500, 1000, 5000]
    results = []
    
    for size in sizes:
        text = (base_text + "\n") * size
        text_size_kb = len(text.encode('utf-8')) / 1024
        
        print(f"\n🔍 Testando com {size} repetições ({text_size_kb:.1f}KB)...")
        
        profiler = pyinstrument.Profiler()
        profiler.start()
        
        start_time = time.perf_counter()
        
        kw_extractor = yake.KeywordExtractor(lan='en', n=3, top=20)
        keywords = kw_extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start_time
        
        profiler.stop()
        
        # Extrair informações do profiler
        session = profiler.last_session
        total_time = session.duration
        
        results.append({
            'size': size,
            'kb': text_size_kb,
            'time': elapsed,
            'keywords': len(keywords),
            'profile_time': total_time
        })
        
        print(f"   ⏱️  Tempo: {elapsed:.3f}s")
        print(f"   📊 Keywords: {len(keywords)}")
    
    # Análise de escalabilidade
    print("\n📊 ANÁLISE DE ESCALABILIDADE:")
    print("┌" + "─"*10 + "┬" + "─"*12 + "┬" + "─"*12 + "┬" + "─"*12 + "┐")
    print("│ Tamanho  │ KB         │ Tempo (s)  │ Keywords   │")
    print("├" + "─"*10 + "┼" + "─"*12 + "┼" + "─"*12 + "┼" + "─"*12 + "┤")
    
    for r in results:
        size = f"{r['size']}"
        kb = f"{r['kb']:.1f}KB"
        time_s = f"{r['time']:.3f}s"
        kw = f"{r['keywords']}"
        print(f"│ {size:<8} │ {kb:<10} │ {time_s:<10} │ {kw:<10} │")
    
    print("└" + "─"*10 + "┴" + "─"*12 + "┴" + "─"*12 + "┴" + "─"*12 + "┘")
    
    # Calcular complexidade
    if len(results) >= 2:
        size_ratio = results[-1]['size'] / results[0]['size']
        time_ratio = results[-1]['time'] / results[0]['time']
        
        print(f"\n📈 Escalabilidade:")
        print(f"   Aumento de tamanho: {size_ratio:.1f}x")
        print(f"   Aumento de tempo: {time_ratio:.1f}x")
        
        if time_ratio < size_ratio * 1.5:
            print(f"   ✅ Escalabilidade sub-linear (boa!)")
        elif time_ratio < size_ratio * 2:
            print(f"   ⚠️  Escalabilidade linear")
        else:
            print(f"   ❌ Escalabilidade super-linear (preocupante)")

def analyze_function_hierarchy(profiler):
    """Analisa hierarquia de chamadas de função"""
    
    if profiler is None or not HAS_PYINSTRUMENT:
        return
    
    print("\n" + "=" * 60)
    print("🌳 HIERARQUIA DE CHAMADAS (Top Functions)")
    print("=" * 60)
    print()
    
    # Obter frame raiz
    session = profiler.last_session
    root_frame = session.root_frame()
    
    def print_frame_tree(frame, indent=0, max_depth=4):
        """Imprime árvore de frames recursivamente"""
        if indent >= max_depth:
            return
        
        # Calcular percentagem do tempo total
        total_time = session.duration
        percentage = (frame.time() / total_time) * 100 if total_time > 0 else 0
        
        # Só mostrar se consumir mais de 1% do tempo
        if percentage < 1.0 and indent > 0:
            return
        
        prefix = "  " * indent + ("└─ " if indent > 0 else "")
        
        # Nome da função
        func_name = frame.function
        if len(func_name) > 60:
            func_name = func_name[:57] + "..."
        
        print(f"{prefix}{func_name}")
        print(f"{'  ' * (indent + 1)}⏱️  {frame.time():.3f}s ({percentage:.1f}%)")
        
        # Processar children ordenados por tempo
        children = sorted(frame.children, key=lambda f: f.time(), reverse=True)
        for child in children[:5]:  # Top 5 children
            print_frame_tree(child, indent + 1, max_depth)
    
    print_frame_tree(root_frame)

def main():
    """Função principal"""
    
    print("🎯 PROFILING AVANÇADO DO YAKE COM PYINSTRUMENT")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not HAS_PYINSTRUMENT:
        print("📦 Para instalar pyinstrument:")
        print("   pip install pyinstrument")
        print()
        print("🎯 Pyinstrument oferece:")
        print("   ✅ Visualização mais clara")
        print("   ✅ Relatórios HTML interativos")
        print("   ✅ Overhead menor que cProfile")
        print("   ✅ Melhor para identificar hotspots")
        print()
        sys.exit(1)
    
    try:
        # 1. Profiling principal
        profiler = profile_with_pyinstrument()
        
        # 2. Mostrar resultados no console
        display_pyinstrument_results(profiler)
        
        # 3. Salvar HTML
        html_file = save_pyinstrument_html(profiler)
        
        # 4. Análise de hierarquia
        analyze_function_hierarchy(profiler)
        
        # 5. Profiling incremental
        profile_incremental_sizes()
        
        print("\n" + "=" * 60)
        print("✅ PROFILING CONCLUÍDO!")
        print("=" * 60)
        
        if html_file:
            print(f"\n🌐 Para visualização interativa, abra:")
            print(f"   {html_file}")
        
        print("\n💡 DICAS:")
        print("   • Procure por funções que consomem >10% do tempo")
        print("   • Identifique loops ou recursões excessivas")
        print("   • Verifique operações de I/O ou acessos repetidos")
        print("   • Compare com versões anteriores para validar otimizações")
        print()
        
    except Exception as e:
        print(f"\n❌ Erro durante profiling: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
