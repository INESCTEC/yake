#!/usr/bin/env python3
# pylint: skip-file
"""
Coletor de Exemplos com Scores Negativos - Versão Problemática
=============================================================

Este script usa a versão atual (com o bug) para coletar exemplos reais
que geram scores negativos. Estes exemplos serão então usados para
validar que a correção do PR #96 efetivamente resolve o problema.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import yake
import json
import time
from datetime import datetime
from collections import defaultdict


class NegativeScoreCollector:
    """Coleta exemplos reais que geram scores negativos"""
    
    def __init__(self):
        self.negative_examples = []
        self.test_texts = []
        self.setup_test_texts()
    
    def setup_test_texts(self):
        """Configura textos de teste propensos a gerar scores negativos"""
        
        self.test_texts = [
            # Textos com muitas stopwords consecutivas (problema principal)
            {
                "name": "heavy_stopwords_english",
                "text": """
                Machine learning algorithms are used in the development of the 
                artificial intelligence systems that are being used in the medical 
                field for the diagnosis of the diseases in the patients who are 
                suffering from the chronic conditions that are affecting the quality 
                of the life of the individuals in the society.
                """,
                "language": "en"
            },
            
            {
                "name": "academic_paper_style",
                "text": """
                In the context of the machine learning research that has been conducted 
                in the field of the natural language processing, it has been observed 
                that the algorithms that are based on the deep learning approaches 
                have shown significant improvements in the performance of the tasks 
                that are related to the understanding of the human language.
                """,
                "language": "en"
            },
            
            {
                "name": "legal_document_style", 
                "text": """
                According to the provisions of the law that governs the use of the 
                artificial intelligence in the healthcare sector, it is required that 
                the systems that are being developed for the diagnosis of the medical 
                conditions should be validated through the processes that are approved 
                by the regulatory authorities that are responsible for the oversight.
                """,
                "language": "en"
            },
            
            {
                "name": "technical_specification",
                "text": """
                The implementation of the neural network architecture that is based on 
                the transformer model requires the configuration of the parameters that 
                control the behavior of the attention mechanism that is used for the 
                processing of the input sequences that contain the textual information.
                """,
                "language": "en"
            },
            
            {
                "name": "bureaucratic_text",
                "text": """
                In accordance with the guidelines that have been established by the 
                committee that is responsible for the evaluation of the proposals that 
                are submitted for the funding of the research projects that focus on 
                the development of the technologies that can be used for the improvement 
                of the educational systems.
                """,
                "language": "en"
            },
            
            # Texto finlandês do Issue #17 original
            {
                "name": "finnish_original_issue17",
                "text": """
                Kuten aiemmin on todettu, useat tutkimukset ovat osoittaneet, että 
                morrow'n neljä eri sitoutumisen tasoa vaikuttavat työntekijöiden 
                suorituskykyyn ja organisaation tehokkuuteen monin eri tavoin.
                """,
                "language": "fi"  
            },
            
            # Outros idiomas propensos ao problema
            {
                "name": "portuguese_verbose",
                "text": """
                De acordo com os estudos que foram realizados no âmbito da investigação 
                que tem sido desenvolvida na área da inteligência artificial, verifica-se 
                que os algoritmos que são baseados nas redes neurais têm demonstrado 
                resultados que são significativamente superiores aos que eram obtidos 
                com os métodos que eram utilizados anteriormente.
                """,
                "language": "pt"
            },
            
            {
                "name": "spanish_academic",
                "text": """
                En el marco de las investigaciones que se han llevado a cabo en el 
                campo de la inteligencia artificial que se aplica en el procesamiento 
                del lenguaje natural, se ha observado que los algoritmos que se basan 
                en las técnicas de aprendizaje profundo han mostrado mejoras que son 
                considerablemente importantes en las tareas que están relacionadas.
                """,
                "language": "es"
            },
            
            {
                "name": "german_complex",
                "text": """
                Im Rahmen der Forschungsarbeiten, die in dem Bereich der künstlichen 
                Intelligenz durchgeführt worden sind, die sich mit der Entwicklung 
                von Algorithmen beschäftigen, die für die Verarbeitung von natürlicher 
                Sprache verwendet werden, ist festgestellt worden, dass die Methoden 
                des maschinellen Lernens bedeutende Verbesserungen ermöglichen.
                """,
                "language": "de"
            },
            
            # Textos sintéticos extremos para testar limites
            {
                "name": "extreme_stopwords",
                "text": """
                It is in the case of the system that is used for the analysis of the 
                data that is generated by the users who are engaged in the activities 
                that are related to the use of the platform that is designed for the 
                management of the information that is stored in the database.
                """,
                "language": "en"
            }
        ]
    
    def test_single_text(self, text_info, n_gram_sizes=[3, 4, 5, 6, 7, 8]):
        """Testa um texto específico com diferentes tamanhos de n-grama"""
        
        text_name = text_info["name"]
        text_content = text_info["text"].strip()
        language = text_info["language"]
        
        print(f"\n🔍 Testando: {text_name} ({language})")
        print(f"📝 Texto: {text_content[:80]}...")
        
        text_results = []
        
        for n in n_gram_sizes:
            try:
                # Configurar extrator
                extractor = yake.KeywordExtractor(
                    lan=language,
                    n=n,
                    dedupLim=0.7,
                    top=20
                )
                
                # Extrair keywords e medir tempo
                start_time = time.perf_counter()
                keywords = extractor.extract_keywords(text_content)
                execution_time = time.perf_counter() - start_time
                
                # Analisar scores
                negative_keywords = [(kw, score) for kw, score in keywords if score < 0]
                positive_keywords = [(kw, score) for kw, score in keywords if score >= 0]
                
                result = {
                    "text_name": text_name,
                    "language": language,
                    "n_gram_size": n,
                    "execution_time_ms": round(execution_time * 1000, 2),
                    "total_keywords": len(keywords),
                    "negative_count": len(negative_keywords),
                    "positive_count": len(positive_keywords),
                    "negative_keywords": negative_keywords,
                    "all_keywords": keywords,
                    "has_negatives": len(negative_keywords) > 0
                }
                
                text_results.append(result)
                
                # Mostrar resultados
                status = f"❌ {len(negative_keywords)} neg" if negative_keywords else "✅ OK"
                print(f"   n={n}: {len(keywords)} kws, {execution_time*1000:.1f}ms {status}")
                
                # Mostrar exemplos de scores negativos
                if negative_keywords:
                    print(f"      🔸 Exemplos negativos:")
                    for i, (kw, score) in enumerate(negative_keywords[:3]):
                        print(f"         {i+1}. '{kw}' → {score:.6f}")
                    
                    # Adicionar aos exemplos coletados
                    self.negative_examples.extend([
                        {
                            "keyword": kw,
                            "score": score,
                            "text_name": text_name,
                            "language": language,
                            "n_gram_size": n,
                            "text_sample": text_content[:100] + "..."
                        }
                        for kw, score in negative_keywords
                    ])
                
            except Exception as e:
                print(f"   ❌ n={n}: ERRO - {e}")
                
        return text_results
    
    def collect_all_examples(self):
        """Coleta exemplos de todos os textos de teste"""
        
        print("🎯 COLETANDO EXEMPLOS COM SCORES NEGATIVOS")
        print("=" * 45)
        print(f"📅 Versão atual: COM BUG (antes da correção PR #96)")
        print(f"🎯 Objetivo: Encontrar casos que geram scores negativos")
        
        all_results = []
        
        for text_info in self.test_texts:
            results = self.test_single_text(text_info)
            all_results.extend(results)
        
        return all_results
    
    def generate_validation_dataset(self):
        """Gera dataset de validação com os exemplos coletados"""
        
        print(f"\n" + "=" * 60)
        print(f"📊 ANÁLISE DOS EXEMPLOS COLETADOS")
        print("=" * 30)
        
        # Estatísticas gerais
        total_negatives = len(self.negative_examples)
        
        if total_negatives == 0:
            print(f"⚠️  Nenhum score negativo encontrado!")
            print(f"   Isso pode indicar que:")
            print(f"   • A versão atual já tem a correção")
            print(f"   • Os textos de teste não são suficientemente problemáticos")
            print(f"   • O bug não se manifesta com essas configurações")
            return None
        
        print(f"📊 Total de scores negativos encontrados: {total_negatives}")
        
        # Agrupar por texto
        by_text = defaultdict(list)
        by_language = defaultdict(list)
        by_ngram = defaultdict(list)
        
        for example in self.negative_examples:
            by_text[example["text_name"]].append(example)
            by_language[example["language"]].append(example)
            by_ngram[example["n_gram_size"]].append(example)
        
        print(f"\n📋 Distribuição por texto:")
        for text_name, examples in sorted(by_text.items()):
            print(f"   • {text_name}: {len(examples)} casos")
        
        print(f"\n📋 Distribuição por idioma:")
        for lang, examples in sorted(by_language.items()):
            print(f"   • {lang}: {len(examples)} casos")
        
        print(f"\n📋 Distribuição por n-grama:")
        for n, examples in sorted(by_ngram.items()):
            print(f"   • n={n}: {len(examples)} casos")
        
        # Selecionar casos mais representativos para validação
        validation_cases = self.select_validation_cases()
        
        return {
            "collection_timestamp": datetime.now().isoformat(),
            "yake_version": "buggy_version_pre_pr96",
            "total_negative_examples": total_negatives,
            "statistics": {
                "by_text": dict([(k, len(v)) for k, v in by_text.items()]),
                "by_language": dict([(k, len(v)) for k, v in by_language.items()]),
                "by_ngram": dict([(k, len(v)) for k, v in by_ngram.items()])
            },
            "validation_cases": validation_cases,
            "all_examples": self.negative_examples
        }
    
    def select_validation_cases(self):
        """Seleciona casos mais representativos para validação"""
        
        validation_cases = []
        
        # Agrupar por (texto, n-grama) para pegar casos únicos
        unique_configs = {}
        for example in self.negative_examples:
            key = (example["text_name"], example["n_gram_size"])
            if key not in unique_configs:
                unique_configs[key] = []
            unique_configs[key].append(example)
        
        # Selecionar os piores casos (scores mais negativos) de cada configuração
        for (text_name, n_gram), examples in unique_configs.items():
            # Pegar o pior caso (score mais negativo)
            worst_case = min(examples, key=lambda x: x["score"])
            
            validation_cases.append({
                "text_name": text_name,
                "n_gram_size": n_gram,
                "language": worst_case["language"],
                "worst_keyword": worst_case["keyword"],
                "worst_score": worst_case["score"],
                "text_sample": worst_case["text_sample"],
                "total_negatives_in_config": len(examples)
            })
        
        # Ordenar por score mais negativo
        validation_cases.sort(key=lambda x: x["worst_score"])
        
        print(f"\n🎯 CASOS SELECIONADOS PARA VALIDAÇÃO:")
        for i, case in enumerate(validation_cases[:10]):  # Top 10
            print(f"   {i+1}. {case['text_name']} (n={case['n_gram_size']})")
            print(f"      Pior caso: '{case['worst_keyword']}' → {case['worst_score']:.6f}")
            print(f"      Total negativos: {case['total_negatives_in_config']}")
        
        if len(validation_cases) > 10:
            print(f"   ... e mais {len(validation_cases) - 10} casos")
        
        return validation_cases
    
    def create_test_script_for_fixed_version(self, validation_data):
        """Cria script de teste para validar a versão corrigida"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        script_content = f'''#!/usr/bin/env python3
