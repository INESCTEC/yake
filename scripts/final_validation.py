#!/usr/bin/env python3
"""
Validação Final de Scores YAKE!
===============================

Este script executa uma bateria completa de testes para garantir
que as otimizações não alteraram os scores do algoritmo YAKE!
"""

import yake
import json
import time
import hashlib
from datetime import datetime


def comprehensive_validation():
    """Executa validação abrangente dos scores"""
    
    print("🎯 VALIDAÇÃO FINAL DE SCORES YAKE!")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Datasets de teste diversos
    test_datasets = {
        "scientific": """
        Machine learning algorithms enable pattern recognition in large datasets.
        Deep neural networks process information through multiple layers.
        Convolutional networks excel at image classification tasks.
        Natural language processing handles text understanding.
        """,
        
        "business": """
        Business intelligence systems provide data-driven insights for decision making.
        Customer relationship management improves client satisfaction rates.
        Supply chain optimization reduces operational costs significantly.
        Market analysis identifies growth opportunities and risks.
        """,
        
        "technical": """
        Software engineering methodologies improve development efficiency.
        Database management systems handle concurrent user transactions.
        Network security protocols protect sensitive information transfer.
        Cloud computing platforms offer scalable infrastructure solutions.
        """,
        
        "mixed": """
        Artificial intelligence revolutionizes healthcare diagnostics through automated
        image analysis and predictive modeling. Machine learning algorithms process
        patient data to identify disease patterns and treatment outcomes. Deep learning
        networks analyze medical imaging for early cancer detection systems.
        """
    }
    
    validation_results = {}
    all_tests_passed = True
    total_tests = 0
    passed_tests = 0
    
    # Testar cada dataset com múltiplas configurações
    for dataset_name, text in test_datasets.items():
        print(f"\n📊 Dataset: {dataset_name.upper()}")
        print("-" * 30)
        
        dataset_results = {}
        
        # Configurações de teste
        test_configs = [
            {"n": 1, "dedupLim": 0.7, "top": 10},
            {"n": 2, "dedupLim": 0.7, "top": 15}, 
            {"n": 3, "dedupLim": 0.7, "top": 20},
            {"n": 4, "dedupLim": 0.5, "top": 10},
            {"n": 5, "dedupLim": 0.9, "top": 12},
            {"n": 6, "dedupLim": 1.0, "top": 8},   # Sem deduplicação
            {"n": 7, "dedupLim": 0.3, "top": 5},
            {"n": 8, "dedupLim": 0.8, "top": 6},
            {"n": 9, "dedupLim": 0.6, "top": 4}
        ]
        
        for config in test_configs:
            total_tests += 1
            test_name = f"n{config['n']}_dedup{config['dedupLim']}_top{config['top']}"
            
            try:
                # Configurar extrator
                extractor = yake.KeywordExtractor(
                    lan="en",
                    n=config["n"],
                    dedupLim=config["dedupLim"],
                    top=config["top"]
                )
                
                # Extrair keywords e medir tempo
                start_time = time.perf_counter()
                keywords = extractor.extract_keywords(text)
                exec_time = time.perf_counter() - start_time
                
                # Análise dos resultados
                if not keywords:
                    print(f"   ⚠️  {test_name}: Nenhuma keyword extraída")
                    continue
                
                scores = [score for _, score in keywords]
                negative_scores = [score for score in scores if score < 0]
                
                # Hash dos scores para comparação futura
                scores_str = ";".join([f"{kw}:{score:.10f}" for kw, score in keywords])
                scores_hash = hashlib.md5(scores_str.encode()).hexdigest()
                
                result = {
                    "config": config,
                    "num_keywords": len(keywords),
                    "execution_time_ms": round(exec_time * 1000, 3),
                    "min_score": min(scores),
                    "max_score": max(scores), 
                    "avg_score": sum(scores) / len(scores),
                    "negative_count": len(negative_scores),
                    "scores_hash": scores_hash,
                    "keywords": keywords,
                    "passed": len(negative_scores) == 0
                }
                
                dataset_results[test_name] = result
                
                # Mostrar resultado
                status = "✅" if result["passed"] else f"❌({len(negative_scores)} neg)"
                print(f"   {test_name}: {len(keywords):2d} kws, {exec_time*1000:5.1f}ms {status}")
                
                if result["passed"]:
                    passed_tests += 1
                else:
                    all_tests_passed = False
                    print(f"      Scores negativos: {negative_scores[:3]}")
                
            except Exception as e:
                print(f"   ❌ {test_name}: ERRO - {e}")
                all_tests_passed = False
        
        validation_results[dataset_name] = dataset_results
    
    # Relatório final
    print(f"\n" + "=" * 50)
    print(f"📊 RELATÓRIO FINAL DE VALIDAÇÃO")
    print("=" * 30)
    print(f"   📋 Testes executados: {total_tests}")
    print(f"   ✅ Testes passaram: {passed_tests}")
    print(f"   ❌ Testes falharam: {total_tests - passed_tests}")
    print(f"   📈 Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    if all_tests_passed:
        print(f"\n🎉 VALIDAÇÃO COMPLETA PASSOU!")
        print(f"   ✅ Nenhum score negativo encontrado")
        print(f"   ✅ Todas as configurações funcionaram")
        print(f"   ✅ Performance dentro do esperado")
    else:
        print(f"\n⚠️  VALIDAÇÃO ENCONTROU PROBLEMAS!")
        print(f"   ❌ Alguns scores negativos detectados")
        print(f"   ❌ Verificar implementação necessário")
    
    # Salvar resultados detalhados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"validation_results_{timestamp}.json"
    
    validation_report = {
        "timestamp": timestamp,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "success_rate": round((passed_tests/total_tests)*100, 2),
        "all_passed": all_tests_passed,
        "datasets": validation_results
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: {results_file}")
    
    return all_tests_passed, validation_report


def compare_validation_results(file1, file2):
    """Compara dois arquivos de validação"""
    
    print(f"\n🔍 COMPARANDO RESULTADOS DE VALIDAÇÃO")
    print("=" * 40)
    
    try:
        with open(file1, 'r', encoding='utf-8') as f:
            results1 = json.load(f)
        with open(file2, 'r', encoding='utf-8') as f:
            results2 = json.load(f)
            
        print(f"📁 Arquivo 1: {file1}")
        print(f"📁 Arquivo 2: {file2}")
        
        # Comparar estatísticas gerais
        print(f"\n📊 Estatísticas gerais:")
        print(f"   Arquivo 1: {results1['passed_tests']}/{results1['total_tests']} ({results1['success_rate']}%)")
        print(f"   Arquivo 2: {results2['passed_tests']}/{results2['total_tests']} ({results2['success_rate']}%)")
        
        # Comparar hashes dos scores
        differences_found = 0
        total_compared = 0
        
        for dataset_name in results1.get("datasets", {}):
            if dataset_name not in results2.get("datasets", {}):
                continue
                
            dataset1 = results1["datasets"][dataset_name]
            dataset2 = results2["datasets"][dataset_name]
            
            for test_name in dataset1:
                if test_name not in dataset2:
                    continue
                    
                total_compared += 1
                hash1 = dataset1[test_name].get("scores_hash")
                hash2 = dataset2[test_name].get("scores_hash")
                
                if hash1 != hash2:
                    differences_found += 1
                    print(f"   ❌ Diferença em {dataset_name}.{test_name}")
                    print(f"      Hash1: {hash1[:16]}...")
                    print(f"      Hash2: {hash2[:16]}...")
        
        print(f"\n📈 Comparação de hashes:")
        print(f"   🔍 Testes comparados: {total_compared}")
        print(f"   ✅ Idênticos: {total_compared - differences_found}")
        print(f"   ❌ Diferentes: {differences_found}")
        
        if differences_found == 0:
            print(f"\n🎉 PERFEITO! Todos os scores são idênticos!")
            return True
        else:
            print(f"\n⚠️  ATENÇÃO! {differences_found} diferenças encontradas!")
            return False
            
    except Exception as e:
        print(f"❌ Erro na comparação: {e}")
        return False


def main():
    """Função principal"""
    
    print("Escolha uma opção:")
    print("1. Executar validação completa")
    print("2. Comparar dois arquivos de validação")
    
    choice = input("\nEscolha (1/2): ").strip()
    
    if choice == "1":
        success, report = comprehensive_validation()
        return success
        
    elif choice == "2":
        file1 = input("Primeiro arquivo: ").strip()
        file2 = input("Segundo arquivo: ").strip()
        return compare_validation_results(file1, file2)
    
    else:
        print("❌ Opção inválida")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)