#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Script simplificado para comparar as 3 versões do YAKE"""

# Texto do test_n1_EN
text_content = '''Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner'''

# Resultados esperados em boas.py (posições 1-20)
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
    ('scientists', 0.3046548516998034)  # <- ESTA é a expectativa em boas.py!
]

print("="*120)
print("ANÁLISE: Por que boas.py espera 'scientists' na posição 20?")
print("="*120)

# Testar versão atual (2.0)
print("\n1. Testando YAKE 2.0 (versão atual)...")
import yake

kw = yake.KeywordExtractor(lan="en", n=1, top=25)
result = kw.extract_keywords(text_content)

print(f"\nTop-25 keywords extraídas por YAKE 2.0:")
print(f"{'Pos':<5} {'Keyword':<20} {'Score':<20}")
print("-"*50)
for i, (keyword, score) in enumerate(result[:25], 1):
    marker = " <- ESPERADO EM BOAS.PY" if i <= 20 and (keyword, score) in [(k, s) for k, s in expected_boas] else ""
    marker_diff = " <- EM BOAS.PY MAS POSIÇÃO DIFERENTE" if keyword == "scientists" else ""
    print(f"{i:<5} {keyword:<20} {score:<20.10f}{marker}{marker_diff}")

# Verificar se "scientists" aparece
scientists_pos = None
for i, (keyword, score) in enumerate(result, 1):
    if keyword == "scientists":
        scientists_pos = i
        scientists_score = score
        break

print(f"\n{'='*120}")
print(f"DESCOBERTA:")
print(f"{'='*120}")
print(f"Em boas.py: 'scientists' está na posição 20 com score {expected_boas[19][1]:.10f}")
if scientists_pos:
    print(f"Em YAKE 2.0: 'scientists' está na posição {scientists_pos} com score {scientists_score:.10f}")
else:
    print(f"Em YAKE 2.0: 'scientists' NÃO aparece no top-25")

# Verificar que keyword está na posição 20 em YAKE 2.0
if len(result) >= 20:
    actual_20th = result[19]  # índice 19 = posição 20
    print(f"\nNa posição 20 de YAKE 2.0 temos: '{actual_20th[0]}' com score {actual_20th[1]:.10f}")
    
    if actual_20th[0] != "scientists":
        print(f"\nCONCLUSÃO:")
        print(f"  - boas.py espera 'scientists' na posição 20")
        print(f"  - YAKE 2.0 retorna '{actual_20th[0]}' na posição 20")
        print(f"  - 'scientists' está na posição {scientists_pos} em YAKE 2.0")
        print(f"\nIsso significa que:")
        print(f"  1. OU boas.py foi criado com uma versão diferente do YAKE")
        print(f"  2. OU boas.py contém expectativas incorretas")
        print(f"  3. OU houve uma mudança no algoritmo que alterou os rankings")
