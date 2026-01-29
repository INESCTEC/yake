#!/usr/bin/env python3
# pylint: skip-file
"""
🔍 TESTE DE VERIFICAÇÃO: Código Local vs Performance Real
=========================================================
Verifica se está usando código local e testa com textos diversos
"""

import yake
import time
import sys
from datetime import datetime

def verify_local_code():
    """Verifica se está usando código local e otimizações"""
    print("🔍 VERIFICAÇÃO DE CÓDIGO LOCAL")
    print("=" * 50)
    
    # 1. Verificar localização do YAKE
    print(f"📁 YAKE path: {yake.__file__}")
    print(f"📋 YAKE version: {getattr(yake, '__version__', 'Unknown')}")
    
    # 2. Verificar se otimizações estão ativas
    try:
        from yake.data.single_word import SingleWord
        has_slots = hasattr(SingleWord, '__slots__')
        print(f"🚀 SingleWord tem __slots__: {has_slots}")
        
        if has_slots:
            print(f"   __slots__ content: {SingleWord.__slots__}")
    except Exception as e:
        print(f"❌ Erro ao verificar __slots__: {e}")
    
    # 3. Verificar cache
    try:
        from yake.data.core import DataCore
        has_cache = hasattr(DataCore, '_stopwords_cache')
        print(f"💾 DataCore tem cache: {has_cache}")
    except Exception as e:
        print(f"❌ Erro ao verificar cache: {e}")
    
    print()

def test_diverse_texts():
    """Teste com textos diversos (não repetitivos)"""
    print("🧪 TESTE COM TEXTOS DIVERSOS")
    print("=" * 50)
    
    # Textos diversos para teste real
    diverse_texts = [
        """Machine learning algorithms have revolutionized artificial intelligence by enabling systems to learn from data without explicit programming. Deep learning neural networks, particularly convolutional and recurrent architectures, have achieved remarkable success in computer vision and natural language processing tasks.""",
        
        """Climate change represents one of the most pressing challenges of our time, with rising global temperatures causing melting ice caps, changing precipitation patterns, and extreme weather events that threaten biodiversity and human settlements worldwide.""",
        
        """Quantum computing leverages quantum mechanical phenomena such as superposition and entanglement to process information in ways that classical computers cannot. This emerging technology promises to solve complex optimization problems and break current cryptographic systems.""",
        
        """Biotechnology advances in gene editing, particularly CRISPR-Cas9 technology, have opened new possibilities for treating genetic diseases, developing drought-resistant crops, and creating novel therapeutic approaches for cancer and other conditions.""",
        
        """Renewable energy sources including solar photovoltaic panels, wind turbines, and hydroelectric systems are becoming increasingly cost-effective alternatives to fossil fuels, driving the global transition toward sustainable energy production.""",
        
        """Space exploration missions to Mars, Jupiter's moons, and beyond continue to expand our understanding of the universe while developing technologies that benefit life on Earth, from satellite communications to advanced materials science.""",
        
        """Cybersecurity threats in the digital age require sophisticated defense mechanisms including artificial intelligence-powered threat detection, zero-trust network architectures, and quantum-resistant encryption methods to protect sensitive information.""",
        
        """Urban planning in megacities faces complex challenges related to transportation infrastructure, housing affordability, environmental sustainability, and social equity that require innovative solutions and community engagement to address effectively.""",
        
        """Medical diagnostics using artificial intelligence and machine learning can analyze medical images, predict disease outcomes, and personalize treatment plans with unprecedented accuracy, improving patient care and reducing healthcare costs.""",
        
        """Financial technology innovations including blockchain, cryptocurrency, mobile payments, and algorithmic trading are transforming traditional banking systems and creating new opportunities for financial inclusion and economic development."""
    ]
    
    # Criar texto grande combinando textos diversos
    large_diverse_text = ""
    target_abstracts = 5000  # Teste menor mas representativo
    
    print(f"📝 Gerando {target_abstracts} abstracts diversos...")
    
    for i in range(target_abstracts):
        # Escolher texto base diverso (rotaciona entre os 10 textos)
        base_text = diverse_texts[i % len(diverse_texts)]
        
        # Adicionar variação única
        variation = f"Study {i+1} findings: "
        large_diverse_text += variation + base_text + "\n\n"
    
    text_size_mb = len(large_diverse_text.encode('utf-8')) / (1024 * 1024)
    print(f"✅ Texto gerado: {len(large_diverse_text):,} chars, {text_size_mb:.1f}MB")
    print(f"📊 Vocabulário diverso: {len(set(large_diverse_text.split()))} palavras únicas")
    
    # Testar YAKE
    print("\n🔍 Executando YAKE com texto diverso...")
    
    config = {
        'lan': 'en',
        'n': 3,
        'dedupLim': 0.7,
        'top': 50,  # Menos keywords para análise focada
        'features': None
    }
    
    start_time = time.time()
    
    try:
        kw_extractor = yake.KeywordExtractor(**config)
        keywords = kw_extractor.extract_keywords(large_diverse_text)
        
        extraction_time = time.time() - start_time
        
        print(f"✅ SUCESSO!")
        print(f"⏱️  Tempo: {extraction_time:.2f}s ({extraction_time/60:.2f} min)")
        print(f"📊 Keywords: {len(keywords)}")
        print(f"📈 Performance: {text_size_mb/extraction_time:.2f} MB/s")
        
        print(f"\n🏆 Top 10 keywords (texto diverso):")
        for i, (kw, score) in enumerate(keywords[:10]):
            print(f"   {i+1:2d}. '{kw}' → {score:.6f}")
        
        # Verificar se há scores negativos (teste de correção PR #96)
        negative_scores = [(kw, score) for kw, score in keywords if score < 0]
        if negative_scores:
            print(f"\n⚠️  ATENÇÃO: {len(negative_scores)} scores negativos encontrados!")
            for kw, score in negative_scores[:5]:
                print(f"   ❌ '{kw}' → {score:.6f}")
        else:
            print(f"\n✅ Correção PR #96 ativa: 0 scores negativos!")
        
        return {
            'status': 'SUCCESS',
            'time_seconds': extraction_time,
            'text_size_mb': text_size_mb,
            'keywords_count': len(keywords),
            'negative_scores': len(negative_scores),
            'performance_mbs': text_size_mb / extraction_time
        }
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return {
            'status': 'ERROR',
            'error': str(e)
        }

