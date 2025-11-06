#!/usr/bin/env python
# pylint: skip-file
"""
Comparação direta: YAKE 0.6.0 (original) vs YAKE 2.0 (atual)
para identificar EXATAMENTE onde está o bug
"""

import sys
import os

# Teste com YAKE 0.6.0 original
print("="*100)
print("TESTE 1: YAKE 0.6.0 ORIGINAL")
print("="*100)

# Adicionar yake_0.6.0 ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yake', 'yake_0.6.0'))
import yake as yake_060

text_content = """
Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner"""

pyake_060 = yake_060.KeywordExtractor(lan="en", n=1, top=25)
result_060 = pyake_060.extract_keywords(text_content)

print("\nYAKE 0.6.0 - Posições 10-25:")
for i, (kw, score) in enumerate(result_060[9:25], 10):
    marker = ""
    if kw == "competitions":
        marker = " ← competitions"
    elif kw == "scientists":
        marker = " ← scientists ✅"
    print(f"  {i:2d}. {kw:20s} {score:.18f}{marker}")

# Remover yake_0.6.0 do path e importar YAKE 2.0
sys.path.pop(0)
del sys.modules['yake']
if 'yake.core' in sys.modules:
    del sys.modules['yake.core']
if 'yake.core.yake' in sys.modules:
    del sys.modules['yake.core.yake']
if 'yake.data' in sys.modules:
    del sys.modules['yake.data']

print()
print("="*100)
print("TESTE 2: YAKE 2.0 ATUAL")
print("="*100)

import yake as yake_20

pyake_20 = yake_20.KeywordExtractor(lan="en", n=1, top=25)
result_20 = pyake_20.extract_keywords(text_content)

print("\nYAKE 2.0 - Posições 10-25:")
for i, (kw, score) in enumerate(result_20[9:25], 10):
    marker = ""
    if kw == "competitions":
        marker = " ← competitions ❌"
    elif kw == "scientists":
        marker = " ← scientists"
    print(f"  {i:2d}. {kw:20s} {score:.18f}{marker}")

print()
print("="*100)
print("COMPARAÇÃO DIRETA")
print("="*100)

print("\nDiferenças encontradas:")
differences = []
for i in range(min(len(result_060), len(result_20))):
    kw_060, score_060 = result_060[i]
    kw_20, score_20 = result_20[i]
    
    if kw_060 != kw_20:
        differences.append((i+1, kw_060, kw_20))
        print(f"  Posição {i+1:2d}: '{kw_060}' (0.6.0) vs '{kw_20}' (2.0)")
    elif abs(score_060 - score_20) > 1e-10:
        print(f"  Posição {i+1:2d}: '{kw_060}' - Score diferente: {score_060:.15f} vs {score_20:.15f}")

if not differences:
    print("  ✅ IDÊNTICO! Nenhuma diferença encontrada!")
else:
    print(f"\n❌ Total de {len(differences)} diferenças de keywords encontradas")

print()
print("="*100)
print("🔍 ANÁLISE ESPECÍFICA: 'competitions' vs 'scientists'")
print("="*100)

# Encontrar posições exatas
pos_comp_060 = next((i for i, (kw, _) in enumerate(result_060, 1) if kw == "competitions"), None)
pos_sci_060 = next((i for i, (kw, _) in enumerate(result_060, 1) if kw == "scientists"), None)
pos_comp_20 = next((i for i, (kw, _) in enumerate(result_20, 1) if kw == "competitions"), None)
pos_sci_20 = next((i for i, (kw, _) in enumerate(result_20, 1) if kw == "scientists"), None)

print(f"\nYAKE 0.6.0:")
if pos_comp_060:
    kw, score = result_060[pos_comp_060-1]
    print(f"  'competitions': posição {pos_comp_060}, score {score:.18f}")
else:
    print(f"  'competitions': não está nos top 25")

if pos_sci_060:
    kw, score = result_060[pos_sci_060-1]
    print(f"  'scientists':   posição {pos_sci_060}, score {score:.18f}")
else:
    print(f"  'scientists': não está nos top 25")

print(f"\nYAKE 2.0:")
if pos_comp_20:
    kw, score = result_20[pos_comp_20-1]
    print(f"  'competitions': posição {pos_comp_20}, score {score:.18f}")
else:
    print(f"  'competitions': não está nos top 25")

if pos_sci_20:
    kw, score = result_20[pos_sci_20-1]
    print(f"  'scientists':   posição {pos_sci_20}, score {score:.18f}")
else:
    print(f"  'scientists': não está nos top 25")

print()
