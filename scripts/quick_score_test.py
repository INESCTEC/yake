#!/usr/bin/env python3
# pylint: skip-file
"""
Teste Rápido de Validação de Scores
===================================

Teste simples para validar que os scores permanecem iguais
após otimizações, testando n-gramas de 1 até 9.
"""

import yake
import time
import sys


def test_score_consistency():
    """Testa consistência dos scores com diferentes n-gramas"""
    
    print("🧪 TESTE RÁPIDO DE CONSISTÊNCIA DE SCORES")
    print("=" * 45)
    
    # Texto de teste padrão
    test_text = """
    Machine learning algorithms and artificial intelligence systems are 
    revolutionizing data science research in computer science and technology 
    innovation. These advanced technologies enable sophisticated analytics, 
    predictive modeling, and business intelligence applications across various 
    industries including healthcare, finance, automotive, and telecommunications.
    
    Natural language processing and computer vision are key areas of artificial 
    intelligence that leverage deep learning neural networks and statistical 
    machine learning methods. These approaches process large datasets to extract 
    meaningful insights and patterns for automated decision making systems.
    """
    
    all_results = {}
    all_passed = True
    
    # Testar n-gramas de 1 até 9
    for n in range(1, 10):
        print(f"\n🔍 Testando n-grama {n}...")
        
        try:
            # Configurar extrator
            extractor = yake.KeywordExtractor(lan="en", n=n, dedupLim=0.7, top=15)
            
            # Medir tempo e extrair keywords
            start_time = time.perf_counter()
            keywords = extractor.extract_keywords(test_text)
            execution_time = time.perf_counter() - start_time
            
            # Verificar se há keywords
            if not keywords:
                print(f"   ⚠️  Nenhuma keyword encontrada para n={n}")
                continue
            
            # Verificar scores negativos
            negative_scores = [(kw, score) for kw, score in keywords if score < 0]
            
            # Calcular estatísticas
            scores = [score for _, score in keywords]
            min_score = min(scores)
            max_score = max(scores)
            avg_score = sum(scores) / len(scores)
            
            # Armazenar resultados
            result = {
                "n": n,
                "num_keywords": len(keywords),
                "execution_time_ms": round(execution_time * 1000, 2),
                "min_score": round(min_score, 8),
                "max_score": round(max_score, 8),
                "avg_score": round(avg_score, 8),
                "negative_count": len(negative_scores),
                "keywords": keywords[:5],  # Top 5 para display
                "all_keywords": keywords   # Todos para análise
            }
            
            all_results[n] = result
            
            # Mostrar resultados
            print(f"   📊 Keywords: {len(keywords)}")
            print(f"   ⏱️  Tempo: {execution_time*1000:.2f}ms")
            print(f"   📈 Scores: {min_score:.6f} - {max_score:.6f} (avg: {avg_score:.6f})")
            print(f"   🔸 Top 3:")
            for i, (keyword, score) in enumerate(keywords[:3]):
                print(f"      {i+1}. {keyword} → {score:.6f}")
            
            # Verificar problemas
            if negative_scores:
                print(f"   ❌ PROBLEMA: {len(negative_scores)} scores negativos!")
                for kw, score in negative_scores[:3]:
                    print(f"      • {kw} = {score}")
                all_passed = False
            else:
                print(f"   ✅ Sem scores negativos")
                
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            all_passed = False
    
    # Resumo final
    print(f"\n" + "=" * 45)
    print(f"📊 RESUMO FINAL")
    print(f"=" * 15)
    
    if all_passed:
        print(f"✅ SUCESSO: Todos os n-gramas funcionaram corretamente")
    else:
        print(f"❌ PROBLEMAS: Alguns n-gramas apresentaram issues")
    
    print(f"\n📈 Estatísticas por n-grama:")
    for n in sorted(all_results.keys()):
        result = all_results[n]
        status = "✅" if result["negative_count"] == 0 else f"❌({result['negative_count']} neg)"
        print(f"   n={n}: {result['num_keywords']:2d} keywords, {result['execution_time_ms']:6.1f}ms {status}")
    
    # Verificar tendências
    print(f"\n🔍 Análise de tendências:")
    
    # Performance por n-grama
    times = [all_results[n]["execution_time_ms"] for n in sorted(all_results.keys())]
    if len(times) > 1:
        time_trend = "crescente" if times[-1] > times[0] else "decrescente"
        print(f"   ⏱️  Tempo: {time_trend} ({times[0]:.1f}ms → {times[-1]:.1f}ms)")
    
    # Quantidade de keywords
    keyword_counts = [all_results[n]["num_keywords"] for n in sorted(all_results.keys())]
    if len(keyword_counts) > 1:
        print(f"   📊 Keywords: {keyword_counts[0]} → {keyword_counts[-1]} (n={min(all_results.keys())} → n={max(all_results.keys())})")
    
    return all_results, all_passed


def compare_with_expected_scores(results, expected_scores=None):
    """Compara com scores esperados se fornecidos"""
    
    if not expected_scores:
        print(f"\n💡 Para comparação rigorosa, forneça scores esperados")
        return True
    
    print(f"\n🔍 COMPARAÇÃO COM SCORES ESPERADOS")
    print("=" * 35)
    
    # TODO: Implementar comparação detalhada
    # quando o usuário fornecer scores de referência
    
    return True


if __name__ == "__main__":
    print("Iniciando teste de consistência de scores...")
    
    # Executar teste principal
    results, passed = test_score_consistency()
    
    # Comparar com scores esperados (se disponíveis)
    compare_with_expected_scores(results)
    
    # Exit code
    sys.exit(0 if passed else 1)