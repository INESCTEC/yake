#!/usr/bin/env python3
# pylint: skip-file
"""
🧪 TESTE DE ESCALABILIDADE: YAKE 2.0 vs ARQUIVOS GRANDES
========================================================
Testa a capacidade da versão atual (otimizada) do YAKE para processar
arquivos grandes, comparando com o benchmark da versão 0.6.0.
"""

import yake
import time
import psutil
import os
import sys
from datetime import datetime
from typing import Dict, Any

class YakeScalabilityTester:
    """Testa a escalabilidade do YAKE atual com arquivos grandes"""
    
    def __init__(self):
        self.results = {
            'version_info': 'YAKE 2.0 (versão otimizada atual)',
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'system_info': self.get_system_info(),
            'tests': []
        }
    
    def get_system_info(self):
        """Coleta informações do sistema"""
        return {
            'cpu': f"{psutil.cpu_count()} cores",
            'ram_total_gb': f"{psutil.virtual_memory().total / (1024**3):.1f}GB",
            'ram_available_gb': f"{psutil.virtual_memory().available / (1024**3):.1f}GB",
            'python_version': sys.version.split()[0]
        }
    
    def generate_large_text(self, target_size_mb: int, filename: str = None) -> str:
        """Gera texto sintético para simular arquivo grande"""
        if filename is None:
            filename = f"test_text_{target_size_mb}mb.txt"
        
        print(f"📝 Gerando texto sintético de {target_size_mb}MB...")
        
        # Template de abstract científico
        abstract_template = """
        Machine learning algorithms are increasingly being used in the development of artificial intelligence systems that can process and analyze large amounts of data. These systems have shown remarkable performance in various domains including natural language processing, computer vision, and speech recognition. The implementation of deep learning neural networks has revolutionized the field by enabling automated feature extraction and pattern recognition capabilities. Researchers have demonstrated that convolutional neural networks can achieve state-of-the-art results in image classification tasks, while recurrent neural networks excel in sequential data processing. The optimization of these models requires careful tuning of hyperparameters and extensive training on large datasets. Recent advances in transformer architectures have further improved the performance of language models, enabling more sophisticated text generation and understanding capabilities. The integration of attention mechanisms allows these models to focus on relevant parts of the input sequence, leading to better contextual understanding. Applications of these technologies span across multiple industries including healthcare, finance, automotive, and telecommunications. The ethical implications of artificial intelligence deployment require careful consideration of bias, fairness, and transparency in algorithmic decision-making processes.
        """
        
        # Calcular quantos abstracts precisamos
        template_size = len(abstract_template.encode('utf-8'))
        target_size_bytes = target_size_mb * 1024 * 1024
        num_abstracts = target_size_bytes // template_size + 1
        
        print(f"   📊 Gerando {num_abstracts:,} abstracts para atingir {target_size_mb}MB...")
        
        # Gerar texto
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(num_abstracts):
                # Adicionar variação nos abstracts
                variation = f" Abstract {i+1}: "
                f.write(variation + abstract_template)
                
                if (i + 1) % 1000 == 0:
                    current_size_mb = os.path.getsize(filename) / (1024 * 1024)
                    print(f"\r   ⏳ Progresso: {i+1:,} abstracts, {current_size_mb:.1f}MB", end="")
                    
                    if current_size_mb >= target_size_mb:
                        break
        
        final_size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"\n   ✅ Arquivo gerado: {filename} ({final_size_mb:.1f}MB)")
        return filename
    
    def test_yake_performance(self, text_file: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Testa performance do YAKE em arquivo específico"""
        file_size_mb = os.path.getsize(text_file) / (1024 * 1024)
        
        print(f"🧪 Testando YAKE com arquivo de {file_size_mb:.1f}MB...")
        print(f"   📋 Configuração: {config}")
        
        # Ler arquivo
        print("   📖 Carregando texto...")
        start_time = time.time()
        
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': f"Erro ao ler arquivo: {e}",
                'file_size_mb': file_size_mb
            }
        
        load_time = time.time() - start_time
        print(f"   ✅ Texto carregado em {load_time:.2f}s ({len(text):,} caracteres)")
        
        # Monitorar memória antes
        ram_before = psutil.virtual_memory()
        
        # Executar YAKE
        print("   🔍 Executando extração de keywords...")
        start_time = time.time()
        
        try:
            kw_extractor = yake.KeywordExtractor(**config)
            keywords = kw_extractor.extract_keywords(text)
            
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': f"Erro no YAKE: {e}",
                'file_size_mb': file_size_mb,
                'load_time_seconds': load_time
            }
        
        extraction_time = time.time() - start_time
        
        # Monitorar memória depois
        ram_after = psutil.virtual_memory()
        
        print(f"   ✅ Extração concluída em {extraction_time:.2f}s")
        print(f"   📊 Keywords extraídas: {len(keywords)}")
        
        return {
            'status': 'SUCCESS',
            'file_size_mb': file_size_mb,
            'text_length': len(text),
            'load_time_seconds': load_time,
            'extraction_time_seconds': extraction_time,
            'total_time_seconds': load_time + extraction_time,
            'keywords_extracted': len(keywords),
            'ram_usage_before_mb': ram_before.used / (1024**2),
            'ram_usage_after_mb': ram_after.used / (1024**2),
            'ram_delta_mb': (ram_after.used - ram_before.used) / (1024**2),
            'sample_keywords': keywords[:10] if keywords else []
        }
    
    def run_scalability_tests(self):
        """Executa bateria de testes de escalabilidade"""
        print("🧪 TESTE DE ESCALABILIDADE: YAKE 2.0")
        print("=" * 50)
        print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💻 Sistema: {self.results['system_info']}")
        print()
        
        # Configuração de teste (similar ao benchmark da discussão)
        test_config = {
            'lan': 'en',
            'n': 3,
            'dedupLim': 0.7,
            'top': 200,  # Como mencionado: "200 keywords"
            'features': None
        }
        
        # Tamanhos de teste progressivos
        test_sizes_mb = [1, 5, 10, 25, 48.5]  # Incluindo o benchmark de 48.5MB
        
        for size_mb in test_sizes_mb:
            print(f"\n{'='*60}")
            print(f"🎯 TESTE: Arquivo de {size_mb}MB")
            print(f"{'='*60}")
            
            try:
                # Gerar arquivo de teste
                text_file = self.generate_large_text(int(size_mb))
                
                # Testar YAKE
                result = self.test_yake_performance(text_file, test_config)
                result['test_size_mb'] = size_mb
                result['config'] = test_config.copy()
                
                self.results['tests'].append(result)
                
                # Mostrar resultado
                if result['status'] == 'SUCCESS':
                    print(f"✅ SUCESSO:")
                    print(f"   ⏱️  Tempo total: {result['total_time_seconds']:.2f}s")
                    print(f"   🔍 Keywords: {result['keywords_extracted']}")
                    print(f"   💾 RAM usada: {result['ram_delta_mb']:.1f}MB")
                    
                    # Comparar com benchmark
                    if size_mb == 48.5:
                        benchmark_time_minutes = 4.4
                        our_time_minutes = result['total_time_seconds'] / 60
                        improvement = ((benchmark_time_minutes - our_time_minutes) / benchmark_time_minutes) * 100
                        
                        print(f"\n🏆 COMPARAÇÃO COM BENCHMARK (YAKE 0.6.0):")
                        print(f"   📊 Benchmark: 4.4 minutos (30k abstracts, 48.5MB)")
                        print(f"   🚀 YAKE 2.0: {our_time_minutes:.2f} minutos")
                        
                        if improvement > 0:
                            print(f"   ⚡ Melhoria: {improvement:.1f}% mais rápido!")
                        else:
                            print(f"   📈 Diferença: {abs(improvement):.1f}% mais lento")
                else:
                    print(f"❌ ERRO: {result['error']}")
                
                # Limpeza
                try:
                    os.remove(text_file)
                except:
                    pass
                    
            except Exception as e:
                print(f"❌ ERRO CRÍTICO no teste {size_mb}MB: {e}")
                self.results['tests'].append({
                    'status': 'CRITICAL_ERROR',
                    'test_size_mb': size_mb,
                    'error': str(e)
                })
        
        self.generate_summary()
        return self.results
    
    def generate_summary(self):
        """Gera sumário dos resultados"""
        print(f"\n{'='*70}")
        print("📊 SUMÁRIO DOS TESTES DE ESCALABILIDADE")
        print(f"{'='*70}")
        
        successful_tests = [t for t in self.results['tests'] if t['status'] == 'SUCCESS']
        
        if not successful_tests:
            print("❌ Nenhum teste foi bem-sucedido!")
            return
        
        print(f"✅ Testes bem-sucedidos: {len(successful_tests)}/{len(self.results['tests'])}")
        print()
        
        # Tabela de resultados
        print("📋 RESULTADOS POR TAMANHO:")
        print("┌" + "─"*10 + "┬" + "─"*15 + "┬" + "─"*15 + "┬" + "─"*12 + "┐")
        print("│ Tamanho  │ Tempo (min)   │ Keywords      │ RAM (MB)   │")
        print("├" + "─"*10 + "┼" + "─"*15 + "┼" + "─"*15 + "┼" + "─"*12 + "┤")
        
        for test in successful_tests:
            size = f"{test['test_size_mb']:.1f}MB"
            time_min = f"{test['total_time_seconds']/60:.2f}min"
            keywords = f"{test['keywords_extracted']}"
            ram = f"{test['ram_delta_mb']:.1f}MB"
            
            print(f"│ {size:<8} │ {time_min:<13} │ {keywords:<13} │ {ram:<10} │")
        
        print("└" + "─"*10 + "┴" + "─"*15 + "┴" + "─"*15 + "┴" + "─"*12 + "┘")
        
        # Análise de escalabilidade
        largest_test = max(successful_tests, key=lambda x: x['test_size_mb'])
        
        print(f"\n🏆 MAIOR ARQUIVO PROCESSADO:")
        print(f"   📏 Tamanho: {largest_test['test_size_mb']}MB")
        print(f"   ⏱️  Tempo: {largest_test['total_time_seconds']/60:.2f} minutos")
        print(f"   🎯 Status: {'✅ Sucesso' if largest_test['test_size_mb'] >= 48.5 else '⚠️ Limitado'}")

def main():
    """Função principal"""
    tester = YakeScalabilityTester()
    
    try:
        results = tester.run_scalability_tests()
        
        # Salvar resultados
        import json
        filename = f"yake_scalability_test_{results['timestamp']}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados salvos em: {filename}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)