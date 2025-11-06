# pylint: skip-file
"""
Benchmark Simples: Compara versões medindo apenas o tempo de execução
Usa subprocess para isolar completamente cada versão
"""

import subprocess
import json
import time
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

# Test texts
TEST_TEXTS = {
    'small': """Artificial intelligence and machine learning are transforming technology. Deep learning models can process natural language with high accuracy.""",
    
    'medium': """Artificial intelligence and machine learning are revolutionizing the modern technology landscape. Deep learning neural networks have enabled breakthrough advances in computer vision, natural language processing, and speech recognition. These sophisticated algorithms can now analyze vast amounts of data to identify complex patterns and make predictions with remarkable accuracy. Transfer learning techniques allow models trained on one task to be adapted for related problems.""",
    
    'large': """Artificial intelligence and machine learning are transforming the technology landscape in unprecedented ways. Deep learning neural networks, inspired by the structure of the human brain, have enabled remarkable breakthroughs in computer vision, natural language processing, and speech recognition systems. These sophisticated algorithms can analyze massive datasets to identify intricate patterns and generate highly accurate predictions across diverse domains. Convolutional neural networks excel at image classification and object detection tasks, while recurrent architectures process sequential data for language modeling and time series forecasting. Transformer models like GPT and BERT have revolutionized natural language understanding by capturing long-range dependencies in text. Transfer learning techniques enable models pre-trained on large corpora to be fine-tuned for specific applications with limited labeled data, dramatically reducing development time and computational requirements. Reinforcement learning agents learn optimal decision-making strategies through iterative interaction with their environment, mastering complex games and real-world control problems."""
}

