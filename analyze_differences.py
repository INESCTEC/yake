#!/usr/bin/env python
# pylint: skip-file
"""Análise detalhada das diferenças entre YAKE 2.0 atual e esperado original"""

import yake

print("="*100)
print("ANÁLISE CRÍTICA: YAKE 2.0 vs Resultados Originais Esperados")
print("="*100)
print()

# TEST 1: test_n1_EN
print("🔍 TEST 1: test_n1_EN (CRÍTICO - texto longo, n=1)")
print("-"*100)

text_content = """
Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner"""

pyake = yake.KeywordExtractor(lan="en", n=1)
result = pyake.extract_keywords(text_content)

expected = [
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

print(f"Resultados Esperados: {len(expected)} keywords")
print(f"Resultados Atuais:    {len(result)} keywords")
print()

if len(result) != len(expected):
    print(f"❌ PROBLEMA: Número diferente de keywords!")
    print()

print(f"{'#':<4} {'Keyword Esperado':<20} {'Score Esperado':<20} {'Keyword Atual':<20} {'Score Atual':<20} {'Status'}")
print("-"*100)

max_len = max(len(result), len(expected))
differences = []

for i in range(max_len):
    if i < len(expected):
        kw_exp, score_exp = expected[i]
    else:
        kw_exp, score_exp = "N/A", 0.0
    
    if i < len(result):
        kw_act, score_act = result[i]
    else:
        kw_act, score_act = "N/A", 0.0
    
    # Verificar diferenças
    status = "✅"
    if kw_exp != kw_act:
        status = "❌ KW"
        differences.append((i+1, "keyword", kw_exp, kw_act))
    elif abs(score_exp - score_act) > 1e-10:
        status = "⚠️ SCORE"
        differences.append((i+1, "score", score_exp, score_act))
    
    print(f"{i+1:<4} {kw_exp:<20} {score_exp:<20.15f} {kw_act:<20} {score_act:<20.15f} {status}")

print()
print(f"📊 RESUMO test_n1_EN:")
print(f"   Total diferenças: {len(differences)}")
if differences:
    print(f"   ❌ FALHOU - Existem diferenças!")
else:
    print(f"   ✅ PASSOU - Resultados idênticos")

print()
print("="*100)

# TEST 2: test_n3_EN
print("\n🔍 TEST 2: test_n3_EN (CRÍTICO - texto longo, n=3)")
print("-"*100)

text_content = """
Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning   competitions. Details about the transaction remain somewhat vague , but given that Google is hosting   its Cloud Next conference in San Francisco this week, the official announcement could come as early   as tomorrow.  Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the   acquisition is happening. Google itself declined 'to comment on rumors'.   Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom   and Ben Hamner in 2010. The service got an early start and even though it has a few competitors   like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its   specific niche. The service is basically the de facto home for running data science  and machine learning   competitions.  With Kaggle, Google is buying one of the largest and most active communities for   data scientists - and with that, it will get increased mindshare in this community, too   (though it already has plenty of that thanks to Tensorflow and other projects).   Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month,   Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying   YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too.   Our understanding is that Google will keep the service running - likely under its current name.   While the acquisition is probably more about Kaggle's community than technology, Kaggle did build   some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are   basically the source code for analyzing data sets and developers can share this code on the   platform (the company previously called them 'scripts').  Like similar competition-centric sites,   Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service.   According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its   launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant,   Google chief economist Hal Varian, Khosla Ventures and Yuri Milner"""

pyake = yake.KeywordExtractor(lan="en", n=3)
result = pyake.extract_keywords(text_content)

expected = [
    ("Google", 0.02509259635302287),
    ("Kaggle", 0.027297150442917317),
    ("CEO Anthony Goldbloom", 0.04834891465259988),
    ("data science", 0.05499112888517541),
    ("acquiring data science", 0.06029572445726576),
    ("Google Cloud Platform", 0.07461585862381104),
    ("data", 0.07999958986489127),
    ("San Francisco", 0.0913829662674319),
    ("Anthony Goldbloom declined", 0.09740885820462175),
    ("science", 0.09834167930168546),
    ("science community Kaggle", 0.1014394718805728),
    ("machine learning", 0.10754988562466912),
    ("Google Cloud", 0.1136787749431024),
    ("Google is acquiring", 0.114683257931042),
    ("acquiring Kaggle", 0.12012386507741751),
    ("Anthony Goldbloom", 0.1213027418574554),
    ("platform", 0.12404419723925647),
    ("co-founder CEO Anthony", 0.12411964553586782),
    ("CEO Anthony", 0.12462950727635251),
    ("service", 0.1316357590449064),
]

print(f"Resultados Esperados: {len(expected)} keywords")
print(f"Resultados Atuais:    {len(result)} keywords")
print()

print(f"{'#':<4} {'Keyword Esperado':<30} {'Score Esperado':<20} {'Keyword Atual':<30} {'Score Atual':<20} {'Status'}")
print("-"*120)

differences = []
for i in range(min(len(result), len(expected))):
    kw_exp, score_exp = expected[i]
    kw_act, score_act = result[i]
    
    status = "✅"
    if kw_exp != kw_act:
        status = "❌ KW"
        differences.append((i+1, "keyword", kw_exp, kw_act))
    elif abs(score_exp - score_act) > 1e-10:
        status = "⚠️ SCORE"  
        differences.append((i+1, "score", score_exp, score_act))
    
    print(f"{i+1:<4} {kw_exp:<30} {score_exp:<20.15f} {kw_act:<30} {score_act:<20.15f} {status}")

print()
print(f"📊 RESUMO test_n3_EN:")
print(f"   Total diferenças: {len(differences)}")
if differences:
    print(f"   ❌ FALHOU - Existem diferenças!")
else:
    print(f"   ✅ PASSOU - Resultados idênticos")

print()
print("="*100)
print("📋 CONCLUSÃO FINAL")
print("="*100)
print()
print("Se algum teste FALHOU, temos um problema CRÍTICO que precisa ser resolvido")
print("antes de continuar com o YAKE 2.0!")
print()
