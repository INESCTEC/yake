#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""
Benchmark F1-Score: Original Publicada vs YAKE 0.6.0 vs YAKE 2.0

Compara as 3 versões do YAKE em termos de F1-score usando datasets padrão.
"""

import os
import sys
from collections import defaultdict

# YAKE 2.0 (atual)
import yake

# YAKE 0.6.0 (da pasta yake_0.6.0)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yake_0.6.0'))
import yake as yake_060


def calculate_f1_score(extracted_keywords, gold_keywords, top_n=10):
    """Calcula F1-score entre keywords extraídas e gold standard."""
    # Normalizar keywords (lowercase)
    extracted_set = set([kw.lower() for kw, _ in extracted_keywords[:top_n]])
    gold_set = set([kw.lower() for kw in gold_keywords])
    
    # True Positives
    tp = len(extracted_set & gold_set)
    
    # False Positives
    fp = len(extracted_set - gold_set)
    
    # False Negatives
    fn = len(gold_set - extracted_set)
    
    # Precision
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    
    # Recall
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    # F1-Score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'fn': fn
    }


# Dataset de teste (exemplo do paper YAKE)
# Usando o texto do Kaggle como exemplo
test_case = {
    'text': '''Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner''',
    
    # Gold standard keywords (selecionados manualmente como os mais relevantes)
    'gold_keywords': [
        'google', 'kaggle', 'data science', 'machine learning',
        'competition', 'competitions', 'platform', 'acquisition',
        'community', 'data scientists', 'service'
    ],
    'language': 'en',
    'n': 1,
    'top': 20
}


print("="*100)
print("BENCHMARK F1-SCORE: Original Publicada vs YAKE 0.6.0 vs YAKE 2.0")
print("="*100)
print()

print("📋 Configuração do Teste:")
print(f"  - Linguagem: {test_case['language']}")
print(f"  - N-gram size: {test_case['n']}")
print(f"  - Top keywords: {test_case['top']}")
print(f"  - Gold keywords: {len(test_case['gold_keywords'])} keywords")
print()

# Extrair keywords com as 3 versões
print("🔄 Extraindo keywords com as 3 versões...")
print()

# Versão Original Publicada (simulada com os resultados de boas.py)
# Como não temos o código exato da versão original, vamos usar os resultados esperados do boas.py
original_results_n1 = [
    ('Google', 0.02509259635302287), 
    ('Kaggle', 0.027297150442917317), 
    ('data', 0.07999958986489127), 
    ('science', 0.09834167930168546), 
    ('platform', 0.12404419723925647), 
    ('service', 0.1316357590449064), 
    ('acquiring', 0.15110282570329972), 
    ('learning', 0.1620911439042445), 
    ('Goldbloom', 0.1624845364505264), 
    ('machine', 0.16721860165903407), 
    ('competition', 0.1826862004451857), 
    ('Cloud', 0.1849060668345104), 
    ('community', 0.202661778267609), 
    ('Ventures', 0.2258881919825325), 
    ('declined', 0.2872980816826787), 
    ('San', 0.2893636939471809), 
    ('Francisco', 0.2893636939471809), 
    ('early', 0.2946076840223411), 
    ('acquisition', 0.2991070691689808), 
    ('scientists', 0.3046548516998034)
]

# YAKE 0.6.0
try:
    kw_extractor_060 = yake_060.KeywordExtractor(
        lan=test_case['language'],
        n=test_case['n'],
        top=test_case['top']
    )
    yake_060_results = kw_extractor_060.extract_keywords(test_case['text'])
    print("✅ YAKE 0.6.0: Extração concluída")
except Exception as e:
    print(f"❌ YAKE 0.6.0: Erro - {e}")
    yake_060_results = []

# YAKE 2.0
try:
    kw_extractor_20 = yake.KeywordExtractor(
        lan=test_case['language'],
        n=test_case['n'],
        top=test_case['top']
    )
    yake_20_results = kw_extractor_20.extract_keywords(test_case['text'])
    print("✅ YAKE 2.0: Extração concluída")
except Exception as e:
    print(f"❌ YAKE 2.0: Erro - {e}")
    yake_20_results = []

print()
print("="*100)
print("RESULTADOS DO BENCHMARK")
print("="*100)
print()

# Calcular F1-scores para diferentes valores de top_n
top_n_values = [5, 10, 15, 20]

results_summary = {
    'Original Publicada': {},
    'YAKE 0.6.0': {},
    'YAKE 2.0': {}
}

for top_n in top_n_values:
    # Original Publicada
    metrics_orig = calculate_f1_score(original_results_n1, test_case['gold_keywords'], top_n)
    results_summary['Original Publicada'][top_n] = metrics_orig
    
    # YAKE 0.6.0
    metrics_060 = calculate_f1_score(yake_060_results, test_case['gold_keywords'], top_n)
    results_summary['YAKE 0.6.0'][top_n] = metrics_060
    
    # YAKE 2.0
    metrics_20 = calculate_f1_score(yake_20_results, test_case['gold_keywords'], top_n)
    results_summary['YAKE 2.0'][top_n] = metrics_20

# Apresentar resultados em tabela
print("📊 F1-Score por Top-N:")
print()
print(f"{'Top-N':<10} {'Original':<20} {'YAKE 0.6.0':<20} {'YAKE 2.0':<20}")
print("-" * 70)

for top_n in top_n_values:
    orig_f1 = results_summary['Original Publicada'][top_n]['f1']
    v060_f1 = results_summary['YAKE 0.6.0'][top_n]['f1']
    v20_f1 = results_summary['YAKE 2.0'][top_n]['f1']
    
    # Marcar o melhor
    best = max(orig_f1, v060_f1, v20_f1)
    
    orig_str = f"{orig_f1:.4f}" + (" 🏆" if orig_f1 == best else "")
    v060_str = f"{v060_f1:.4f}" + (" 🏆" if v060_f1 == best else "")
    v20_str = f"{v20_f1:.4f}" + (" 🏆" if v20_f1 == best else "")
    
    print(f"Top-{top_n:<5} {orig_str:<20} {v060_str:<20} {v20_str:<20}")

print()
print("="*100)
print("ANÁLISE DETALHADA (Top-10)")
print("="*100)
print()

for version_name in ['Original Publicada', 'YAKE 0.6.0', 'YAKE 2.0']:
    metrics = results_summary[version_name][10]
    print(f"📈 {version_name}:")
    print(f"   Precision: {metrics['precision']:.4f}")
    print(f"   Recall:    {metrics['recall']:.4f}")
    print(f"   F1-Score:  {metrics['f1']:.4f}")
    print(f"   TP: {metrics['tp']}, FP: {metrics['fp']}, FN: {metrics['fn']}")
    print()

print("="*100)
print("KEYWORDS EXTRAÍDAS (Top-10)")
print("="*100)
print()

print("🔵 Original Publicada:")
for i, (kw, score) in enumerate(original_results_n1[:10], 1):
    in_gold = "✅" if kw.lower() in [g.lower() for g in test_case['gold_keywords']] else "❌"
    print(f"  {i:2}. {kw:<20} {score:.6f} {in_gold}")
print()

print("🟢 YAKE 0.6.0:")
for i, (kw, score) in enumerate(yake_060_results[:10], 1):
    in_gold = "✅" if kw.lower() in [g.lower() for g in test_case['gold_keywords']] else "❌"
    print(f"  {i:2}. {kw:<20} {score:.6f} {in_gold}")
print()

print("🟡 YAKE 2.0:")
for i, (kw, score) in enumerate(yake_20_results[:10], 1):
    in_gold = "✅" if kw.lower() in [g.lower() for g in test_case['gold_keywords']] else "❌"
    print(f"  {i:2}. {kw:<20} {score:.6f} {in_gold}")
print()

print("="*100)
print("CONCLUSÃO")
print("="*100)
print()

# Calcular média de F1 scores
avg_orig = sum([results_summary['Original Publicada'][n]['f1'] for n in top_n_values]) / len(top_n_values)
avg_060 = sum([results_summary['YAKE 0.6.0'][n]['f1'] for n in top_n_values]) / len(top_n_values)
avg_20 = sum([results_summary['YAKE 2.0'][n]['f1'] for n in top_n_values]) / len(top_n_values)

print(f"📊 Média F1-Score (Top-5, 10, 15, 20):")
print(f"   Original Publicada: {avg_orig:.4f}")
print(f"   YAKE 0.6.0:         {avg_060:.4f}")
print(f"   YAKE 2.0:           {avg_20:.4f}")
print()

best_version = max([('Original Publicada', avg_orig), ('YAKE 0.6.0', avg_060), ('YAKE 2.0', avg_20)], key=lambda x: x[1])
print(f"🏆 Melhor versão: {best_version[0]} (F1 médio: {best_version[1]:.4f})")
print()

# Verificar se YAKE 0.6.0 e 2.0 são idênticos
if yake_060_results == yake_20_results:
    print("✅ CONFIRMADO: YAKE 0.6.0 e YAKE 2.0 produzem resultados IDÊNTICOS")
else:
    print("⚠️ ATENÇÃO: YAKE 0.6.0 e YAKE 2.0 produzem resultados DIFERENTES")

print()
print("="*100)
