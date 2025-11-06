#!/usr/bin/env python3
# pylint: skip-file
"""
Comparador de Scores Externos
=============================

Este script permite comparar scores do YAKE! atual com scores
de referência fornecidos externamente (de outras versões ou datasets).
"""

import yake
import json
import sys
from typing import List, Dict, Tuple


class ExternalScoreComparator:
    """Classe para comparar com scores externos fornecidos"""
    
    def __init__(self):
        self.tolerance = 1e-10  # Tolerância para diferenças numéricas
        
    def compare_keywords(self, current_keywords: List[Tuple[str, float]], 
                        expected_keywords: List[Tuple[str, float]], 
                        test_name: str = "Test") -> bool:
        """Compara duas listas de keywords e seus scores"""
        
        print(f"\n🔍 Comparando: {test_name}")
        print("-" * (15 + len(test_name)))
        
        # Converter para dicionários para comparação mais fácil
        current_dict = {kw: score for kw, score in current_keywords}
        expected_dict = {kw: score for kw, score in expected_keywords}
        
        # Verificar se há keywords em comum
        current_kws = set(current_dict.keys())
        expected_kws = set(expected_dict.keys())
        
        common_kws = current_kws & expected_kws
        only_current = current_kws - expected_kws
        only_expected = expected_kws - current_kws
        
        print(f"   📊 Keywords atuais: {len(current_keywords)}")
        print(f"   📊 Keywords esperadas: {len(expected_keywords)}")
        print(f"   🔗 Em comum: {len(common_kws)}")
        
        if only_current:
            print(f"   ➕ Só na versão atual: {len(only_current)}")
            for kw in list(only_current)[:3]:
                print(f"      • {kw} = {current_dict[kw]:.8f}")
            if len(only_current) > 3:
                print(f"      ... e mais {len(only_current)-3}")
                
        if only_expected:
            print(f"   ➖ Só na versão esperada: {len(only_expected)}")
            for kw in list(only_expected)[:3]:
                print(f"      • {kw} = {expected_dict[kw]:.8f}")
            if len(only_expected) > 3:
                print(f"      ... e mais {len(only_expected)-3}")
        
        # Comparar scores das keywords em comum
        score_differences = []
        for kw in common_kws:
            current_score = current_dict[kw]
            expected_score = expected_dict[kw]
            diff = abs(current_score - expected_score)
            
            if diff > self.tolerance:
                score_differences.append((kw, current_score, expected_score, diff))
        
        if score_differences:
            print(f"   ❌ Diferenças de score: {len(score_differences)}")
            for kw, curr, exp, diff in score_differences[:5]:
                print(f"      • {kw}: {curr:.8f} ≠ {exp:.8f} (Δ={diff:.8f})")
            if len(score_differences) > 5:
                print(f"      ... e mais {len(score_differences)-5}")
            return False
        else:
            print(f"   ✅ Todos os scores idênticos (±{self.tolerance})")
            return True
    
    def test_with_reference_data(self, text: str, config: dict, 
                               expected_keywords: List[Tuple[str, float]], 
                               test_name: str = "Reference Test") -> bool:
        """Testa com dados de referência específicos"""
        
        try:
            # Extrair keywords com configuração fornecida
            extractor = yake.KeywordExtractor(**config)
            current_keywords = extractor.extract_keywords(text)
            
            # Comparar resultados
            return self.compare_keywords(current_keywords, expected_keywords, test_name)
            
        except Exception as e:
            print(f"❌ Erro durante extração: {e}")
            return False