def benchmark_version_simple(version_name, text, iterations=20):
    """Benchmark usando método simples"""
    # Salva texto em arquivo temporário
    text_file = BASE_PATH / "scripts" / f"temp_text_{version_name}.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # Cria script de teste
    if version_name == "v0.1.0":
        test_script = f"""
import sys
import time
sys.path.insert(0, r'{BASE_PATH / "yake"}')

# Importar v0.1.0
import yake_1 as yake_module
from yake_1.yake import KeywordExtractor

with open(r'{text_file}', 'r', encoding='utf-8') as f:
    text = f.read()

times = []
for _ in range({iterations}):
    start = time.perf_counter()
    kw = KeywordExtractor(lan="en", n=3, top=20)
    keywords = kw.extract_keywords(text)
    elapsed = (time.perf_counter() - start) * 1000
    times.append(elapsed)

mean_time = sum(times) / len(times)
min_time = min(times)
max_time = max(times)
print(f"{{mean_time:.2f}}|{{min_time:.2f}}|{{max_time:.2f}}|{{len(keywords)}}")
"""
    elif version_name == "v0.6.0":
        test_script = f"""
import sys
import time
sys.path.insert(0, r'{BASE_PATH / "yake" / "yake_0.6.0"}')

from core.yake import KeywordExtractor

with open(r'{text_file}', 'r', encoding='utf-8') as f:
    text = f.read()

times = []
for _ in range({iterations}):
    start = time.perf_counter()
    kw = KeywordExtractor(lan="en", n=3, top=20)
    keywords = kw.extract_keywords(text)
    elapsed = (time.perf_counter() - start) * 1000
    times.append(elapsed)

mean_time = sum(times) / len(times)
min_time = min(times)
max_time = max(times)
print(f"{{mean_time:.2f}}|{{min_time:.2f}}|{{max_time:.2f}}|{{len(keywords)}}")
"""
    else:  # v2.0
        test_script = f"""
import sys
import time
sys.path.insert(0, r'{BASE_PATH}')

from yake import KeywordExtractor

with open(r'{text_file}', 'r', encoding='utf-8') as f:
    text = f.read()

times = []
for _ in range({iterations}):
    start = time.perf_counter()
    kw = KeywordExtractor(lan="en", n=3, top=20)
    keywords = kw.extract_keywords(text)
    elapsed = (time.perf_counter() - start) * 1000
    times.append(elapsed)

mean_time = sum(times) / len(times)
min_time = min(times)
max_time = max(times)
print(f"{{mean_time:.2f}}|{{min_time:.2f}}|{{max_time:.2f}}|{{len(keywords)}}")
"""
    
    # Salva script
    script_file = BASE_PATH / "scripts" / f"temp_bench_{version_name}.py"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    # Executa
    try:
        result = subprocess.run(
            ['python', str(script_file)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            mean, min_t, max_t, kw_count = output.split('|')
            return {
                'mean_time': float(mean),
                'min_time': float(min_t),
                'max_time': float(max_t),
                'keywords_count': int(kw_count)
            }
        else:
            print(f"Erro ao executar {version_name}:")
            print(result.stderr)
            return None
    finally:
        # Cleanup
        if text_file.exists():
            text_file.unlink()
        if script_file.exists():
            script_file.unlink()


def main():
    print("="*80)
    print("  YAKE BENCHMARK: v0.1.0 vs v0.6.0 vs v2.0")
    print("="*80)
    
    all_results = {}
    
    for size_name, text in TEST_TEXTS.items():
        print(f"\n{'='*80}")
        print(f"  {size_name.upper()} ({len(text.split())} palavras)")
        print(f"{'='*80}\n")
        
        results = {}
        
        print(f"  Benchmarking v0.1.0...")
        results['v0.1.0'] = benchmark_version_simple("v0.1.0", text)
        
        print(f"  Benchmarking v0.6.0...")
        results['v0.6.0'] = benchmark_version_simple("v0.6.0", text)
        
        print(f"  Benchmarking v2.0...")
        results['v2.0'] = benchmark_version_simple("v2.0", text)
        
        all_results[size_name] = results
        
        # Print comparison
        if all(v is not None for v in results.values()):
            v010 = results['v0.1.0']
            v060 = results['v0.6.0']
            v20 = results['v2.0']
            
            speedup_010 = v010['mean_time'] / v20['mean_time']
            speedup_060 = v060['mean_time'] / v20['mean_time']
            
            print(f"\n  {'Versão':<12} {'Tempo Médio':<15} {'Min':<12} {'Max':<12}")
            print(f"  {'-'*60}")
            print(f"  {'v0.1.0':<12} {v010['mean_time']:>10.2f}ms  {v010['min_time']:>8.2f}ms  {v010['max_time']:>8.2f}ms")
            print(f"  {'v0.6.0':<12} {v060['mean_time']:>10.2f}ms  {v060['min_time']:>8.2f}ms  {v060['max_time']:>8.2f}ms")
            print(f"  {'v2.0':<12} {v20['mean_time']:>10.2f}ms  {v20['min_time']:>8.2f}ms  {v20['max_time']:>8.2f}ms")
            
            print(f"\n  MELHORIAS:")
            print(f"    v0.1.0 → v2.0: {speedup_010:.2f}x mais rápido")
            print(f"    v0.6.0 → v2.0: {speedup_060:.2f}x mais rápido")
    
    # Summary
    print(f"\n\n{'='*80}")
    print("  RESUMO FINAL")
    print(f"{'='*80}\n")
    
    for version in ['v0.1.0', 'v0.6.0', 'v2.0']:
        avg_time = sum(all_results[size][version]['mean_time'] 
                      for size in TEST_TEXTS.keys()) / len(TEST_TEXTS)
        print(f"  {version}: {avg_time:.2f}ms (média)")
    
    avg_v010 = sum(all_results[size]['v0.1.0']['mean_time'] for size in TEST_TEXTS.keys()) / len(TEST_TEXTS)
    avg_v060 = sum(all_results[size]['v0.6.0']['mean_time'] for size in TEST_TEXTS.keys()) / len(TEST_TEXTS)
    avg_v20 = sum(all_results[size]['v2.0']['mean_time'] for size in TEST_TEXTS.keys()) / len(TEST_TEXTS)
    
    print(f"\n  SPEEDUP MÉDIO:")
    print(f"    v2.0 é {avg_v010/avg_v20:.2f}x mais rápido que v0.1.0")
    print(f"    v2.0 é {avg_v060/avg_v20:.2f}x mais rápido que v0.6.0")
    print(f"\n{'='*80}\n")
    
    # Save results
    output_file = BASE_PATH / "scripts" / "benchmark_results_complete.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"📊 Resultados salvos em: {output_file}")
    
    return all_results


if __name__ == "__main__":
    main()
