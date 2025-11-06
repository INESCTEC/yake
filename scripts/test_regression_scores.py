#!/usr/bin/env python3
# pylint: skip-file
"""
Testes de Regressão para Validar Scores do YAKE!
================================================

Este script testa se as otimizações implementadas mantêm os scores
exatamente iguais à versão original, testando com diferentes:
- Tamanhos de n-gramas (1 até 9)
- Diferentes tipos de texto
- Diferentes configurações
- Diferentes idiomas

Objetivo: Garantir que nenhuma otimização alterou os resultados algorítmicos.
"""

import yake
import time
import json
import hashlib
from datetime import datetime
from collections import OrderedDict


class YakeRegressionTester:
    """Classe para testar regressão de scores do YAKE!"""
    
    def __init__(self):
        self.test_results = []
        self.baseline_scores = {}
        
    def generate_test_cases(self):
        """Gera casos de teste abrangentes"""
        
        test_cases = []
        
        # Textos de teste variados
        texts = {
            "short_english": "Machine learning algorithms and artificial intelligence.",
            
            "medium_english": """
            Machine learning algorithms and artificial intelligence systems are 
            revolutionizing data science research in computer science. These 
            technologies enable advanced analytics and predictive modeling for 
            business intelligence applications across various industries.
            """,
            
            "long_english": """
            Machine learning algorithms and artificial intelligence systems are 
            revolutionizing data science research in computer science and technology 
            innovation. These advanced technologies enable sophisticated analytics, 
            predictive modeling, and business intelligence applications across various 
            industries including healthcare, finance, automotive, and telecommunications.
            
            Natural language processing and computer vision are key areas of artificial 
            intelligence that leverage deep learning neural networks and statistical 
            machine learning methods. These approaches process large datasets to extract 
            meaningful insights and patterns for automated decision making systems.
            
            Data scientists and machine learning engineers collaborate to develop 
            scalable solutions using cloud computing platforms and distributed processing 
            frameworks. The integration of big data technologies with advanced analytics 
            enables organizations to gain competitive advantages through data-driven 
            decision making and intelligent automation of business processes.
            """,
            
            "technical_text": """
            The implementation of convolutional neural networks (CNNs) in computer vision 
            applications requires careful consideration of architectural design patterns, 
            optimization algorithms, and regularization techniques. Backpropagation 
            algorithms enable gradient-based optimization of network parameters through 
            stochastic gradient descent and its variants such as Adam, RMSprop, and 
            AdaGrad optimizers.
            """,
            
            "mixed_content": """
            Python programming language offers excellent libraries for machine learning 
            including scikit-learn, TensorFlow, PyTorch, and Keras. These frameworks 
            provide high-level APIs for building, training, and deploying deep learning 
            models. The NumPy and Pandas libraries handle numerical computing and data 
            manipulation tasks efficiently. Matplotlib and Seaborn enable comprehensive 
            data visualization and exploratory data analysis workflows.
            """,
        }
        
        # Configurações de teste
        configs = [
            {"lan": "en", "n": 1, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 2, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 3, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 4, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 5, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 6, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 7, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 8, "dedupLim": 0.7, "top": 20},
            {"lan": "en", "n": 9, "dedupLim": 0.7, "top": 20},
        ]
        
        # Configurações adicionais com diferentes parâmetros
        additional_configs = [
            {"lan": "en", "n": 3, "dedupLim": 0.5, "top": 10},
            {"lan": "en", "n": 3, "dedupLim": 0.9, "top": 15},
            {"lan": "en", "n": 3, "dedupLim": 1.0, "top": 25}, # sem deduplicação
            {"lan": "en", "n": 4, "dedupLim": 0.3, "top": 30},
            {"lan": "en", "n": 5, "dedupLim": 0.8, "top": 12},
        ]
        
        # Combinar todos os textos com todas as configurações
        test_id = 0
        for text_name, text_content in texts.items():
            for config in configs + additional_configs:
                test_cases.append({
                    "id": test_id,
                    "text_name": text_name,
                    "text": text_content.strip(),
                    "config": config.copy(),
                    "description": f"{text_name}_n{config['n']}_dedup{config['dedupLim']}_top{config['top']}"
                })
                test_id += 1
                
        return test_cases
    
    def run_single_test(self, test_case):
        """Executa um único teste e captura os resultados"""
        
        try:
            # Configurar extrator
            config = test_case["config"]
            extractor = yake.KeywordExtractor(
                lan=config["lan"],
                n=config["n"], 
                dedupLim=config["dedupLim"],
                top=config["top"]
            )
            
            # Medir tempo de execução
            start_time = time.perf_counter()
            keywords = extractor.extract_keywords(test_case["text"])
            execution_time = time.perf_counter() - start_time
            
            # Criar resultado estruturado
            result = {
                "test_id": test_case["id"],
                "description": test_case["description"],
                "text_name": test_case["text_name"],
                "config": config,
                "execution_time_ms": round(execution_time * 1000, 3),
                "num_keywords": len(keywords),
                "keywords": keywords,
                "success": True,
                "error": None
            }
            
            # Gerar hash dos scores para comparação rápida
            scores_str = ";".join([f"{kw}:{score:.10f}" for kw, score in keywords])
            result["scores_hash"] = hashlib.md5(scores_str.encode()).hexdigest()
            
            return result
            
        except Exception as e:
            return {
                "test_id": test_case["id"],
                "description": test_case["description"],
                "text_name": test_case["text_name"],
                "config": config,
                "execution_time_ms": None,
                "num_keywords": 0,
                "keywords": [],
                "success": False,
                "error": str(e),
                "scores_hash": None
            }
    
    def run_regression_tests(self, save_baseline=False):
        """Executa todos os testes de regressão"""
        
        print("🧪 TESTE DE REGRESSÃO DE SCORES DO YAKE!")
        print("=" * 50)
        print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Gerar casos de teste
        test_cases = self.generate_test_cases()
        print(f"📊 Total de testes: {len(test_cases)}")
        
        # Executar testes
        results = []
        passed_tests = 0
        failed_tests = 0
        
        for i, test_case in enumerate(test_cases):
            print(f"\r⏳ Executando teste {i+1}/{len(test_cases)}: {test_case['description'][:50]}...", end="")
            
            result = self.run_single_test(test_case)
            results.append(result)
            
            if result["success"]:
                passed_tests += 1
            else:
                failed_tests += 1
        
        print()  # Nova linha após o progresso
        
        # Salvar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if save_baseline:
            filename = f"baseline_scores_{timestamp}.json"
            print(f"\n💾 Salvando baseline em: {filename}")
        else:
            filename = f"regression_test_results_{timestamp}.json"
            print(f"\n💾 Salvando resultados em: {filename}")
        
        test_report = {
            "timestamp": timestamp,
            "total_tests": len(test_cases),
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": round((passed_tests / len(test_cases)) * 100, 2),
            "test_type": "baseline" if save_baseline else "regression",
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_report, f, indent=2, ensure_ascii=False)
        
        return test_report
    
    def compare_with_baseline(self, baseline_file, current_results=None):
        """Compara resultados atuais com baseline"""
        
        print(f"\n🔍 COMPARAÇÃO COM BASELINE")
        print("=" * 30)
        
        # Carregar baseline
        try:
            with open(baseline_file, 'r', encoding='utf-8') as f:
                baseline = json.load(f)
                baseline_results = {r["test_id"]: r for r in baseline["results"]}
        except FileNotFoundError:
            print(f"❌ Arquivo baseline não encontrado: {baseline_file}")
            return False
        
        # Usar resultados atuais ou executar novos testes
        if current_results is None:
            print("🔄 Executando testes atuais...")
            current_results = self.run_regression_tests()
        
        current_results_dict = {r["test_id"]: r for r in current_results["results"]}
        
        # Comparar resultados
        identical_count = 0
        different_count = 0
        missing_count = 0
        differences = []
        
        for test_id, baseline_result in baseline_results.items():
            if test_id not in current_results_dict:
                missing_count += 1
                continue
                
            current_result = current_results_dict[test_id]
            
            # Comparar hashes dos scores
            baseline_hash = baseline_result.get("scores_hash")
            current_hash = current_result.get("scores_hash")
            
            if baseline_hash == current_hash:
                identical_count += 1
            else:
                different_count += 1
                differences.append({
                    "test_id": test_id,
                    "description": baseline_result["description"],
                    "baseline_keywords": len(baseline_result.get("keywords", [])),
                    "current_keywords": len(current_result.get("keywords", [])),
                    "baseline_hash": baseline_hash,
                    "current_hash": current_hash
                })
        
        # Relatório de comparação
        print(f"\n📊 RESULTADOS DA COMPARAÇÃO:")
        print(f"   ✅ Testes idênticos: {identical_count}")
        print(f"   ❌ Testes diferentes: {different_count}")
        print(f"   ⚠️  Testes ausentes: {missing_count}")
        
        if different_count == 0:
            print(f"\n🎉 SUCESSO! Todos os scores permanecem idênticos!")
            print(f"   ✅ {identical_count} testes passaram na regressão")
            return True
        else:
            print(f"\n⚠️  ATENÇÃO! Encontradas {different_count} diferenças:")
            for diff in differences[:10]:  # Mostrar apenas as primeiras 10
                print(f"   • {diff['description']}")
                print(f"     Baseline: {diff['baseline_keywords']} keywords ({diff['baseline_hash'][:8]}...)")
                print(f"     Atual: {diff['current_keywords']} keywords ({diff['current_hash'][:8]}...)")
            
            if len(differences) > 10:
                print(f"   ... e mais {len(differences) - 10} diferenças")
            
            return False
    
    def generate_detailed_report(self, results):
        """Gera relatório detalhado dos testes"""
        
        print(f"\n📋 RELATÓRIO DETALHADO")
        print("=" * 25)
        
        # Agrupar por n-grama
        by_ngram = {}
        for result in results["results"]:
            n = result["config"]["n"]
            if n not in by_ngram:
                by_ngram[n] = []
            by_ngram[n].append(result)
        
        for n in sorted(by_ngram.keys()):
            ngram_results = by_ngram[n]
            success_count = sum(1 for r in ngram_results if r["success"])
            avg_time = sum(r["execution_time_ms"] for r in ngram_results if r["execution_time_ms"]) / len(ngram_results)
            avg_keywords = sum(r["num_keywords"] for r in ngram_results if r["success"]) / max(success_count, 1)
            
            print(f"\n🔹 N-grama {n}:")
            print(f"   📊 Testes: {success_count}/{len(ngram_results)} sucessos")
            print(f"   ⏱️  Tempo médio: {avg_time:.2f}ms")
            print(f"   🎯 Keywords médias: {avg_keywords:.1f}")
        
        # Verificar scores negativos
        negative_scores_found = False
        for result in results["results"]:
            if result["success"]:
                for keyword, score in result["keywords"]:
                    if score < 0:
                        if not negative_scores_found:
                            print(f"\n⚠️  SCORES NEGATIVOS ENCONTRADOS:")
                            negative_scores_found = True
                        print(f"   • {result['description']}: '{keyword}' = {score}")
        
        if not negative_scores_found:
            print(f"\n✅ Nenhum score negativo encontrado!")


def main():
    """Função principal para executar os testes"""
    
    tester = YakeRegressionTester()
    
    print("Escolha uma opção:")
    print("1. Executar testes e salvar como baseline")
    print("2. Executar testes de regressão")
    print("3. Comparar com baseline existente")
    
    choice = input("\nEscolha (1/2/3): ").strip()
    
    if choice == "1":
        print("\n🏁 Executando testes baseline...")
        results = tester.run_regression_tests(save_baseline=True)
        tester.generate_detailed_report(results)
        
    elif choice == "2":
        print("\n🧪 Executando testes de regressão...")
        results = tester.run_regression_tests(save_baseline=False)
        tester.generate_detailed_report(results)
        
    elif choice == "3":
        baseline_file = input("Arquivo baseline (ex: baseline_scores_20241001_120000.json): ").strip()
        if baseline_file:
            success = tester.compare_with_baseline(baseline_file)
            if success:
                print("\n🎉 Regressão PASSOU! Scores mantidos.")
            else:
                print("\n❌ Regressão FALHOU! Scores alterados.")
        else:
            print("❌ Nome do arquivo necessário.")
    
    else:
        print("❌ Opção inválida.")


if __name__ == "__main__":
    main()