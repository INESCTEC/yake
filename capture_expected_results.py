# pylint: skip-file
"""Script para capturar resultados esperados dos novos testes"""

import yake

# Test n4_EN - capturar resultado esperado
text = """
Artificial intelligence and machine learning technologies 
enable deep neural network architectures to process data.
"""

kw = yake.KeywordExtractor(lan="en", n=4, top=10)
result = kw.extract_keywords(text)

print("=" * 80)
print("test_n4_EN - Resultados:")
print("=" * 80)
for keyword, score in result:
    print(f'    ("{keyword}", {score}),')

print("\n" + "=" * 80)
print("test_composed_word_different_sizes - n=4:")
print("=" * 80)

text2 = """
Artificial intelligence and machine learning technologies 
enable deep neural network architectures to process data.
"""

kw4 = yake.KeywordExtractor(lan="en", n=4, top=5)
result4 = kw4.extract_keywords(text2)

print("n=4 results:")
for keyword, score in result4:
    print(f'    ("{keyword}", {score}),')
    # Validar que não há scores negativos
    assert score > 0.0, f"ERRO: Score negativo para '{keyword}': {score}"

print("\n✅ Nenhum score negativo detectado!")

print("\n" + "=" * 80)
print("test_multilingual_support - German:")
print("=" * 80)

text_de = "Die künstliche Intelligenz verändert die Welt"
kw_de = yake.KeywordExtractor(lan="de", n=2, top=5)
result_de = kw_de.extract_keywords(text_de)

for keyword, score in result_de:
    print(f'    ("{keyword}", {score}),')

print("\n" + "=" * 80)
print("test_multilingual_support - French:")
print("=" * 80)

text_fr = "L'intelligence artificielle transforme le monde"
kw_fr = yake.KeywordExtractor(lan="fr", n=2, top=5)
result_fr = kw_fr.extract_keywords(text_fr)

for keyword, score in result_fr:
    print(f'    ("{keyword}", {score}),')

print("\n" + "=" * 80)
print("test_composed_word_update_h_with_consecutive_stopwords - n=4:")
print("=" * 80)

text3 = "This is a test of the new algorithm for machine learning"
kw = yake.KeywordExtractor(lan="en", n=4, top=10)
result = kw.extract_keywords(text3)

print("Results with consecutive stopwords:")
for keyword, score in result:
    print(f'    ("{keyword}", {score}),')
    assert score > 0.0, f"ERRO: Score negativo para '{keyword}': {score}"

print("\n✅ Teste de consecutive stopwords OK - sem scores negativos!")
