#!/usr/bin/env python
# pylint: skip-file
"""Teste definitivo: O que YAKE 0.6.0 retorna com top=20 (default)?"""

import sys
import os

# Importar YAKE 0.6.0 original
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yake', 'yake_0.6.0'))
import yake as yake_060

text_content = """
Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner"""

print("="*100)
print("TESTE: YAKE 0.6.0 SEM ESPECIFICAR TOP (default=20)")
print("="*100)
print()

# NÃO especificar top, usar default
pyake = yake_060.KeywordExtractor(lan="en", n=1)
result = pyake.extract_keywords(text_content)

print(f"Número de keywords retornadas: {len(result)}")
print()

expected_from_pqp = [
    ("Google", 0.02509259635302287),
    ("Kaggle", 0.027297150442917317),
    ("data", 0.07999958986489127),
    ("science", 0.09834167930168546),
    ("platform", 0.12404419723925647),
    ("service", 0.1316357590449064),
    ("acquiring", 0.15110282570329972),
    ("learning", 0.1620911439042445),
    ("Goldbloom", 0.1624845364505264),
    ("machine", 0.16721860165903407),
    ("competition", 0.1826862004451857),
    ("Cloud", 0.1849060668345104),
    ("community", 0.202661778267609),
    ("Ventures", 0.2258881919825325),
    ("declined", 0.2872980816826787),
    ("San", 0.2893636939471809),
    ("Francisco", 0.2893636939471809),
    ("early", 0.2946076840223411),
    ("acquisition", 0.2991070691689808),
    ("scientists", 0.3046548516998034),
]

print("Resultados ESPERADOS pelo pqp.py (20 keywords):")
for i, (kw, score) in enumerate(expected_from_pqp, 1):
    print(f"  {i:2d}. {kw:20s} {score:.18f}")

print()
print("Resultados REAIS do YAKE 0.6.0:")
for i, (kw, score) in enumerate(result, 1):
    marker = ""
    if kw == "competitions":
        marker = " ← ❌ competitions está aqui!"
    elif kw == "scientists":
        marker = " ← ✅ scientists"
    print(f"  {i:2d}. {kw:20s} {score:.18f}{marker}")

print()
print("="*100)
print("COMPARAÇÃO")
print("="*100)

if len(result) != len(expected_from_pqp):
    print(f"❌ ERRO: Número diferente - Esperado: {len(expected_from_pqp)}, Real: {len(result)}")

print()
match = True
for i in range(min(len(result), len(expected_from_pqp))):
    kw_exp, score_exp = expected_from_pqp[i]
    kw_real, score_real = result[i]
    
    if kw_exp != kw_real:
        print(f"❌ Posição {i+1}: Esperado '{kw_exp}', Real '{kw_real}'")
        match = False
    elif abs(score_exp - score_real) > 1e-15:
        print(f"⚠️  Posição {i+1}: '{kw_exp}' - Score diferente")
        match = False

if match and len(result) == len(expected_from_pqp):
    print("✅ MATCH PERFEITO! pqp.py está correto para YAKE 0.6.0")
else:
    print()
    print("="*100)
    print("❌ CONCLUSÃO: pqp.py tem resultados INCORRETOS/DESATUALIZADOS!")
    print("="*100)
