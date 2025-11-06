#!/usr/bin/env python
# pylint: skip-file
"""Comparação simples entre YAKE 2.0 e resultados conhecidos da versão 0.6.0"""

import yake

print("="*80)
print("VERIFICAÇÃO: YAKE 2.0 vs Resultados Conhecidos do YAKE 0.6.0")
print("="*80)
print()

# Teste 1: test_n3_EN - Este é um dos testes originais
print("🧪 TEST 1: test_n3_EN (baseline original)")
print("-"*80)

text_content = """
Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. 
Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, 
the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. 
Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, 
was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, 
it has managed to stay well ahead of them by focusing on its specific niche. 
The service is basically the de facto home for running data science and machine learning competitions. 
With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, 
it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). 
Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. 
That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - 
likely under its current name. While the acquisition is probably more about Kaggle's community than technology, 
Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). 
Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. 
According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its   launch in 2010. 
Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner.
"""

kw_extractor = yake.KeywordExtractor(lan="en", n=3, top=10)
result_atual = kw_extractor.extract_keywords(text_content)

# Resultados esperados do YAKE 0.6.0 (do teste original test_n3_EN)
resultado_060 = [
    ('Google', 0.026580662729899),
    ('Kaggle', 0.0289005976239829),
    ('Kaggle co-founder CEO', 0.033407849666882),
    ('CEO Anthony Goldbloom', 0.0334166471719609),
    ('Anthony Goldbloom declined', 0.0335569915022888),
    ('Goldbloom declined', 0.0341906827390181),
    ('Google Cloud Platform', 0.0417104281356548),
    ('acquiring Kaggle', 0.0427605689364459),
    ('data', 0.043276765915315),
    ('Kaggle raised', 0.0437652514407458)
]

print("📦 YAKE 2.0 (atual):")
for i, (kw, score) in enumerate(result_atual, 1):
    print(f"  {i}. {kw:35s} {score:.16f}")

print("\n📦 YAKE 0.6.0 (esperado do teste original):")
for i, (kw, score) in enumerate(resultado_060, 1):
    print(f"  {i}. {kw:35s} {score:.16f}")

print("\n🔍 COMPARAÇÃO:")
if len(result_atual) != len(resultado_060):
    print(f"  ❌ Número diferente: Atual={len(result_atual)}, 0.6.0={len(resultado_060)}")
else:
    all_identical = True
    for i, ((kw_a, score_a), (kw_e, score_e)) in enumerate(zip(result_atual, resultado_060), 1):
        if kw_a != kw_e:
            print(f"  ❌ Posição {i}: Keyword diferente")
            print(f"     Atual:   '{kw_a}'")
            print(f"     0.6.0:   '{kw_e}'")
            all_identical = False
        elif abs(score_a - score_e) > 1e-10:
            print(f"  ⚠️  Posição {i}: Score diferente ('{kw_a}')")
            print(f"     Atual: {score_a:.18f}")
            print(f"     0.6.0: {score_e:.18f}")
            print(f"     Diff:  {abs(score_a - score_e):.2e}")
            all_identical = False
    
    if all_identical:
        print(f"  ✅ IDÊNTICO! Todos os {len(result_atual)} resultados são iguais ao YAKE 0.6.0")
        match_status_test1 = True
    else:
        match_status_test1 = False

print()
print("="*80)

# Teste 2: test_n1_EN
print("\n🧪 TEST 2: test_n1_EN")
print("-"*80)

text_content = "machine learning artificial intelligence deep learning neural networks"
kw_extractor = yake.KeywordExtractor(lan="en", n=1, top=5)
result_atual = kw_extractor.extract_keywords(text_content)

# Resultados esperados do teste original
resultado_060 = [
    ('machine', 0.15831692877998726),
    ('intelligence', 0.15831692877998726),
    ('networks', 0.15831692877998726),
    ('deep', 0.19488865479360015),
    ('learning', 0.2973655825602151)
]

