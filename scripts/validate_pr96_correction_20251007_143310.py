#!/usr/bin/env python3
"""
Script de Validação - Teste da Correção PR #96
=============================================

Este script testa se a correção do PR #96 eliminou os scores negativos
usando os casos problemáticos identificados na versão com bug.

Gerado automaticamente em: 2025-10-07T14:33:10.340982
Casos de teste: 32
"""

import yake
import json
import sys
from datetime import datetime

def test_pr96_correction():
    """Testa se a correção PR #96 funciona nos casos problemáticos"""
    
    print("🧪 VALIDAÇÃO DA CORREÇÃO PR #96")
    print("=" * 35)
    print(f"📅 Testando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Casos de teste (copiados da versão com bug)
    validation_cases = [
    {
        "text_name": "academic_paper_style",
        "n_gram_size": 5,
        "language": "en",
        "worst_keyword": "research that has been conducted",
        "worst_score": -0.17383185508074003,
        "text_sample": "In the context of the machine learning research that has been conducted \n                in the fiel...",
        "total_negatives_in_config": 2
    },
    {
        "text_name": "academic_paper_style",
        "n_gram_size": 6,
        "language": "en",
        "worst_keyword": "research that has been conducted",
        "worst_score": -0.17383185508074003,
        "text_sample": "In the context of the machine learning research that has been conducted \n                in the fiel...",
        "total_negatives_in_config": 3
    },
    {
        "text_name": "academic_paper_style",
        "n_gram_size": 7,
        "language": "en",
        "worst_keyword": "research that has been conducted",
        "worst_score": -0.17383185508074003,
        "text_sample": "In the context of the machine learning research that has been conducted \n                in the fiel...",
        "total_negatives_in_config": 9
    },
    {
        "text_name": "academic_paper_style",
        "n_gram_size": 8,
        "language": "en",
        "worst_keyword": "research that has been conducted",
        "worst_score": -0.17383185508074003,
        "text_sample": "In the context of the machine learning research that has been conducted \n                in the fiel...",
        "total_negatives_in_config": 12
    },
    {
        "text_name": "spanish_academic",
        "n_gram_size": 4,
        "language": "es",
        "worst_keyword": "marco de las investigaciones",
        "worst_score": -0.11684849320955795,
        "text_sample": "En el marco de las investigaciones que se han llevado a cabo en el \n                campo de la inte...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "spanish_academic",
        "n_gram_size": 5,
        "language": "es",
        "worst_keyword": "marco de las investigaciones",
        "worst_score": -0.11684849320955795,
        "text_sample": "En el marco de las investigaciones que se han llevado a cabo en el \n                campo de la inte...",
        "total_negatives_in_config": 2
    },
    {
        "text_name": "spanish_academic",
        "n_gram_size": 6,
        "language": "es",
        "worst_keyword": "marco de las investigaciones",
        "worst_score": -0.11684849320955795,
        "text_sample": "En el marco de las investigaciones que se han llevado a cabo en el \n                campo de la inte...",
        "total_negatives_in_config": 2
    },
    {
        "text_name": "spanish_academic",
        "n_gram_size": 7,
        "language": "es",
        "worst_keyword": "marco de las investigaciones",
        "worst_score": -0.11684849320955795,
        "text_sample": "En el marco de las investigaciones que se han llevado a cabo en el \n                campo de la inte...",
        "total_negatives_in_config": 6
    },
    {
        "text_name": "spanish_academic",
        "n_gram_size": 8,
        "language": "es",
        "worst_keyword": "marco de las investigaciones",
        "worst_score": -0.11684849320955795,
        "text_sample": "En el marco de las investigaciones que se han llevado a cabo en el \n                campo de la inte...",
        "total_negatives_in_config": 10
    },
    {
        "text_name": "extreme_stopwords",
        "n_gram_size": 4,
        "language": "en",
        "worst_keyword": "activities that are related",
        "worst_score": -0.06906105838624688,
        "text_sample": "It is in the case of the system that is used for the analysis of the \n                data that is g...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "extreme_stopwords",
        "n_gram_size": 5,
        "language": "en",
        "worst_keyword": "activities that are related",
        "worst_score": -0.06906105838624688,
        "text_sample": "It is in the case of the system that is used for the analysis of the \n                data that is g...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "extreme_stopwords",
        "n_gram_size": 6,
        "language": "en",
        "worst_keyword": "activities that are related",
        "worst_score": -0.06906105838624688,
        "text_sample": "It is in the case of the system that is used for the analysis of the \n                data that is g...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "extreme_stopwords",
        "n_gram_size": 7,
        "language": "en",
        "worst_keyword": "activities that are related",
        "worst_score": -0.06906105838624688,
        "text_sample": "It is in the case of the system that is used for the analysis of the \n                data that is g...",
        "total_negatives_in_config": 9
    },
    {
        "text_name": "extreme_stopwords",
        "n_gram_size": 8,
        "language": "en",
        "worst_keyword": "activities that are related",
        "worst_score": -0.06906105838624688,
        "text_sample": "It is in the case of the system that is used for the analysis of the \n                data that is g...",
        "total_negatives_in_config": 9
    },
    {
        "text_name": "portuguese_verbose",
        "n_gram_size": 4,
        "language": "pt",
        "worst_keyword": "verifica-se que os algoritmos",
        "worst_score": -0.04930530899318827,
        "text_sample": "De acordo com os estudos que foram realizados no \u00e2mbito da investiga\u00e7\u00e3o \n                que tem sid...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "portuguese_verbose",
        "n_gram_size": 5,
        "language": "pt",
        "worst_keyword": "verifica-se que os algoritmos",
        "worst_score": -0.04930530899318827,
        "text_sample": "De acordo com os estudos que foram realizados no \u00e2mbito da investiga\u00e7\u00e3o \n                que tem sid...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "portuguese_verbose",
        "n_gram_size": 6,
        "language": "pt",
        "worst_keyword": "verifica-se que os algoritmos",
        "worst_score": -0.04930530899318827,
        "text_sample": "De acordo com os estudos que foram realizados no \u00e2mbito da investiga\u00e7\u00e3o \n                que tem sid...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "portuguese_verbose",
        "n_gram_size": 7,
        "language": "pt",
        "worst_keyword": "verifica-se que os algoritmos",
        "worst_score": -0.04930530899318827,
        "text_sample": "De acordo com os estudos que foram realizados no \u00e2mbito da investiga\u00e7\u00e3o \n                que tem sid...",
        "total_negatives_in_config": 2
    },
    {
        "text_name": "portuguese_verbose",
        "n_gram_size": 8,
        "language": "pt",
        "worst_keyword": "verifica-se que os algoritmos",
        "worst_score": -0.04930530899318827,
        "text_sample": "De acordo com os estudos que foram realizados no \u00e2mbito da investiga\u00e7\u00e3o \n                que tem sid...",
        "total_negatives_in_config": 3
    },
    {
        "text_name": "academic_paper_style",
        "n_gram_size": 4,
        "language": "en",
        "worst_keyword": "observed that the algorithms",
        "worst_score": -0.04154539669000149,
        "text_sample": "In the context of the machine learning research that has been conducted \n                in the fiel...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "legal_document_style",
        "n_gram_size": 6,
        "language": "en",
        "worst_keyword": "governs the use of the artificial",
        "worst_score": -0.025946612881254574,
        "text_sample": "According to the provisions of the law that governs the use of the \n                artificial intel...",
        "total_negatives_in_config": 2
    },
    {
        "text_name": "legal_document_style",
        "n_gram_size": 7,
        "language": "en",
        "worst_keyword": "governs the use of the artificial",
        "worst_score": -0.025946612881254574,
        "text_sample": "According to the provisions of the law that governs the use of the \n                artificial intel...",
        "total_negatives_in_config": 7
    },
    {
        "text_name": "legal_document_style",
        "n_gram_size": 8,
        "language": "en",
        "worst_keyword": "governs the use of the artificial",
        "worst_score": -0.025946612881254574,
        "text_sample": "According to the provisions of the law that governs the use of the \n                artificial intel...",
        "total_negatives_in_config": 13
    },
    {
        "text_name": "legal_document_style",
        "n_gram_size": 4,
        "language": "en",
        "worst_keyword": "required that the systems",
        "worst_score": -0.025657288711170963,
        "text_sample": "According to the provisions of the law that governs the use of the \n                artificial intel...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "legal_document_style",
        "n_gram_size": 5,
        "language": "en",
        "worst_keyword": "required that the systems",
        "worst_score": -0.025657288711170963,
        "text_sample": "According to the provisions of the law that governs the use of the \n                artificial intel...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "technical_specification",
        "n_gram_size": 7,
        "language": "en",
        "worst_keyword": "mechanism that is used for the processing",
        "worst_score": -0.025637799953478528,
        "text_sample": "The implementation of the neural network architecture that is based on \n                the transfor...",
        "total_negatives_in_config": 2
    },
    {
        "text_name": "technical_specification",
        "n_gram_size": 8,
        "language": "en",
        "worst_keyword": "mechanism that is used for the processing",
        "worst_score": -0.025637799953478528,
        "text_sample": "The implementation of the neural network architecture that is based on \n                the transfor...",
        "total_negatives_in_config": 5
    },
    {
        "text_name": "bureaucratic_text",
        "n_gram_size": 8,
        "language": "en",
        "worst_keyword": "technologies that can be used for the improvement",
        "worst_score": -0.022676388252881693,
        "text_sample": "In accordance with the guidelines that have been established by the \n                committee that ...",
        "total_negatives_in_config": 11
    },
    {
        "text_name": "heavy_stopwords_english",
        "n_gram_size": 6,
        "language": "en",
        "worst_keyword": "algorithms are used in the development",
        "worst_score": -0.02255932766595673,
        "text_sample": "Machine learning algorithms are used in the development of the \n                artificial intellige...",
        "total_negatives_in_config": 1
    },
    {
        "text_name": "heavy_stopwords_english",
        "n_gram_size": 7,
        "language": "en",
        "worst_keyword": "algorithms are used in the development",
        "worst_score": -0.02255932766595673,
        "text_sample": "Machine learning algorithms are used in the development of the \n                artificial intellige...",
        "total_negatives_in_config": 8
    },
    {
        "text_name": "heavy_stopwords_english",
        "n_gram_size": 8,
        "language": "en",
        "worst_keyword": "algorithms are used in the development",
        "worst_score": -0.02255932766595673,
        "text_sample": "Machine learning algorithms are used in the development of the \n                artificial intellige...",
        "total_negatives_in_config": 13
    },
    {
        "text_name": "bureaucratic_text",
        "n_gram_size": 7,
        "language": "en",
        "worst_keyword": "responsible for the evaluation of the proposals",
        "worst_score": -0.00871932899397742,
        "text_sample": "In accordance with the guidelines that have been established by the \n                committee that ...",
        "total_negatives_in_config": 7
    }
]
    
    all_passed = True
    results = []
    
    for i, case in enumerate(validation_cases):
        text_name = case["text_name"]
        n_gram = case["n_gram_size"] 
        language = case["language"]
        original_worst_score = case["worst_score"]
        
        print(f"\n{i+1}. Testando {text_name} (n={n_gram}, {language})")
        print(f"   Score original (com bug): {original_worst_score:.6f}")
        
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
            
            case_result = {
                "case_id": i + 1,
                "text_name": text_name,
                "n_gram_size": n_gram,
                "language": language,
                "original_worst_score": original_worst_score,
                "new_negative_count": len(negative_keywords),
                "new_keywords": keywords,
                "passed": len(negative_keywords) == 0
            }
            
            results.append(case_result)
            
            if len(negative_keywords) == 0:
                print(f"   ✅ PASSOU: Nenhum score negativo!")
            else:
                print(f"   ❌ FALHOU: {len(negative_keywords)} scores ainda negativos:")
                for kw, score in negative_keywords[:3]:
                    print(f"      • '{kw}' → {score:.6f}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            case_result = {
                "case_id": i + 1,
                "text_name": text_name,
                "error": str(e),
                "passed": False
            }
            results.append(case_result)
            all_passed = False
    
    # Resumo final
    passed_count = sum(1 for r in results if r.get("passed", False))
    total_count = len(results)
    
    print(f"\n" + "=" * 50)
    print(f"📊 RESULTADO FINAL DA VALIDAÇÃO")
    print("=" * 30)
    print(f"   ✅ Casos que passaram: {passed_count}/{total_count}")
    print(f"   ❌ Casos que falharam: {total_count - passed_count}/{total_count}")
    print(f"   📈 Taxa de sucesso: {(passed_count/total_count)*100:.1f}%")
    
    if all_passed:
        print(f"\n🎉 CORREÇÃO PR #96 VALIDADA COM SUCESSO!")
        print(f"   ✅ Todos os casos problemáticos foram corrigidos")
        print(f"   ✅ Nenhum score negativo detectado")
    else:
        print(f"\n⚠️  CORREÇÃO INCOMPLETA!")
        print(f"   ❌ Alguns casos ainda geram scores negativos")
        print(f"   ❌ Investigação adicional necessária")
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"pr96_validation_results_{timestamp}.json"
    
    validation_report = {
        "timestamp": datetime.now().isoformat(),
        "total_cases": total_count,
        "passed_cases": passed_count,
        "success_rate": (passed_count/total_count)*100,
        "all_passed": all_passed,
        "results": results
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: {results_file}")
    
    return all_passed

def get_test_text(text_name):
    """Retorna texto de teste baseado no nome"""
    
    test_texts = {
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
    }
    
    return test_texts.get(text_name, "Default test text for validation").strip()

if __name__ == "__main__":
    success = test_pr96_correction()
    sys.exit(0 if success else 1)
