#!/usr/bin/env python3
# pylint: skip-file
"""
Executa benchmarks REAIS das 3 versões usando subprocess
para garantir completo isolamento
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

def run_isolated_benchmark(script_name: str, version: str) -> dict:
    """Executa benchmark em subprocess isolado"""
    script_path = Path(__file__).parent / script_name
    
    print(f"\n🔬 Executando benchmark {version}...")
    print(f"   Script: {script_name}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            print(f"   ❌ Erro: {result.stderr}")
            return {"error": result.stderr, "version": version}
        
        data = json.loads(result.stdout)
        print(f"   ✅ Sucesso! Tempo médio: {data.get('overall_avg', 0):.2f}ms")
        return data
        
    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout!")
        return {"error": "Timeout", "version": version}
    except json.JSONDecodeError as e:
        print(f"   ❌ Erro ao parsear JSON: {e}")
        print(f"   Output: {result.stdout}")
        return {"error": f"JSON decode error: {e}", "version": version}
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return {"error": str(e), "version": version}

def main():
    print("=" * 70)
    print("🚀 YAKE - BENCHMARK REAL DAS 3 VERSÕES")
    print("=" * 70)
    print("\nExecutando benchmarks isolados via subprocess...")
    
    # Executar cada versão em subprocess separado
    v010_data = run_isolated_benchmark("benchmark_v010_isolated.py", "0.1.0")
    v060_data = run_isolated_benchmark("benchmark_v060_isolated.py", "0.6.0")
    v20_data = run_isolated_benchmark("benchmark_v20_isolated.py", "2.0")
    
    # Verificar se todos foram bem-sucedidos
    if "error" in v010_data:
        print(f"\n❌ Falha no benchmark v0.1.0: {v010_data['error']}")
    if "error" in v060_data:
        print(f"\n❌ Falha no benchmark v0.6.0: {v060_data['error']}")
    if "error" in v20_data:
        print(f"\n❌ Falha no benchmark v2.0: {v20_data['error']}")
    
    # Se algum falhou, ainda assim continuar com os que funcionaram
    all_success = all("error" not in d for d in [v010_data, v060_data, v20_data])
    
    if not all_success:
        print("\n⚠️  Alguns benchmarks falharam, mas continuando com os disponíveis...")
    
    # Calcular melhorias
    print("\n" + "=" * 70)
    print("📊 RESULTADOS DA COMPARAÇÃO")
    print("=" * 70)
    
    # Comparação detalhada por tamanho
    if "error" not in v010_data and "error" not in v060_data and "error" not in v20_data:
        print("\n📏 BREAKDOWN POR TAMANHO DE TEXTO:\n")
        
        for i, size in enumerate(["small", "medium", "large"]):
            v010_result = v010_data["results"][i]
            v060_result = v060_data["results"][i]
            v20_result = v20_data["results"][i]
            
            print(f"   {size.upper()}:")
            print(f"      v0.1.0: {v010_result['avg_time_ms']:6.2f}ms")
            print(f"      v0.6.0: {v060_result['avg_time_ms']:6.2f}ms")
            print(f"      v2.0:   {v20_result['avg_time_ms']:6.2f}ms")
            
            improvement_06 = ((v010_result['avg_time_ms'] - v060_result['avg_time_ms']) / 
                             v010_result['avg_time_ms'] * 100)
            improvement_20 = ((v060_result['avg_time_ms'] - v20_result['avg_time_ms']) / 
                             v060_result['avg_time_ms'] * 100)
            improvement_total = ((v010_result['avg_time_ms'] - v20_result['avg_time_ms']) / 
                                v010_result['avg_time_ms'] * 100)
            
            print(f"      Melhoria v0.1.0→v0.6.0: {improvement_06:+.1f}%")
            print(f"      Melhoria v0.6.0→v2.0:   {improvement_20:+.1f}%")
            print(f"      Melhoria TOTAL:         {improvement_total:+.1f}%")
            print()
        
        # Resumo geral
        v010_avg = v010_data["overall_avg"]
        v060_avg = v060_data["overall_avg"]
        v20_avg = v20_data["overall_avg"]
        
        print("📈 RESUMO GERAL:\n")
        print(f"   v0.1.0 (baseline): {v010_avg:.2f}ms")
        print(f"   v0.6.0:            {v060_avg:.2f}ms ({((v010_avg - v060_avg) / v010_avg * 100):+.1f}%)")
        print(f"   v2.0:              {v20_avg:.2f}ms ({((v010_avg - v20_avg) / v010_avg * 100):+.1f}%)")
        print()
        
        speedup_06 = v010_avg / v060_avg
        speedup_20_from_06 = v060_avg / v20_avg
        speedup_total = v010_avg / v20_avg
        
        print(f"   Speedup v0.1.0→v0.6.0: {speedup_06:.2f}x")
        print(f"   Speedup v0.6.0→v2.0:   {speedup_20_from_06:.2f}x")
        print(f"   Speedup TOTAL:         {speedup_total:.2f}x")
    
    # Salvar resultados
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"real_comparison_3_versions_{timestamp}.json"
    
    comparison_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "type": "real_benchmark",
            "note": "Benchmarks reais executados via subprocess isolado"
        },
        "v010": v010_data,
        "v06": v060_data,
        "v20": v20_data
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: {output_file}")
    print("\n✅ Benchmark real concluído!")
    
    return comparison_data

if __name__ == "__main__":
    main()
