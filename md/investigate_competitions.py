#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Investigar diferenças no processamento do texto"""

import yake

# Texto EXATO do boas.py (copiado diretamente)
text_boas = '''
    Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner'''

print("="*120)
print("INVESTIGAÇÃO: Por que 'competitions' aparece em YAKE 2.0?")
print("="*120)

kw = yake.KeywordExtractor(lan="en", n=1, top=25)
result = kw.extract_keywords(text_boas)

print("\nAnálise das keywords relacionadas com 'competition':")
print("-"*120)

for i, (keyword, score) in enumerate(result[:25], 1):
    if 'competition' in keyword.lower():
        print(f"Posição {i}: '{keyword}' (score: {score:.10f})")

# Contar ocorrências no texto
print("\nContagem de ocorrências no texto:")
print(f"  - 'competition ' (singular com espaço): {text_boas.count('competition ')}")
print(f"  - 'competition.' (singular com ponto): {text_boas.count('competition.')}")
print(f"  - 'competitions' (plural): {text_boas.count('competitions')}")
print(f"  - Total 'competition': {text_boas.lower().count('competition')}")

# Verificar "scientists"
print("\nContagem de 'scientists':")
print(f"  - 'scientists' (plural): {text_boas.count('scientists')}")
print(f"  - 'scientist' (singular): {text_boas.count('scientist')}")

print("\n" + "="*120)
print("HIPÓTESE")
print("="*120)
print("Se 'competitions' tem score 0.2740 e 'scientists' tem score 0.3046:")
print("  - 'competitions' é MELHOR (score mais baixo) que 'scientists'")
print("  - Logo,'competitions' deveria aparecer ANTES de 'scientists' no ranking")
print("\nPorém, boas.py espera que 'scientists' esteja na posição 20,")
print("o que significa que 'competitions' NÃO deveria estar no top-20.")
print("\nPossíveis causas:")
print("  1. Bug no cálculo do score de 'competitions'")
print("  2. Diferença na contagem de ocorrências (singular vs plural)")
print("  3. Diferença no processamento de n-gramas")
print("  4. boas.py foi criado com versão diferente ou texto diferente")