def test_standard_examples():
    """Testa com exemplos padrão conhecidos"""
    
    comparator = ExternalScoreComparator()
    all_passed = True
    
    print("🧪 TESTE COM EXEMPLOS PADRÃO")
    print("=" * 30)
    
    # Exemplo 1: Texto simples, n=1
    text1 = "Machine learning is a subset of artificial intelligence."
    config1 = {"lan": "en", "n": 1, "dedupLim": 0.7, "top": 10}
    
    extractor1 = yake.KeywordExtractor(**config1)
    keywords1 = extractor1.extract_keywords(text1)
    
    print(f"\n📝 Exemplo 1 (n=1, texto simples):")
    print(f"   Texto: '{text1[:50]}...'")
    print(f"   Keywords extraídas: {len(keywords1)}")
    for i, (kw, score) in enumerate(keywords1[:5]):
        print(f"      {i+1}. {kw} → {score:.8f}")
    
    # Verificar por scores negativos
    negative1 = [(kw, score) for kw, score in keywords1 if score < 0]
    if negative1:
        print(f"   ❌ {len(negative1)} scores negativos encontrados!")
        all_passed = False
    else:
        print(f"   ✅ Sem scores negativos")
    
    # Exemplo 2: Texto médio, n=3
    text2 = """
    Natural language processing enables computers to understand human language.
    Machine learning algorithms can process large datasets efficiently.
    Deep learning networks perform complex pattern recognition tasks.
    """
    config2 = {"lan": "en", "n": 3, "dedupLim": 0.7, "top": 15}
    
    extractor2 = yake.KeywordExtractor(**config2)
    keywords2 = extractor2.extract_keywords(text2)
    
    print(f"\n📝 Exemplo 2 (n=3, texto médio):")
    print(f"   Keywords extraídas: {len(keywords2)}")
    for i, (kw, score) in enumerate(keywords2[:5]):
        print(f"      {i+1}. {kw} → {score:.8f}")
    
    # Verificar por scores negativos
    negative2 = [(kw, score) for kw, score in keywords2 if score < 0]
    if negative2:
        print(f"   ❌ {len(negative2)} scores negativos encontrados!")
        all_passed = False
    else:
        print(f"   ✅ Sem scores negativos")
    
    return all_passed, {
        "example1": {"text": text1, "config": config1, "keywords": keywords1},
        "example2": {"text": text2, "config": config2, "keywords": keywords2}
    }


def create_reference_template():
    """Cria template para dados de referência"""
    
    print(f"\n📋 TEMPLATE PARA DADOS DE REFERÊNCIA")
    print("=" * 35)
    
    template = {
        "test_cases": [
            {
                "name": "example_test",
                "text": "Your test text here",
                "config": {
                    "lan": "en",
                    "n": 3,
                    "dedupLim": 0.7,
                    "top": 20
                },
                "expected_keywords": [
                    ["keyword1", 0.12345678],
                    ["keyword2", 0.23456789],
                    ["keyword3", 0.34567890]
                ]
            }
        ]
    }
    
    print("Template JSON para comparação:")
    print(json.dumps(template, indent=2, ensure_ascii=False))
    
    return template


def main():
    """Função principal"""
    
    print("🔍 COMPARADOR DE SCORES EXTERNOS")
    print("=" * 35)
    
    print("\nOpções disponíveis:")
    print("1. Testar com exemplos padrão")
    print("2. Criar template para dados de referência")
    print("3. Comparar com arquivo JSON de referência")
    
    choice = input("\nEscolha (1/2/3): ").strip()
    
    if choice == "1":
        passed, examples = test_standard_examples()
        
        print(f"\n" + "=" * 50)
        if passed:
            print("✅ SUCESSO: Todos os exemplos padrão passaram!")
        else:
            print("❌ PROBLEMAS: Alguns exemplos apresentaram issues!")
        
        # Oferecer salvar como referência
        save = input("\nSalvar resultados como referência? (s/n): ").strip().lower()
        if save == 's':
            filename = "reference_scores.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(examples, f, indent=2, ensure_ascii=False)
            print(f"💾 Salvo em: {filename}")
        
        return passed
        
    elif choice == "2":
        create_reference_template()
        return True
        
    elif choice == "3":
        filename = input("Arquivo JSON de referência: ").strip()
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reference_data = json.load(f)
            
            comparator = ExternalScoreComparator()
            all_passed = True
            
            for test_case in reference_data.get("test_cases", []):
                passed = comparator.test_with_reference_data(
                    test_case["text"],
                    test_case["config"],
                    test_case["expected_keywords"],
                    test_case["name"]
                )
                if not passed:
                    all_passed = False
            
            print(f"\n" + "=" * 50)
            if all_passed:
                print("✅ SUCESSO: Todos os testes de referência passaram!")
            else:
                print("❌ FALHOU: Algumas diferenças encontradas!")
            
            return all_passed
            
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {filename}")
            return False
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
            return False
    
    else:
        print("❌ Opção inválida.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)