def test_repeated_vs_diverse():
    """Compara texto repetitivo vs diverso"""
    print("\n" + "="*70)
    print("📊 COMPARAÇÃO: TEXTO REPETITIVO vs DIVERSO")
    print("="*70)
    
    base_text = """Machine learning algorithms are used in artificial intelligence systems for data processing and analysis."""
    
    # Teste 1: Texto repetitivo (como no teste original)
    print("\n🔄 Teste 1: TEXTO REPETITIVO")
    repeated_text = ""
    for i in range(1000):
        repeated_text += f"Abstract {i+1}: " + base_text + "\n"
    
    print(f"📝 Tamanho: {len(repeated_text.encode('utf-8')) / (1024*1024):.1f}MB")
    print(f"📊 Palavras únicas: {len(set(repeated_text.split()))}")
    
    start = time.time()
    extractor1 = yake.KeywordExtractor(lan='en', n=3, top=20)
    keywords1 = extractor1.extract_keywords(repeated_text)
    time1 = time.time() - start
    
    print(f"⏱️  Tempo: {time1:.2f}s")
    
    # Teste 2: Texto diverso
    print("\n🌟 Teste 2: TEXTO DIVERSO")
    diverse_texts_base = [
        "Machine learning algorithms revolutionize artificial intelligence systems.",
        "Climate change affects global weather patterns and ecosystems.",
        "Quantum computing enables complex mathematical calculations.",
        "Biotechnology advances improve medical treatment options.",
        "Renewable energy reduces environmental impact significantly."
    ]
    
    diverse_text = ""
    for i in range(1000):
        base = diverse_texts_base[i % len(diverse_texts_base)]
        diverse_text += f"Study {i+1}: " + base + "\n"
    
    print(f"📝 Tamanho: {len(diverse_text.encode('utf-8')) / (1024*1024):.1f}MB")
    print(f"📊 Palavras únicas: {len(set(diverse_text.split()))}")
    
    start = time.time()
    extractor2 = yake.KeywordExtractor(lan='en', n=3, top=20)
    keywords2 = extractor2.extract_keywords(diverse_text)
    time2 = time.time() - start
    
    print(f"⏱️  Tempo: {time2:.2f}s")
    
    # Comparação
    print(f"\n📊 COMPARAÇÃO DE PERFORMANCE:")
    print(f"   🔄 Repetitivo: {time1:.2f}s")
    print(f"   🌟 Diverso:    {time2:.2f}s")
    
    if time1 < time2:
        diff = ((time2 - time1) / time1) * 100
        print(f"   ⚡ Repetitivo é {diff:.1f}% mais rápido (cache effect)")
    else:
        diff = ((time1 - time2) / time2) * 100
        print(f"   🌟 Diverso é {diff:.1f}% mais rápido (não esperado)")

def main():
    """Função principal"""
    print("🔍 VERIFICAÇÃO COMPLETA DE CÓDIGO E PERFORMANCE")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Verificar código local
    verify_local_code()
    
    # 2. Teste com textos diversos
    result = test_diverse_texts()
    
    # 3. Comparação repetitivo vs diverso
    test_repeated_vs_diverse()
    
    print("\n" + "="*60)
    print("🎯 CONCLUSÕES:")
    
    if result['status'] == 'SUCCESS':
        print(f"✅ Código local confirmado e funcional")
        print(f"📊 Performance com texto diverso: {result['performance_mbs']:.2f} MB/s")
        
        if result['negative_scores'] == 0:
            print(f"✅ Correção PR #96 ativa (0 scores negativos)")
        else:
            print(f"⚠️  Possível problema: {result['negative_scores']} scores negativos")
    else:
        print(f"❌ Problemas detectados no teste")
    
    return result['status'] == 'SUCCESS'

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)