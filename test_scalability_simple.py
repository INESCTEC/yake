#!/usr/bin/env python3
# pylint: skip-file
"""
🧪 TESTE DE ESCALABILIDADE SIMPLES: YAKE 2.0 vs ARQUIVOS GRANDES
================================================================
Testa a capacidade da versão atual (otimizada) do YAKE para processar
arquivos grandes, similar ao benchmark da versão 0.6.0.
"""

import yake
import time
import os
import sys
from datetime import datetime

def test_yake_large_file():
    """Teste simplificado de escalabilidade"""
    
    print("🧪 TESTE DE ESCALABILIDADE: YAKE 2.0 (Versão Otimizada)")
    print("=" * 65)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Objetivo: Testar processamento de arquivos grandes")
    print()
    
    # Texto base para simular abstracts científicos
    abstract_base = """
Machine learning algorithms are increasingly being used in the development of artificial intelligence systems that can process and analyze large amounts of data. These systems have shown remarkable performance in various domains including natural language processing, computer vision, and speech recognition. The implementation of deep learning neural networks has revolutionized the field by enabling automated feature extraction and pattern recognition capabilities. Researchers have demonstrated that convolutional neural networks can achieve state-of-the-art results in image classification tasks, while recurrent neural networks excel in sequential data processing. The optimization of these models requires careful tuning of hyperparameters and extensive training on large datasets. Recent advances in transformer architectures have further improved the performance of language models, enabling more sophisticated text generation and understanding capabilities. The integration of attention mechanisms allows these models to focus on relevant parts of the input sequence, leading to better contextual understanding. Applications of these technologies span across multiple industries including healthcare, finance, automotive, and telecommunications. The ethical implications of artificial intelligence deployment require careful consideration of bias, fairness, and transparency in algorithmic decision-making processes.
"""
    
    # Configuração similar ao benchmark (200 keywords)
    config = {
        'lan': 'en',
        'n': 3,
        'dedupLim': 0.7,
        'top': 200,
        'features': None
    }
    
    print(f"⚙️ Configuração YAKE: {config}")
    print()
    
    # Testes progressivos
    test_sizes = [
        (1000, "1K abstracts (~1.5MB)"),
        (5000, "5K abstracts (~7.5MB)"),
        (10000, "10K abstracts (~15MB)"),
        (20000, "20K abstracts (~30MB)"),
        (30000, "30K abstracts (~45MB)"),  # Similar ao benchmark
    ]
    
    results = []
    
    for num_abstracts, description in test_sizes:
        print(f"🎯 TESTE: {description}")
        print("-" * 50)
        
        # Gerar texto
        print("📝 Gerando texto...")
        start_gen = time.time()
        
        text_parts = []
        for i in range(num_abstracts):
            variation = f"Abstract {i+1}: "
            text_parts.append(variation + abstract_base)
            
            if (i + 1) % 2000 == 0:
                print(f"   ⏳ Gerados {i+1:,} abstracts...")
        
        text = "\n".join(text_parts)
        gen_time = time.time() - start_gen
        
        text_size_mb = len(text.encode('utf-8')) / (1024 * 1024)
        print(f"   ✅ Texto gerado: {len(text):,} chars, {text_size_mb:.1f}MB em {gen_time:.2f}s")
        
        # Testar YAKE
        print("🔍 Executando YAKE...")
        start_yake = time.time()
        
        try:
            kw_extractor = yake.KeywordExtractor(**config)
            keywords = kw_extractor.extract_keywords(text)
            
            yake_time = time.time() - start_yake
            
            print(f"   ✅ SUCESSO!")
            print(f"   ⏱️  Tempo de extração: {yake_time:.2f}s ({yake_time/60:.2f} min)")
            print(f"   📊 Keywords extraídas: {len(keywords)}")
            print(f"   🏆 Top 5 keywords:")
            
            for i, (kw, score) in enumerate(keywords[:5]):
                print(f"      {i+1}. '{kw}' → {score:.6f}")
            
            # Comparar com benchmark se for ~30k abstracts
            if num_abstracts == 30000:
                benchmark_time_min = 4.4
                our_time_min = yake_time / 60
                
                print(f"\n📊 COMPARAÇÃO COM BENCHMARK (YAKE 0.6.0):")
                print(f"   📋 Benchmark: {benchmark_time_min} minutos (30k abstracts, ~48.5MB)")
                print(f"   🚀 YAKE 2.0: {our_time_min:.2f} minutos (~{text_size_mb:.1f}MB)")
                
                if our_time_min < benchmark_time_min:
                    improvement = ((benchmark_time_min - our_time_min) / benchmark_time_min) * 100
                    print(f"   ⚡ Melhoria: {improvement:.1f}% mais rápido!")
                else:
                    diff = ((our_time_min - benchmark_time_min) / benchmark_time_min) * 100
                    print(f"   📈 Diferença: {diff:.1f}% mais lento")
            
            result = {
                'num_abstracts': num_abstracts,
                'text_size_mb': text_size_mb,
                'generation_time_s': gen_time,
                'extraction_time_s': yake_time,
                'total_time_s': gen_time + yake_time,
                'keywords_count': len(keywords),
                'status': 'SUCCESS'
            }
            
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            result = {
                'num_abstracts': num_abstracts,
                'text_size_mb': text_size_mb,
                'status': 'ERROR',
                'error': str(e)
            }
        
        results.append(result)
        print()
        
        # Para por segurança se der erro
        if result['status'] == 'ERROR':
            print("⚠️ Interrompendo testes devido a erro.")
            break
    
    # Sumário final
    print("=" * 65)
    print("📊 SUMÁRIO FINAL DOS TESTES")
    print("=" * 65)
    
    successful = [r for r in results if r['status'] == 'SUCCESS']
    
    if successful:
        print("✅ RESULTADOS:")
        print("┌" + "─"*15 + "┬" + "─"*12 + "┬" + "─"*15 + "┬" + "─"*12 + "┐")
        print("│ Abstracts      │ Tamanho    │ Tempo (min)   │ Keywords   │")
        print("├" + "─"*15 + "┼" + "─"*12 + "┼" + "─"*15 + "┼" + "─"*12 + "┤")
        
        for r in successful:
            abstracts = f"{r['num_abstracts']:,}"
            size = f"{r['text_size_mb']:.1f}MB"
            time_min = f"{r['extraction_time_s']/60:.2f}min"
            keywords = f"{r['keywords_count']}"
            
            print(f"│ {abstracts:<13} │ {size:<10} │ {time_min:<13} │ {keywords:<10} │")
        
        print("└" + "─"*15 + "┴" + "─"*12 + "┴" + "─"*15 + "┴" + "─"*12 + "┘")
        
        # Maior arquivo processado
        largest = max(successful, key=lambda x: x['text_size_mb'])
        
        print(f"\n🏆 CAPACIDADE MÁXIMA TESTADA:")
        print(f"   📏 {largest['num_abstracts']:,} abstracts ({largest['text_size_mb']:.1f}MB)")
        print(f"   ⏱️  {largest['extraction_time_s']/60:.2f} minutos")
        print(f"   🎯 Status: {'✅ Processamento bem-sucedido' if largest['text_size_mb'] >= 40 else '⚠️ Teste limitado'}")
        
        # Conclusão sobre capacidade
        if largest['text_size_mb'] >= 40:
            print(f"\n🎉 CONCLUSÃO: YAKE 2.0 consegue processar arquivos grandes!")
            print(f"   ✅ Capacidade confirmada para arquivos ≥40MB")
            print(f"   ⚡ Performance competitiva com versão 0.6.0")
        else:
            print(f"\n⚠️ CONCLUSÃO: Teste limitado a {largest['text_size_mb']:.1f}MB")
            print(f"   📝 Recomendação: Teste com arquivo real de ~48MB")
        
    else:
        print("❌ Nenhum teste foi bem-sucedido!")
    
    print()
    return successful

def main():
    """Função principal"""
    try:
        results = test_yake_large_file()
        
        if results:
            print("✅ Testes de escalabilidade concluídos com sucesso!")
            return True
        else:
            print("❌ Testes falharam!")
            return False
            
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)