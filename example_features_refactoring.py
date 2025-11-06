# pylint: skip-file
"""
Exemplos de uso das funções de features isoladas.

Demonstra como as refatorações baseadas na versão de referência
melhoram testabilidade e flexibilidade.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from yake import calculate_term_features, calculate_composed_features
from yake.data.single_word import SingleWord
from yake.data.composed_word import ComposedWord
import networkx as nx


def example_1_isolated_term_features():
    """Exemplo 1: Calcular features de um termo isoladamente."""
    print("=" * 60)
    print("EXEMPLO 1: Features Isoladas de Termo")
    print("=" * 60)

    # Criar um grafo mock simples
    g = nx.DiGraph()

    # Criar termo
    term = SingleWord("machine", 0, g)
    term.tf = 10
    term.tf_a = 0
    term.tf_n = 2  # Aparece como nome próprio 2x
    term.sentence_ids = {0, 1, 3, 5}  # Aparece em 4 sentenças
    term.occurs = {2: 1, 15: 1, 28: 1, 45: 1}  # Posições no texto

    # Adicionar algumas arestas para simular co-ocorrências
    g.add_node(term.id, unique=term.unique)
    g.add_edge(term.id, 1, tf=3.0)
    g.add_edge(2, term.id, tf=2.0)

    # Calcular features sem precisar de DataCore completo
    features = calculate_term_features(
        term=term,
        max_tf=15,  # TF máximo no documento
        avg_tf=5.2,  # Média de TF
        std_tf=3.1,  # Desvio padrão de TF
        number_of_sentences=10  # Total de sentenças
    )

    # Mostrar resultados
    print(f"Termo: '{term.unique}'")
    print(f"  TF: {term.tf}")
    print(f"  TF_N (nome próprio): {term.tf_n}")
    print(f"  Sentenças: {len(term.sentence_ids)}")
    print(f"\nFeatures Calculadas:")
    print(f"  W_Rel (relevância): {features['w_rel']:.4f}")
    print(f"  W_Freq (frequência): {features['w_freq']:.4f}")
    print(f"  W_Spread (dispersão): {features['w_spread']:.4f}")
    print(f"  W_Case (maiúsculas): {features['w_case']:.4f}")
    print(f"  W_Pos (posição): {features['w_pos']:.4f}")
    print(f"  H (score final): {features['h']:.4f}")
    print()


def example_2_stopword_strategies():
    """Exemplo 2: Comparar estratégias de tratamento de stopwords."""
    print("=" * 60)
    print("EXEMPLO 2: Comparação de Estratégias de Stopwords")
    print("=" * 60)

    # Criar grafo mock
    g = nx.DiGraph()

    # Criar termos para a frase "machine learning algorithm"
    # onde "learning" pode ser considerado stopword em alguns contextos
    term1 = SingleWord("machine", 0, g)
    term1.h = 0.15
    term1.tf = 5
    term1.stopword = False
    g.add_node(0, unique="machine")

    term2 = SingleWord("learning", 1, g)
    term2.h = 0.45  # Stopword com score alto
    term2.tf = 8
    term2.stopword = True
    g.add_node(1, unique="learning")

    term3 = SingleWord("algorithm", 2, g)
    term3.h = 0.12
    term3.tf = 4
    term3.stopword = False
    g.add_node(2, unique="algorithm")

    # Adicionar arestas simulando co-ocorrências
    g.add_edge(0, 1, tf=4.0)
    g.add_edge(1, 2, tf=3.0)

    # Criar ComposedWord
    composed = ComposedWord([term1, term2, term3])
    composed.tf = 4

    # Testar diferentes estratégias
    print("Frase: 'machine learning algorithm'")
    print("(onde 'learning' é stopword)\n")

    strategies = {
        'bi': 'BiWeight (probabilidade de conexão)',
        'h': 'HWeight (inclui H da stopword)',
        'none': 'None (ignora stopword)'
    }

    for strategy, description in strategies.items():
        features = calculate_composed_features(
            composed_word=composed,
            stopword_weight=strategy
        )

        print(f"Estratégia: {strategy} - {description}")
        print(f"  prod_h: {features['prod_h']:.4f}")
        print(f"  sum_h: {features['sum_h']:.4f}")
        print(f"  H final: {features['h']:.4f}")
        print()


def example_3_benchmarking_features():
    """Exemplo 3: Benchmark de diferentes configurações."""
    import time

    print("=" * 60)
    print("EXEMPLO 3: Benchmark de Cálculo de Features")
    print("=" * 60)

    # Criar 1000 termos mock
    g = nx.DiGraph()
    terms = []
    for i in range(1000):
        term = SingleWord(f"term_{i}", i, g)
        term.tf = i % 20 + 1
        term.tf_a = i % 5
        term.tf_n = i % 3
        term.sentence_ids = {j for j in range(i % 10)}
        term.occurs = {j*10: 1 for j in range(i % 15)}
        terms.append(term)

    # Benchmark: calcular features para todos os termos
    start = time.perf_counter()

    for term in terms:
        features = calculate_term_features(
            term=term,
            max_tf=20,
            avg_tf=10,
            std_tf=5,
            number_of_sentences=100
        )

    elapsed = (time.perf_counter() - start) * 1000

    print(f"Calculadas features para {len(terms)} termos")
    print(f"Tempo total: {elapsed:.2f}ms")
    print(f"Média por termo: {elapsed/len(terms):.4f}ms")
    print(f"\n✅ Função isolada permite benchmark preciso!")
    print()


def example_4_unit_testing():
    """Exemplo 4: Como testar facilmente."""
    print("=" * 60)
    print("EXEMPLO 4: Testabilidade Melhorada")
    print("=" * 60)

    # Teste de caso extremo: termo com TF = 0
    g = nx.DiGraph()
    term = SingleWord("rare", 0, g)
    term.tf = 0  # Zero occorrências!
    term.tf_a = 0
    term.tf_n = 0
    term.sentence_ids = set()
    term.occurs = {}
    g.add_node(0, unique="rare")

    try:
        features = calculate_term_features(
            term=term,
            max_tf=1,
            avg_tf=0.5,
            std_tf=0.1,
            number_of_sentences=1
        )
        print("✅ Teste edge case (TF=0): PASSOU")
        print(f"   H score: {features['h']}")
    except Exception as e:
        print(f"❌ Teste edge case (TF=0): FALHOU - {e}")

    # Teste de valores esperados
    g2 = nx.DiGraph()
    term2 = SingleWord("test", 0, g2)
    term2.tf = 10
    term2.tf_a = 0
    term2.tf_n = 0
    term2.sentence_ids = {0, 1, 2}
    term2.occurs = {5: 1, 10: 1, 15: 1}
    g2.add_node(0, unique="test")

    features2 = calculate_term_features(
        term=term2,
        max_tf=10,
        avg_tf=5,
        std_tf=2,
        number_of_sentences=5
    )

    # Verificar que W_Spread está correto
    expected_spread = 3 / 5  # 3 sentenças de 5 total
    actual_spread = features2['w_spread']

    if abs(expected_spread - actual_spread) < 0.0001:
        print("✅ Teste W_Spread: PASSOU")
        print(f"   Esperado: {expected_spread:.4f}, Obtido: {actual_spread:.4f}")
    else:
        print("❌ Teste W_Spread: FALHOU")

    print(f"\n✅ Features isoladas são muito mais fáceis de testar!")
    print()


if __name__ == "__main__":
    print("\n🔬 DEMONSTRAÇÃO: Refatorações Baseadas na Versão de Referência")
    print("Arquivo: yake/data/features.py")
    print()

    example_1_isolated_term_features()
    example_2_stopword_strategies()
    example_3_benchmarking_features()
    example_4_unit_testing()

    print("=" * 60)
    print("✅ CONCLUSÃO")
    print("=" * 60)
    print("A separação de features em módulo dedicado oferece:")
    print("  1. Testabilidade: Testes unitários sem mocks complexos")
    print("  2. Benchmark: Medição precisa de performance")
    print("  3. Flexibilidade: Experimentar diferentes estratégias")
    print("  4. Clareza: Código mais legível e manutenível")
    print()
