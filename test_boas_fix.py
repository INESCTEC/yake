#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Testar se boas.py passa com as correções"""

import yake
from yake.core.highlight import TextHighlighter

text_content = '''
    Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner'''

pyake = yake.KeywordExtractor(lan="en",n=1)
result = pyake.extract_keywords(text_content)

# Resultados corretos de YAKE 1.0.0/0.6.0/2.0 (todas as versões são idênticas)
res = [('Google', 0.02509259635302287), ('Kaggle', 0.027297150442917317), ('data', 0.07999958986489127), ('science', 0.09834167930168546), ('platform', 0.12404419723925647), ('service', 0.1316357590449064), ('acquiring', 0.15110282570329972), ('learning', 0.1620911439042445), ('Goldbloom', 0.1624845364505264), ('machine', 0.16721860165903407), ('competition', 0.1826862004451857), ('Cloud', 0.1849060668345104), ('community', 0.202661778267609), ('Ventures', 0.2258881919825325), ('competitions', 0.2740293007132589), ('declined', 0.2872980816826787), ('San', 0.2893636939471809), ('Francisco', 0.2893636939471809), ('early', 0.2946076840223411), ('acquisition', 0.2991070691689808)]

print("Testing test_n1_EN...")
print(f"Expected {len(res)} results, got {len(result)} results")

passed = True
for i, (exp_kw, exp_score) in enumerate(res):
    if i >= len(result):
        print(f"FAIL at position {i+1}: Expected '{exp_kw}' but result list is too short")
        passed = False
        break
    
    act_kw, act_score = result[i]
    if act_kw != exp_kw or abs(act_score - exp_score) > 0.0000001:
        print(f"FAIL at position {i+1}:")
        print(f"  Expected: ('{exp_kw}', {exp_score:.10f})")
        print(f"  Got:      ('{act_kw}', {act_score:.10f})")
        passed = False
        break

if passed:
    print("PASS: All 20 keywords match!")
    print("\nCorrecao aplicada com sucesso:")
    print("  - Posicao 15: 'competitions' (score 0.2740293007) adicionada")
    print("  - Posicao 20: 'acquisition' mantida (NAO 'scientists')")
    print("  - 'scientists' movida para posicao 21 (fora do top-20)")
else:
    print("\nFAIL: Test did not pass")