print("📦 YAKE 2.0 (atual):")
for i, (kw, score) in enumerate(result_atual, 1):
    print(f"  {i}. {kw:20s} {score:.18f}")

print("\n📦 YAKE 0.6.0 (esperado):")
for i, (kw, score) in enumerate(resultado_060, 1):
    print(f"  {i}. {kw:20s} {score:.18f}")

print("\n🔍 COMPARAÇÃO:")
all_identical = True
for i, ((kw_a, score_a), (kw_e, score_e)) in enumerate(zip(result_atual, resultado_060), 1):
    if kw_a != kw_e or abs(score_a - score_e) > 1e-15:
        print(f"  ❌ Diferença na posição {i}")
        all_identical = False

if all_identical:
    print(f"  ✅ IDÊNTICO! Todos os {len(result_atual)} resultados são iguais ao YAKE 0.6.0")
    match_status_test2 = True
else:
    match_status_test2 = False

print()
print("="*80)

# Teste 3: test_n3_PT
print("\n🧪 TEST 3: test_n3_PT (Português)")
print("-"*80)

text_content = """
Já são conhecidas as canções que estão na corrida para representar Portugal no Festival Eurovisão da Canção 2017, 
que este ano decorre em Kiev, na Ucrânia. As músicas a concurso são interpretadas por, entre outros, 
Diogo Piçarra, Marta Carvalho ou Leonor Andrade. As canções foram apresentadas durante a conferência de imprensa 
de lançamento da próxima edição do Festival da Canção, esta segunda-feira.
"""

kw_extractor = yake.KeywordExtractor(lan="pt", n=3, top=10)
result_atual = kw_extractor.extract_keywords(text_content)

# Resultados esperados
resultado_060 = [
    ('Festival da Canção', 0.0116215125517051),
    ('Eurovisão da Canção', 0.0127692939890272),
    ('Festival Eurovisão', 0.0163599425415126),
    ('da Canção', 0.019489690572460597),
    ('Canção', 0.0254786325430471),
    ('Festival', 0.026115644576321503),
    ('próxima edição', 0.029860943004833298),
    ('edição', 0.030778858039146203),
    ('músicas', 0.032632746415417804),
    ('Diogo Piçarra', 0.035303010985872105)
]

print("📦 YAKE 2.0 (atual):")
for i, (kw, score) in enumerate(result_atual, 1):
    print(f"  {i}. {kw:30s} {score:.18f}")

print("\n📦 YAKE 0.6.0 (esperado):")
for i, (kw, score) in enumerate(resultado_060, 1):
    print(f"  {i}. {kw:30s} {score:.18f}")

print("\n🔍 COMPARAÇÃO:")
all_identical = True
for i, ((kw_a, score_a), (kw_e, score_e)) in enumerate(zip(result_atual, resultado_060), 1):
    if kw_a != kw_e or abs(score_a - score_e) > 1e-15:
        print(f"  ❌ Diferença na posição {i}")
        all_identical = False

if all_identical:
    print(f"  ✅ IDÊNTICO! Todos os {len(result_atual)} resultados são iguais ao YAKE 0.6.0")
    match_status_test3 = True
else:
    match_status_test3 = False

print()
print("="*80)
print("📊 RESULTADO FINAL")
print("="*80)

if match_status_test1 and match_status_test2 and match_status_test3:
    print("✅ SIM! YAKE 2.0 produz resultados IDÊNTICOS ao YAKE 0.6.0")
    print("✅ Todos os testes baseline (test_n3_EN, test_n1_EN, test_n3_PT) passaram")
    print("✅ Keywords e scores são exatamente iguais")
else:
    print("⚠️  Existem diferenças entre YAKE 2.0 e YAKE 0.6.0")
    print(f"   test_n3_EN: {'✅' if match_status_test1 else '❌'}")
    print(f"   test_n1_EN: {'✅' if match_status_test2 else '❌'}")
    print(f"   test_n3_PT: {'✅' if match_status_test3 else '❌'}")

print("="*80)