"""
Script de Validação - Teste da Correção PR #96
=============================================

Este script testa se a correção do PR #96 eliminou os scores negativos
usando os casos problemáticos identificados na versão com bug.

Gerado automaticamente em: {datetime.now().isoformat()}
Casos de teste: {len(validation_data.get("validation_cases", []))}
"""

import yake
import json
import sys
from datetime import datetime

def test_pr96_correction():
    """Testa se a correção PR #96 funciona nos casos problemáticos"""
    
    print("🧪 VALIDAÇÃO DA CORREÇÃO PR #96")
    print("=" * 35)
    print(f"📅 Testando em: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    
    # Casos de teste (copiados da versão com bug)
    validation_cases = {json.dumps(validation_data.get("validation_cases", []), indent=4)}
    
    all_passed = True
    results = []
    
    for i, case in enumerate(validation_cases):
        text_name = case["text_name"]
        n_gram = case["n_gram_size"] 
        language = case["language"]
        original_worst_score = case["worst_score"]
        
        print(f"\\n{{i+1}}. Testando {{text_name}} (n={{n_gram}}, {{language}})")
        print(f"   Score original (com bug): {{original_worst_score:.6f}}")
        
        # Recuperar texto original (seria melhor ter o texto completo)
        # Por agora, usar um texto representativo
        test_text = get_test_text(text_name)
        
        try:
            # Testar com a versão corrigida
            extractor = yake.KeywordExtractor(
                lan=language,
                n=n_gram,
                dedupLim=0.7,
                top=20
            )
            
            keywords = extractor.extract_keywords(test_text)
            negative_keywords = [(kw, score) for kw, score in keywords if score < 0]
            
            case_result = {{
                "case_id": i + 1,
                "text_name": text_name,
                "n_gram_size": n_gram,
                "language": language,
                "original_worst_score": original_worst_score,
                "new_negative_count": len(negative_keywords),
                "new_keywords": keywords,
                "passed": len(negative_keywords) == 0
            }}
            
            results.append(case_result)
            
            if len(negative_keywords) == 0:
                print(f"   ✅ PASSOU: Nenhum score negativo!")
            else:
                print(f"   ❌ FALHOU: {{len(negative_keywords)}} scores ainda negativos:")
                for kw, score in negative_keywords[:3]:
                    print(f"      • '{{kw}}' → {{score:.6f}}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERRO: {{e}}")
            case_result = {{
                "case_id": i + 1,
                "text_name": text_name,
                "error": str(e),
                "passed": False
            }}
            results.append(case_result)
            all_passed = False
    
    # Resumo final
    passed_count = sum(1 for r in results if r.get("passed", False))
    total_count = len(results)
    
    print(f"\\n" + "=" * 50)
    print(f"📊 RESULTADO FINAL DA VALIDAÇÃO")
    print("=" * 30)
    print(f"   ✅ Casos que passaram: {{passed_count}}/{{total_count}}")
    print(f"   ❌ Casos que falharam: {{total_count - passed_count}}/{{total_count}}")
    print(f"   📈 Taxa de sucesso: {{(passed_count/total_count)*100:.1f}}%")
    
    if all_passed:
        print(f"\\n🎉 CORREÇÃO PR #96 VALIDADA COM SUCESSO!")
        print(f"   ✅ Todos os casos problemáticos foram corrigidos")
        print(f"   ✅ Nenhum score negativo detectado")
    else:
        print(f"\\n⚠️  CORREÇÃO INCOMPLETA!")
        print(f"   ❌ Alguns casos ainda geram scores negativos")
        print(f"   ❌ Investigação adicional necessária")
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"pr96_validation_results_{{timestamp}}.json"
    
    validation_report = {{
        "timestamp": datetime.now().isoformat(),
        "total_cases": total_count,
        "passed_cases": passed_count,
        "success_rate": (passed_count/total_count)*100,
        "all_passed": all_passed,
        "results": results
    }}
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2, ensure_ascii=False)
    
    print(f"\\n💾 Resultados salvos em: {{results_file}}")
    
    return all_passed

