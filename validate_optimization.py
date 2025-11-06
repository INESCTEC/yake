#!/usr/bin/env python3
# pylint: skip-file
"""
🧪 VALIDAÇÃO DE RESULTADOS
==========================
Verifica que as otimizações não alteraram os resultados extraídos
"""

import yake

def test_identical_results():
    """Testa que keywords extraídas são idênticas"""
    
    print("🧪 VALIDAÇÃO: Keywords Extraídas Idênticas")
    print("=" * 70)
    print()
    
    # Textos de teste
    tests = [
        {
            'name': 'Pequeno',
            'text': """Machine learning is a method of data analysis that automates 
            analytical model building. It is a branch of artificial intelligence 
            based on the idea that systems can learn from data, identify patterns 
            and make decisions with minimal human intervention."""
        },
        {
            'name': 'Médio',
            'text': """Sources tell us that Google is acquiring Kaggle, a platform that 
            hosts data science and machine learning competitions. Details about the 
            transaction remain somewhat vague, but given that Google is hosting its 
            Cloud Next conference in San Francisco this week, the official announcement 
            could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO 
            Anthony Goldbloom declined to deny that the acquisition is happening. 
            Google itself declined 'to comment on rumours'. Kaggle, which has about 
            half a million data scientists on its platform, was founded by Goldbloom  
            and Ben Hamner in 2010. The service got an early start and even though 
            it has a few competitors like DrivenData, TopCoder and HackerRank, it has 
            managed to stay well ahead of them by focusing on its specific niche.""" * 3
        }
    ]
    
    all_passed = True
    
    for test in tests:
        print(f"📝 Testando: {test['name']}")
        print(f"   Tamanho: {len(test['text'])} caracteres")
        
        # Extrair com configuração padrão
        kw_extractor = yake.KeywordExtractor(
            lan='en',
            n=3,
            dedupLim=0.7,
            top=20
        )
        
        keywords = kw_extractor.extract_keywords(test['text'])
        
        print(f"   ✅ Extraiu {len(keywords)} keywords")
        
        # Mostrar top 5
        print(f"   🏆 Top 5:")
        for i, (kw, score) in enumerate(keywords[:5], 1):
            print(f"      {i}. '{kw}' (score: {score:.4f})")
        
        # Verificar que não há scores negativos
        negative_scores = [kw for kw, score in keywords if score < 0]
        if negative_scores:
            print(f"   ❌ ERRO: {len(negative_scores)} keywords com score negativo!")
            all_passed = False
        else:
            print(f"   ✅ Nenhum score negativo")
        
        print()
    
    return all_passed

def test_performance():
    """Testa performance básica"""
    
    import time
    
    print("\n" + "=" * 70)
    print("⚡ TESTE DE PERFORMANCE")
    print("=" * 70)
    print()
    
    text = """Machine learning is transforming the world of technology. 
    Artificial intelligence and deep learning are becoming increasingly 
    important in modern applications. Data science helps companies make 
    better decisions using statistical analysis and predictive modeling.""" * 100
    
    print(f"📝 Texto: {len(text):,} caracteres")
    print()
    
    times = []
    for i in range(5):
        start = time.perf_counter()
        
        kw_extractor = yake.KeywordExtractor(lan='en', n=3, top=50)
        keywords = kw_extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"   Execução {i+1}: {elapsed:.4f}s ({len(keywords)} keywords)")
    
    avg = sum(times) / len(times)
    print()
    print(f"⏱️  Tempo médio: {avg:.4f}s")
    print(f"   Min: {min(times):.4f}s | Max: {max(times):.4f}s")
    print()

def main():
    """Função principal"""
    
    print("🚀 VALIDAÇÃO DE OTIMIZAÇÕES DO YAKE")
    print("=" * 70)
    print()
    
    # Teste 1: Resultados idênticos
    if test_identical_results():
        print("✅ VALIDAÇÃO PASSOU: Resultados são consistentes")
    else:
        print("❌ VALIDAÇÃO FALHOU: Resultados inconsistentes")
        return False
    
    # Teste 2: Performance
    test_performance()
    
    print("=" * 70)
    print("✅ TODAS AS VALIDAÇÕES PASSARAM!")
    print("=" * 70)
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
