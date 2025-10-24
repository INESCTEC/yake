#!/usr/bin/env python3
"""
🔧 VERIFICADOR DA CORREÇÃO DO BUG DE SCORES NEGATIVOS
===================================================
Script para verificar se a correção PR #96 foi aplicada com sucesso
e se todos os casos anteriormente problemáticos foram resolvidos.
"""

import json
import os
import sys
from datetime import datetime
import yake

class BugFixVerifier:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'version_info': 'VERSÃO CORRIGIDA (com otimizações)',
            'total_cases_tested': 0,
            'negative_scores_found': 0,
            'fixed_cases': 0,
            'test_results': {},
            'summary': {}
        }
        
    def load_original_cases(self):
        """Carrega os casos problemáticos da versão original"""
        json_files = [f for f in os.listdir('.') if f.startswith('negative_scores_examples_') and f.endswith('.json')]
        
        if not json_files:
            print("❌ Nenhum arquivo de casos negativos encontrado!")
            print("   Execute primeiro o collect_negative_examples.py na versão com bug")
            return None
            
        # Pega o arquivo mais recente
        latest_file = sorted(json_files)[-1]
        print(f"📁 Carregando casos de: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_single_case(self, test_name, text, language, n_gram, max_kws=20):
        """Testa um caso específico na versão corrigida"""
        try:
            # Configurar YAKE
            kw_extractor = yake.KeywordExtractor(
                lan=language,
                n=n_gram,
                dedupLim=0.7,
                top=max_kws
            )
            
            # Extrair keywords
            keywords = kw_extractor.extract_keywords(text)
            
            # Analisar resultados
            negative_count = 0
            negative_examples = []
            
            for kw, score in keywords:
                if score < 0:
                    negative_count += 1
                    negative_examples.append({
                        'keyword': kw,
                        'score': score
                    })
            
            return {
                'status': 'SUCCESS',
                'total_keywords': len(keywords),
                'negative_count': negative_count,
                'negative_examples': negative_examples[:5],  # Máximo 5 exemplos
                'is_fixed': negative_count == 0
            }
            
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e),
                'is_fixed': False
            }
    
    def run_verification(self):
        """Executa a verificação completa"""
        print("🔧 VERIFICADOR DA CORREÇÃO DO BUG DE SCORES NEGATIVOS")
        print("=" * 55)
        print(f"📅 Versão: {self.results['version_info']}")
        print("🎯 Objetivo: Verificar se todos os casos negativos foram corrigidos")
        print()
        
        # Carregar casos originais
        original_data = self.load_original_cases()
        if not original_data:
            return
            
        validation_cases = original_data.get('validation_cases', [])
        
        if not validation_cases:
            print("❌ Nenhum caso de validação encontrado nos dados!")
            return
        
        print(f"📋 Testando {len(validation_cases)} casos problemáticos...")
        print()
        
        # Testar cada caso
        for i, case in enumerate(validation_cases, 1):
            test_name = case['test_name']
            config = case['config']
            
            print(f"🔍 Testando caso {i}/{len(validation_cases)}: {test_name}")
            print(f"   📝 Idioma: {config['language']}, n={config['n_gram']}")
            
            result = self.test_single_case(
                test_name,
                config['text'],
                config['language'],
                config['n_gram'],
                config.get('max_kws', 20)
            )
            
            # Armazenar resultado
            case_key = f"{test_name}_n{config['n_gram']}"
            self.results['test_results'][case_key] = {
                'original_negative_count': case['original_negative_count'],
                'original_worst_score': case['worst_negative_score'],
                'current_result': result
            }
            
            # Atualizar contadores
            self.results['total_cases_tested'] += 1
            if result['negative_count'] > 0:
                self.results['negative_scores_found'] += result['negative_count']
                print(f"   ❌ AINDA TEM PROBLEMAS: {result['negative_count']} scores negativos")
                for neg in result['negative_examples']:
                    print(f"      🔸 '{neg['keyword']}' → {neg['score']:.6f}")
            else:
                self.results['fixed_cases'] += 1
                print(f"   ✅ CORRIGIDO: 0 scores negativos (antes: {case['original_negative_count']})")
            
            print()
        
        # Gerar sumário
        self.generate_summary()
        
        # Salvar resultados
        self.save_results()
        
        return self.results
    
    def generate_summary(self):
        """Gera sumário dos resultados"""
        total = self.results['total_cases_tested']
        fixed = self.results['fixed_cases']
        still_negative = self.results['negative_scores_found']
        
        self.results['summary'] = {
            'total_cases_tested': total,
            'cases_fixed': fixed,
            'cases_still_problematic': total - fixed,
            'fix_success_rate': (fixed / total * 100) if total > 0 else 0,
            'total_negative_scores_remaining': still_negative,
            'is_fully_fixed': still_negative == 0
        }
        
        print("=" * 60)
        print("📊 SUMÁRIO DA VERIFICAÇÃO")
        print("=" * 60)
        print(f"📋 Total de casos testados: {total}")
        print(f"✅ Casos corrigidos: {fixed}")
        print(f"❌ Casos ainda problemáticos: {total - fixed}")
        print(f"📈 Taxa de sucesso: {fixed/total*100:.1f}%")
        print(f"🎯 Total de scores negativos restantes: {still_negative}")
        print()
        
        if still_negative == 0:
            print("🎉 PARABÉNS! Todos os casos foram corrigidos!")
            print("✅ A correção PR #96 foi aplicada com sucesso!")
        else:
            print("⚠️  ATENÇÃO: Ainda existem casos com scores negativos!")
            print("🔧 A correção pode não ter sido aplicada corretamente.")
        
        print("=" * 60)
    
    def save_results(self):
        """Salva os resultados em arquivo JSON"""
        filename = f"bug_fix_verification_{self.results['timestamp']}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultados salvos em: {filename}")

def main():
    verifier = BugFixVerifier()
    results = verifier.run_verification()
    
    if results and results['summary']['is_fully_fixed']:
        print("\n🎯 VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        sys.exit(0)
    else:
        print("\n❌ VERIFICAÇÃO DETECTOU PROBLEMAS!")
        sys.exit(1)

if __name__ == "__main__":
    main()