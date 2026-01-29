#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Comparação entre versões do YAKE: Original Publicada vs 0.6.0 vs 2.0"""

# Resultados ORIGINAIS PUBLICADOS (de boas.py)
original_published = [
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

# Resultados YAKE 2.0 (atual)
import yake

text_content = '''
Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner'''

pyake = yake.KeywordExtractor(lan="en", n=1, top=20)
yake_20_results = pyake.extract_keywords(text_content)

print("="*80)
print("COMPARAÇÃO: YAKE Original Publicada vs YAKE 2.0")
print("="*80)
print()

print("📊 Top 20 Keywords:")
print()
print(f"{'Pos':<5} {'Original Publicada':<40} {'YAKE 2.0':<40}")
print("-" * 90)

for i in range(20):
    orig = f"{original_published[i][0]:<20} ({original_published[i][1]:.10f})"
    new = f"{yake_20_results[i][0]:<20} ({yake_20_results[i][1]:.10f})"
    
    # Marcar diferenças
    if original_published[i][0] != yake_20_results[i][0]:
        marker = " ❌ DIFERENTE"
    else:
        marker = " ✅"
    
    print(f"{i+1:<5} {orig:<40} {new:<40}{marker}")

print()
print("="*80)
print("DIFERENÇAS ENCONTRADAS:")
print("="*80)

orig_keywords = set([kw[0] for kw in original_published])
new_keywords = set([kw[0] for kw in yake_20_results])

only_in_original = orig_keywords - new_keywords
only_in_new = new_keywords - orig_keywords

if only_in_original:
    print(f"\n🔴 Apenas na versão ORIGINAL PUBLICADA: {only_in_original}")
if only_in_new:
    print(f"\n🔵 Apenas no YAKE 2.0: {only_in_new}")

# Verificar posição de "scientists" e "competitions"
scientists_pos_orig = None
competitions_pos_orig = None
scientists_pos_new = None
competitions_pos_new = None

for i, (kw, score) in enumerate(original_published):
    if kw == "scientists":
        scientists_pos_orig = i + 1
    if kw == "competitions":
        competitions_pos_orig = i + 1

for i, (kw, score) in enumerate(yake_20_results):
    if kw == "scientists":
        scientists_pos_new = i + 1
    if kw == "competitions":
        competitions_pos_new = i + 1

print()
print("="*80)
print("ANÁLISE ESPECÍFICA:")
print("="*80)
print(f"\n'scientists':")
print(f"  - Original Publicada: posição {scientists_pos_orig if scientists_pos_orig else 'NÃO ENCONTRADA'}")
print(f"  - YAKE 2.0: posição {scientists_pos_new if scientists_pos_new else 'NÃO ENCONTRADA (está em #21)'}")

print(f"\n'competitions':")
print(f"  - Original Publicada: posição {competitions_pos_orig if competitions_pos_orig else 'NÃO ENCONTRADA'}")
print(f"  - YAKE 2.0: posição {competitions_pos_new if competitions_pos_new else 'NÃO ENCONTRADA'}")

print()
print("="*80)
print("CONCLUSÃO:")
print("="*80)
print("""
A versão ORIGINAL PUBLICADA do YAKE tinha "scientists" na posição 20.
A versão YAKE 2.0 (e aparentemente 0.6.0) tem "competitions" na posição 15.

Isso indica que HOUVE UMA MUDANÇA NO ALGORITMO entre a primeira versão
publicada e as versões posteriores (0.6.0+).

PRÓXIMO PASSO: Verificar qual versão é a "correta" para usar como baseline.
""")
