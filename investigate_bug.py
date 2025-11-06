#!/usr/bin/env python
# pylint: skip-file
"""Investigação profunda do problema com 'competitions' vs 'scientists'"""

import yake

text_content = """
Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner"""

print("="*100)
print("INVESTIGAÇÃO: Por que 'competitions' aparece e 'scientists' não?")
print("="*100)
print()

# Extrair TODOS os keywords (não apenas top 20)
pyake = yake.KeywordExtractor(lan="en", n=1, top=50)
all_results = pyake.extract_keywords(text_content)

print("🔍 Procurando 'competitions' e 'scientists' em TODOS os resultados:")
print()

for i, (kw, score) in enumerate(all_results, 1):
    if kw.lower() in ['competitions', 'competition', 'scientists', 'scientist']:
        print(f"Posição {i:2d}: {kw:20s} score={score:.18f}")

print()
print("-"*100)

# Contar ocorrências no texto
comp_count = text_content.lower().count('competition ')
comps_count = text_content.lower().count('competitions')
sci_count = text_content.lower().count('scientist ')
scis_count = text_content.lower().count('scientists')

print()
print("📊 Contagem de ocorrências no texto:")
print(f"   'competition' (singular):  {comp_count} ocorrências")
print(f"   'competitions' (plural):   {comps_count} ocorrências")
print(f"   'scientist' (singular):    {sci_count} ocorrências")
print(f"   'scientists' (plural):     {scis_count} ocorrências")
print()

print("="*100)
print("🧪 TESTE: Extraindo apenas top 20 (como esperado)")
print("="*100)
print()

pyake = yake.KeywordExtractor(lan="en", n=1, top=20)
result = pyake.extract_keywords(text_content)

expected_at_15_20 = [
    ("declined", 0.2872980816826787),
    ("San", 0.2893636939471809),
    ("Francisco", 0.2893636939471809),
    ("early", 0.2946076840223411),
    ("acquisition", 0.2991070691689808),
    ("scientists", 0.3046548516998034),
]

print("Posições 15-20 esperadas:")
for i, (kw, score) in enumerate(expected_at_15_20, 15):
    print(f"  {i}. {kw:20s} {score:.18f}")

print()
print("Posições 15-20 atuais:")
for i, (kw, score) in enumerate(result[14:20], 15):
    print(f"  {i}. {kw:20s} {score:.18f}")

print()
print("="*100)
print("💡 ANÁLISE:")
print("="*100)
print()
print("Se 'competitions' tem um score MENOR que 'declined' (0.287), então deveria")
print("aparecer ANTES na lista (scores menores = melhores keywords).")
print()
print("Se 'competitions' aparece na posição 15 e 'declined' na posição 16,")
print("significa que 'competitions' tem um score MENOR do que o esperado.")
print()
print("Possíveis causas:")
print("1. Bug no cálculo de TF para palavras no plural")
print("2. Bug no cálculo de features (TFIDF, Casing, Position, etc.)")
print("3. Otimização @lru_cache alterando ordem de processamento")
print("4. Frozenset conversion alterando scores")
print()
