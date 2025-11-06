#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Testar YAKE 1.0.0 diretamente para verificar se produz resultados do boas.py"""

import sys
import os

# Texto exato do boas.py
text_content = '''
    Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner'''

# Resultados esperados no boas.py ORIGINAL
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

print("="*120)
print("TESTE DIRETO: YAKE 1.0.0 produz os resultados esperados no boas.py?")
print("="*120)

# Adicionar yake_1.0.0 ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yake', 'yake_1.0.0'))

try:
    # Importar YAKE 1.0.0
    from yake import KeywordExtractor
    
    print("\n✅ YAKE 1.0.0 importado com sucesso")
    
    # Extrair keywords (default top=20)
    kw = KeywordExtractor(lan="en", n=1)
    result = kw.extract_keywords(text_content)
    
    print(f"\n📊 YAKE 1.0.0 extraiu {len(result)} keywords")
    
    # Comparar com boas.py
    print(f"\n{'Pos':<5} {'Esperado (boas.py)':<30} {'Score Esperado':<20} {'Real (1.0.0)':<30} {'Score Real':<20} {'Match'}")
    print("-"*120)
    
    matches = 0
    differences = []
    
    for i in range(min(20, len(result))):
        if i < len(expected_boas):
            exp_kw, exp_score = expected_boas[i]
            act_kw, act_score = result[i]
            
            match = (exp_kw == act_kw and abs(exp_score - act_score) < 0.000001)
            symbol = "✅" if match else "❌"
            
            print(f"{i+1:<5} {exp_kw:<30} {exp_score:<20.10f} {act_kw:<30} {act_score:<20.10f} {symbol}")
            
            if match:
                matches += 1
            else:
                differences.append({
                    'pos': i+1,
                    'expected': (exp_kw, exp_score),
                    'actual': (act_kw, act_score)
                })
    
    print("\n" + "="*120)
    print("RESULTADO")
    print("="*120)
    print(f"Matches: {matches}/20")
    print(f"Diferenças: {len(differences)}")
    
    if differences:
        print("\n⚠️  DIFERENÇAS ENCONTRADAS:")
        for diff in differences:
            print(f"  Posição {diff['pos']}:")
            print(f"    Esperado: {diff['expected'][0]} (score: {diff['expected'][1]:.10f})")
            print(f"    Real:     {diff['actual'][0]} (score: {diff['actual'][1]:.10f})")
    
    if matches == 20:
        print("\n✅ YAKE 1.0.0 PRODUZ os resultados esperados no boas.py!")
        print("   Conclusão: boas.py foi criado com YAKE 1.0.0")
    else:
        print("\n❌ YAKE 1.0.0 NÃO PRODUZ os resultados esperados no boas.py!")
        print("   Conclusão: boas.py foi criado com versão/configuração diferente")
        
except Exception as e:
    print(f"\n❌ ERRO ao importar/executar YAKE 1.0.0: {e}")
    import traceback
    traceback.print_exc()
