#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Comparar resultados esperados em boas.py vs resultados reais das 3 versões"""

import sys

# Texto do test_n1_EN
text_content = '''Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner'''

# Resultados esperados em boas.py
expected_boas = [
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

print("="*100)
print("COMPARAÇÃO: Resultados esperados (boas.py) vs Resultados reais (3 versões)")
print("="*100)

# Testar YAKE 1.0.0
print("\nTESTANDO YAKE 1.0.0 (Original)")
print("-"*100)
sys.path.insert(0, 'yake/yake_1.0.0')
import yake as yake_100
sys.path.pop(0)

kw_100 = yake_100.KeywordExtractor(lan="en", n=1, top=20)
result_100 = kw_100.extract_keywords(text_content)

print(f"\n{'Posição':<10} {'Esperado (boas.py)':<30} {'Score Esperado':<20} {'Real (1.0.0)':<30} {'Score Real':<20} {'Match':<10}")
print("-"*100)

for i in range(20):
    expected_kw, expected_score = expected_boas[i]
    actual_kw, actual_score = result_100[i]
    match = "OK" if (expected_kw == actual_kw and abs(expected_score - actual_score) < 0.000001) else "DIFF"
    print(f"{i+1:<10} {expected_kw:<30} {expected_score:<20.10f} {actual_kw:<30} {actual_score:<20.10f} {match:<10}")

# Testar YAKE 0.6.0
print("\n\nTESTANDO YAKE 0.6.0")
print("-"*100)
sys.path.insert(0, 'yake/yake_0.6.0')
import yake as yake_060
sys.path.pop(0)

kw_060 = yake_060.KeywordExtractor(lan="en", n=1, top=20)
result_060 = kw_060.extract_keywords(text_content)

print(f"\n{'Posição':<10} {'Esperado (boas.py)':<30} {'Score Esperado':<20} {'Real (0.6.0)':<30} {'Score Real':<20} {'Match':<10}")
print("-"*100)

for i in range(20):
    expected_kw, expected_score = expected_boas[i]
    actual_kw, actual_score = result_060[i]
    match = "OK" if (expected_kw == actual_kw and abs(expected_score - actual_score) < 0.000001) else "DIFF"
    print(f"{i+1:<10} {expected_kw:<30} {expected_score:<20.10f} {actual_kw:<30} {actual_score:<20.10f} {match:<10}")

# Testar YAKE 2.0
print("\n\nTESTANDO YAKE 2.0 (Atual)")
print("-"*100)
import yake as yake_20

kw_20 = yake_20.KeywordExtractor(lan="en", n=1, top=20)
result_20 = kw_20.extract_keywords(text_content)

print(f"\n{'Posição':<10} {'Esperado (boas.py)':<30} {'Score Esperado':<20} {'Real (2.0)':<30} {'Score Real':<20} {'Match':<10}")
print("-"*100)

for i in range(20):
    expected_kw, expected_score = expected_boas[i]
    actual_kw, actual_score = result_20[i]
    match = "OK" if (expected_kw == actual_kw and abs(expected_score - actual_score) < 0.000001) else "DIFF"
    print(f"{i+1:<10} {expected_kw:<30} {expected_score:<20.10f} {actual_kw:<30} {actual_score:<20.10f} {match:<10}")

# Comparar as 3 versões entre si
print("\n\n" + "="*100)
print("COMPARAÇÃO ENTRE AS 3 VERSÕES")
print("="*100)

all_same = True
for i in range(20):
    kw_100, score_100 = result_100[i]
    kw_060, score_060 = result_060[i]
    kw_20, score_20 = result_20[i]
    
    if kw_100 != kw_060 or kw_100 != kw_20 or abs(score_100 - score_060) > 0.000001 or abs(score_100 - score_20) > 0.000001:
        all_same = False
        print(f"\nDIFF na posicao {i+1}:")
        print(f"   1.0.0: {kw_100} ({score_100:.10f})")
        print(f"   0.6.0: {kw_060} ({score_060:.10f})")
        print(f"   2.0:   {kw_20} ({score_20:.10f})")

if all_same:
    print("\nOK: As 3 versoes (1.0.0, 0.6.0, 2.0) produzem resultados IDENTICOS!")

print("\n" + "="*100)
print("CONCLUSÃO")
print("="*100)

# Contar diferenças
diffs_100 = sum(1 for i in range(20) if expected_boas[i][0] != result_100[i][0] or abs(expected_boas[i][1] - result_100[i][1]) > 0.000001)
diffs_060 = sum(1 for i in range(20) if expected_boas[i][0] != result_060[i][0] or abs(expected_boas[i][1] - result_060[i][1]) > 0.000001)
diffs_20 = sum(1 for i in range(20) if expected_boas[i][0] != result_20[i][0] or abs(expected_boas[i][1] - result_20[i][1]) > 0.000001)

print(f"\nDiferencas entre boas.py e cada versao:")
print(f"  - YAKE 1.0.0: {diffs_100} diferencas")
print(f"  - YAKE 0.6.0: {diffs_060} diferencas")
print(f"  - YAKE 2.0:   {diffs_20} diferencas")

if diffs_100 == diffs_060 == diffs_20:
    print(f"\nATENCAO: TODAS as versoes diferem do boas.py igualmente ({diffs_100} diferencas)")
    print(f"   Conclusao: boas.py NAO contem os resultados corretos de nenhuma versao!")
else:
    print("\nAs versoes diferem do boas.py de forma diferente")
    print("   Investigacao necessaria para identificar a origem das expectativas em boas.py")
