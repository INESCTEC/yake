#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""
ANÁLISE RIGOROSA: Comparação COMPLETA entre Original Publicada e YAKE 0.6.0/2.0

Testa TODOS os casos do boas.py e identifica TODAS as diferenças.
"""

import sys
import os

# YAKE 2.0 (atual)
import yake

# YAKE 0.6.0
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yake_0.6.0'))
import yake as yake_060


def compare_results(name, original_expected, yake_060_actual, yake_20_actual, show_keywords=True):
    """Compara resultados em detalhe."""
    print(f"\n{'='*100}")
    print(f"TESTE: {name}")
    print(f"{'='*100}")
    
    # Verificar se são idênticos
    identical_060_20 = (yake_060_actual == yake_20_actual)
    identical_orig_060 = (original_expected == yake_060_actual)
    identical_orig_20 = (original_expected == yake_20_actual)
    
    print(f"\n🔍 Verificação de Identidade:")
    print(f"   YAKE 0.6.0 == YAKE 2.0:          {'✅ IDÊNTICOS' if identical_060_20 else '❌ DIFERENTES'}")
    print(f"   Original == YAKE 0.6.0:          {'✅ IDÊNTICOS' if identical_orig_060 else '❌ DIFERENTES'}")
    print(f"   Original == YAKE 2.0:            {'✅ IDÊNTICOS' if identical_orig_20 else '❌ DIFERENTES'}")
    
    if not identical_orig_060:
        print(f"\n⚠️  ATENÇÃO: Há diferenças entre Original Publicada e YAKE 0.6.0/2.0")
        
        # Comparar keyword por keyword
        print(f"\n📊 Comparação Detalhada (Top-20):")
        print(f"{'Pos':<5} {'Original':<30} {'YAKE 0.6.0':<30} {'YAKE 2.0':<30} {'Status':<15}")
        print("-" * 115)
        
        max_len = max(len(original_expected), len(yake_060_actual), len(yake_20_actual))
        
        differences = []
        for i in range(min(20, max_len)):
            orig_kw = original_expected[i][0] if i < len(original_expected) else "---"
            orig_score = f"{original_expected[i][1]:.6f}" if i < len(original_expected) else "---"
            
            kw_060 = yake_060_actual[i][0] if i < len(yake_060_actual) else "---"
            score_060 = f"{yake_060_actual[i][1]:.6f}" if i < len(yake_060_actual) else "---"
            
            kw_20 = yake_20_actual[i][0] if i < len(yake_20_actual) else "---"
            score_20 = f"{yake_20_actual[i][1]:.6f}" if i < len(yake_20_actual) else "---"
            
            # Status
            if orig_kw == kw_060 == kw_20:
                status = "✅ Igual"
            elif kw_060 == kw_20 != orig_kw:
                status = "⚠️ Difere Orig"
                differences.append({
                    'pos': i+1,
                    'original': orig_kw,
                    'new': kw_060
                })
            else:
                status = "❌ Todos Dif"
            
            orig_str = f"{orig_kw:<15} ({orig_score})"
            kw_060_str = f"{kw_060:<15} ({score_060})"
            kw_20_str = f"{kw_20:<15} ({score_20})"
            
            print(f"{i+1:<5} {orig_str:<30} {kw_060_str:<30} {kw_20_str:<30} {status:<15}")
        
        if differences:
            print(f"\n🔴 DIFERENÇAS ENCONTRADAS ({len(differences)}):")
            for diff in differences:
                print(f"   Posição {diff['pos']:2}: '{diff['original']}' → '{diff['new']}'")
        
        # Verificar se há keywords que estão em uma versão mas não em outra (top-20)
        orig_keywords = set([kw for kw, _ in original_expected[:20]])
        new_keywords = set([kw for kw, _ in yake_060_actual[:20]])
        
        only_in_orig = orig_keywords - new_keywords
        only_in_new = new_keywords - orig_keywords
        
        if only_in_orig or only_in_new:
            print(f"\n🔄 KEYWORDS TROCADAS:")
            if only_in_orig:
                print(f"   Saíram do top-20: {only_in_orig}")
            if only_in_new:
                print(f"   Entraram no top-20: {only_in_new}")
    
    return {
        'identical_060_20': identical_060_20,
        'identical_orig_060': identical_orig_060,
        'identical_orig_20': identical_orig_20
    }


# ============================================================================
# TESTE 1: test_n1_EN
# ============================================================================

text_n1_en = '''
Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner'''

original_n1_en = [
    ('Google', 0.02509259635302287), ('Kaggle', 0.027297150442917317), ('data', 0.07999958986489127), 
    ('science', 0.09834167930168546), ('platform', 0.12404419723925647), ('service', 0.1316357590449064), 
    ('acquiring', 0.15110282570329972), ('learning', 0.1620911439042445), ('Goldbloom', 0.1624845364505264), 
    ('machine', 0.16721860165903407), ('competition', 0.1826862004451857), ('Cloud', 0.1849060668345104), 
    ('community', 0.202661778267609), ('Ventures', 0.2258881919825325), ('declined', 0.2872980816826787), 
    ('San', 0.2893636939471809), ('Francisco', 0.2893636939471809), ('early', 0.2946076840223411), 
    ('acquisition', 0.2991070691689808), ('scientists', 0.3046548516998034)
]

kw_060_n1_en = yake_060.KeywordExtractor(lan="en", n=1, top=20)
kw_20_n1_en = yake.KeywordExtractor(lan="en", n=1, top=20)

result_060_n1_en = kw_060_n1_en.extract_keywords(text_n1_en)
result_20_n1_en = kw_20_n1_en.extract_keywords(text_n1_en)

results_n1_en = compare_results("test_n1_EN (n=1, English)", original_n1_en, result_060_n1_en, result_20_n1_en)


# ============================================================================
# TESTE 2: test_n3_EN
# ============================================================================

text_n3_en = text_n1_en  # Mesmo texto

original_n3_en = [
    ('Google', 0.02509259635302287), ('Kaggle', 0.027297150442917317),
    ('CEO Anthony Goldbloom', 0.04834891465259988), ('data science', 0.05499112888517541),
    ('acquiring data science', 0.06029572445726576), ('Google Cloud Platform', 0.07461585862381104),
    ('data', 0.07999958986489127), ('San Francisco', 0.0913829662674319),
    ('Anthony Goldbloom declined', 0.09740885820462175), ('science', 0.09834167930168546),
    ('science community Kaggle', 0.1014394718805728), ('machine learning', 0.10754988562466912),
    ('Google Cloud', 0.1136787749431024), ('Google is acquiring', 0.114683257931042),
    ('acquiring Kaggle', 0.12012386507741751), ('Anthony Goldbloom', 0.1213027418574554),
    ('platform', 0.12404419723925647), ('co-founder CEO Anthony', 0.12411964553586782),
    ('CEO Anthony', 0.12462950727635251), ('service', 0.1316357590449064)
]

kw_060_n3_en = yake_060.KeywordExtractor(lan="en", n=3, top=20)
kw_20_n3_en = yake.KeywordExtractor(lan="en", n=3, top=20)

result_060_n3_en = kw_060_n3_en.extract_keywords(text_n3_en)
result_20_n3_en = kw_20_n3_en.extract_keywords(text_n3_en)

results_n3_en = compare_results("test_n3_EN (n=3, English)", original_n3_en, result_060_n3_en, result_20_n3_en)


# ============================================================================
# TESTE 3: test_n3_PT
# ============================================================================

text_n3_pt = '''
"Conta-me Histórias." Xutos inspiram projeto premiado. A plataforma "Conta-me Histórias" foi distinguida com o Prémio Arquivo.pt, atribuído a trabalhos inovadores de investigação ou aplicação de recursos preservados da Web, através dos serviços de pesquisa e acesso disponibilizados publicamente pelo Arquivo.pt . Nesta plataforma em desenvolvimento, o utilizador pode pesquisar sobre qualquer tema e ainda executar alguns exemplos predefinidos. Como forma de garantir a pluralidade e diversidade de fontes de informação, esta são utilizadas 24 fontes de notícias eletrónicas, incluindo a TSF. Uma versão experimental (beta) do "Conta-me Histórias" está disponível aqui.
A plataforma foi desenvolvida por Ricardo Campos investigador do LIAAD do INESC TEC e docente do Instituto Politécnico de Tomar, Arian Pasquali e Vitor Mangaravite, também investigadores do LIAAD do INESC TEC, Alípio Jorge, coordenador do LIAAD do INESC TEC e docente na Faculdade de Ciências da Universidade do Porto, e Adam Jatwot docente da Universidade de Kyoto.
'''

original_n3_pt = [
    ('Conta-me Histórias', 0.006225012963810038),
    ('LIAAD do INESC', 0.01899063587015275),
    ('INESC TEC', 0.01995432290332246),
    ('Conta-me', 0.04513273690417472),
    ('Histórias', 0.04513273690417472),
    ('Prémio Arquivo.pt', 0.05749361520927859),
    ('LIAAD', 0.07738867367929901),
    ('INESC', 0.07738867367929901),
    ('TEC', 0.08109398065524037),
    ('Xutos inspiram projeto', 0.08720742489353424),
    ('inspiram projeto premiado', 0.08720742489353424),
    ('Adam Jatwot docente', 0.09407053486771558),
    ('Arquivo.pt', 0.10261392141666957),
    ('Alípio Jorge', 0.12190479662535166),
    ('Ciências da Universidade', 0.12368384021490342),
    ('Ricardo Campos investigador', 0.12789997272332762),
    ('Politécnico de Tomar', 0.13323587141127738),
    ('Arian Pasquali', 0.13323587141127738),
    ('Vitor Mangaravite', 0.13323587141127738),
    ('preservados da Web', 0.13596322680882506)
]

kw_060_n3_pt = yake_060.KeywordExtractor(lan="pt", n=3, top=20)
kw_20_n3_pt = yake.KeywordExtractor(lan="pt", n=3, top=20)

result_060_n3_pt = kw_060_n3_pt.extract_keywords(text_n3_pt)
result_20_n3_pt = kw_20_n3_pt.extract_keywords(text_n3_pt)

results_n3_pt = compare_results("test_n3_PT (n=3, Portuguese)", original_n3_pt, result_060_n3_pt, result_20_n3_pt)


# ============================================================================
# TESTE 4: test_n1_EL (Greek)
# ============================================================================

text_n1_el = '''
Ανώτατος διοικητής του ρωσικού στρατού φέρεται να σκοτώθηκε κοντά στο Χάρκοβο, σύμφωνα με την υπηρεσία πληροφοριών του υπουργείου Άμυνας της Ουκρανίας. Σύμφωνα με δήλωση του υπουργείου Άμυνας της Ουκρανίας, πρόκειται για τον Vitaly Gerasimov, υποστράτηγο και υποδιοικητή από την Κεντρική Στρατιωτική Περιφέρεια της Ρωσίας.'''

original_n1_el = [
    ('Ουκρανίας', 0.04685829498124156), ('Χάρκοβο', 0.0630891548728466), ('Άμυνας', 0.06395408991254226), 
    ('σύμφωνα', 0.07419311338418161), ('υπουργείου', 0.1069960715371627), ('Ανώτατος', 0.12696931063105557), 
    ('διοικητής', 0.18516501832552387), ('ρωσικού', 0.18516501832552387), ('στρατού', 0.18516501832552387), 
    ('φέρεται', 0.18516501832552387), ('σκοτώθηκε', 0.18516501832552387), ('κοντά', 0.18516501832552387), 
    ('υπηρεσία', 0.18516501832552387), ('πληροφοριών', 0.18516501832552387), ('Gerasimov', 0.1895400421770795), 
    ('Ρωσίας', 0.1895400421770795), ('Vitaly', 0.24366598777562623), ('Κεντρική', 0.24366598777562623), 
    ('Στρατιωτική', 0.24366598777562623), ('Περιφέρεια', 0.24366598777562623)
]

kw_060_n1_el = yake_060.KeywordExtractor(lan="el", n=1, top=20)
kw_20_n1_el = yake.KeywordExtractor(lan="el", n=1, top=20)

result_060_n1_el = kw_060_n1_el.extract_keywords(text_n1_el)
result_20_n1_el = kw_20_n1_el.extract_keywords(text_n1_el)

results_n1_el = compare_results("test_n1_EL (n=1, Greek)", original_n1_el, result_060_n1_el, result_20_n1_el)


# ============================================================================
# RESUMO GERAL
# ============================================================================

print(f"\n\n{'='*100}")
print("RESUMO FINAL - ANÁLISE COMPLETA")
print(f"{'='*100}\n")

all_results = {
    'test_n1_EN': results_n1_en,
    'test_n3_EN': results_n3_en,
    'test_n3_PT': results_n3_pt,
    'test_n1_EL': results_n1_el
}

print("📊 Status de Compatibilidade:\n")
print(f"{'Teste':<20} {'0.6.0 == 2.0':<20} {'Orig == 0.6.0':<20} {'Orig == 2.0':<20}")
print("-" * 80)

for test_name, result in all_results.items():
    status_060_20 = "✅ Idênticos" if result['identical_060_20'] else "❌ Diferentes"
    status_orig_060 = "✅ Idênticos" if result['identical_orig_060'] else "❌ Diferentes"
    status_orig_20 = "✅ Idênticos" if result['identical_orig_20'] else "❌ Diferentes"
    
    print(f"{test_name:<20} {status_060_20:<20} {status_orig_060:<20} {status_orig_20:<20}")

# Contar quantos testes são idênticos
total_tests = len(all_results)
identical_060_20_count = sum([1 for r in all_results.values() if r['identical_060_20']])
identical_orig_060_count = sum([1 for r in all_results.values() if r['identical_orig_060']])

print(f"\n📈 Estatísticas:\n")
print(f"   Total de testes: {total_tests}")
print(f"   YAKE 0.6.0 == YAKE 2.0: {identical_060_20_count}/{total_tests} ({identical_060_20_count/total_tests*100:.0f}%)")
print(f"   Original == YAKE 0.6.0/2.0: {identical_orig_060_count}/{total_tests} ({identical_orig_060_count/total_tests*100:.0f}%)")

print(f"\n{'='*100}")
print("CONCLUSÃO")
print(f"{'='*100}\n")

if identical_060_20_count == total_tests:
    print("✅ CONFIRMADO: YAKE 0.6.0 e YAKE 2.0 produzem resultados 100% IDÊNTICOS")
else:
    print(f"⚠️  ATENÇÃO: YAKE 0.6.0 e YAKE 2.0 diferem em {total_tests - identical_060_20_count} teste(s)")

if identical_orig_060_count == total_tests:
    print("✅ Original Publicada e YAKE 0.6.0/2.0 são IDÊNTICOS")
    print("\n💡 RECOMENDAÇÃO: Pode usar qualquer versão como baseline")
elif identical_orig_060_count == 0:
    print("❌ Original Publicada e YAKE 0.6.0/2.0 DIFEREM EM TODOS OS TESTES")
    print("\n💡 RECOMENDAÇÃO: Houve mudança significativa no algoritmo")
    print("   Decisão necessária: Usar Original ou YAKE 0.6.0/2.0 como baseline?")
else:
    print(f"⚠️  Original Publicada e YAKE 0.6.0/2.0 diferem em {total_tests - identical_orig_060_count} teste(s)")
    print("\n💡 RECOMENDAÇÃO: Análise caso-a-caso necessária")

print(f"\n{'='*100}\n")