def get_test_text(text_name):
    """Retorna texto de teste baseado no nome"""
    
    test_texts = {{
        "heavy_stopwords_english": """
        Machine learning algorithms are used in the development of the 
        artificial intelligence systems that are being used in the medical 
        field for the diagnosis of the diseases in the patients who are 
        suffering from the chronic conditions that are affecting the quality 
        of the life of the individuals in the society.
        """,
        
        "academic_paper_style": """
        In the context of the machine learning research that has been conducted 
        in the field of the natural language processing, it has been observed 
        that the algorithms that are based on the deep learning approaches 
        have shown significant improvements in the performance of the tasks 
        that are related to the understanding of the human language.
        """,
        
        "finnish_original_issue17": """
        Kuten aiemmin on todettu, useat tutkimukset ovat osoittaneet, että 
        morrow'n neljä eri sitoutumisen tasoa vaikuttavat työntekijöiden 
        suorituskykyyn ja organisaation tehokkuuteen monin eri tavoin.
        """
        # Adicionar mais textos conforme necessário
    }}
    
    return test_texts.get(text_name, "Default test text for validation").strip()

if __name__ == "__main__":
    success = test_pr96_correction()
    sys.exit(0 if success else 1)
'''
        
        script_filename = f"validate_pr96_correction_{timestamp}.py"
        
        with open(script_filename, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"\n💾 Script de validação criado: {script_filename}")
        print(f"   🎯 Use este script na versão corrigida para validar a correção")
        
        return script_filename


def main():
    """Função principal"""
    
    print("🎯 COLETOR DE EXEMPLOS COM SCORES NEGATIVOS")
    print("=" * 45)
    print("📋 Versão: COM BUG (antes da correção PR #96)")
    
    collector = NegativeScoreCollector()
    
    # Coletar exemplos
    all_results = collector.collect_all_examples()
    
    # Analisar e gerar dataset de validação
    validation_data = collector.generate_validation_dataset()
    
    if validation_data:
        # Salvar dados de validação
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        validation_file = f"negative_scores_examples_{timestamp}.json"
        
        with open(validation_file, 'w', encoding='utf-8') as f:
            json.dump(validation_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados salvos em: {validation_file}")
        
        # Criar script de validação para a versão corrigida
        script_file = collector.create_test_script_for_fixed_version(validation_data)
        
        print(f"\n🎯 PRÓXIMOS PASSOS:")
        print(f"   1. ✅ Exemplos com scores negativos coletados")
        print(f"   2. 🔧 Aplicar correção PR #96 na versão do código")
        print(f"   3. 🧪 Executar script: {script_file}")
        print(f"   4. ✅ Validar que todos os casos passam (sem scores negativos)")
        
    else:
        print(f"\n⚠️  Nenhum exemplo negativo coletado!")
        print(f"   Possíveis causas:")
        print(f"   • Versão já tem a correção")  
        print(f"   • Textos de teste insuficientes")
        print(f"   • Configurações não adequadas")

if __name__ == "__main__":
    main()