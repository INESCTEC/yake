#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

"""
Comparação de resultados de benchmarks
"""

# BASELINE (antes das otimizações)
BASELINE = {
    "small": {
        "time_mean": 10.886,
        "memory_mean": 0.17
    },
    "medium": {
        "time_mean": 47.619,
        "memory_mean": 0.58
    },
    "large": {
        "time_mean": 81.158,
        "memory_mean": 0.94
    }
}

# OTIMIZAÇÃO #1: List Comprehensions otimizadas
OPT1_LIST_COMP = {
    "small": {
        "time_mean": 11.195,
        "memory_mean": 0.17
    },
    "medium": {
        "time_mean": 40.894,
        "memory_mean": 0.58
    },
    "large": {
        "time_mean": 80.118,
        "memory_mean": 0.94
    }
}

# OTIMIZAÇÃO #1 + #2: List Comprehensions + String Interning
OPT2_STRING_INTERNING = {
    "small": {
        "time_mean": 11.076,
        "memory_mean": 0.17
    },
    "medium": {
        "time_mean": 42.086,
        "memory_mean": 0.59
    },
    "large": {
        "time_mean": 80.404,
        "memory_mean": 0.95
    }
}

# OTIMIZAÇÃO #1 + #3: List Comprehensions + Evitar NumPy em listas pequenas
OPT3_NO_NUMPY_SMALL = {
    "small": {
        "time_mean": 11.020,
        "memory_mean": 0.17
    },
    "medium": {
        "time_mean": 35.861,
        "memory_mean": 0.58
    },
    "large": {
        "time_mean": 75.087,
        "memory_mean": 0.94
    }
}


def compare_optimizations(baseline, optimized, opt_name):
    """Compara duas versões e calcula melhorias"""
    print(f"\n{'='*70}")
    print(f"📊 COMPARAÇÃO: {opt_name}")
    print(f"{'='*70}\n")
    
    improvements = []
    
    for size in ["small", "medium", "large"]:
        base_time = baseline[size]["time_mean"]
        opt_time = optimized[size]["time_mean"]
        base_mem = baseline[size]["memory_mean"]
        opt_mem = optimized[size]["memory_mean"]
        
        time_improvement = ((base_time - opt_time) / base_time) * 100
        memory_improvement = ((base_mem - opt_mem) / base_mem) * 100
        
        improvements.append(time_improvement)
        
        print(f"📈 Texto {size.upper()}:")
        print(f"   Tempo:    {base_time:.3f} ms → {opt_time:.3f} ms ", end="")
        if time_improvement > 0:
            print(f"(✅ +{time_improvement:.1f}% mais rápido)")
        elif time_improvement < 0:
            print(f"(❌ {abs(time_improvement):.1f}% mais lento)")
        else:
            print(f"(= sem mudança)")
        
        print(f"   Memória:  {base_mem:.2f} MB → {opt_mem:.2f} MB ", end="")
        if memory_improvement > 0:
            print(f"(✅ +{memory_improvement:.1f}% menos memória)")
        elif memory_improvement < 0:
            print(f"(❌ {abs(memory_improvement):.1f}% mais memória)")
        else:
            print(f"(= sem mudança)")
        print()
    
    avg_improvement = sum(improvements) / len(improvements)
    
    print(f"{'='*70}")
    print(f"🎯 RESUMO GERAL:")
    print(f"   Melhoria média de tempo: ", end="")
    if avg_improvement > 0:
        print(f"✅ +{avg_improvement:.2f}% mais rápido")
    elif avg_improvement < 0:
        print(f"❌ {abs(avg_improvement):.2f}% mais lento")
    else:
        print(f"= sem mudança")
    
    if avg_improvement >= 5:
        print(f"\n   ✅✅✅ OTIMIZAÇÃO EXCELENTE! (≥5% melhoria) - APLICAR!")
    elif avg_improvement >= 3:
        print(f"\n   ✅✅ OTIMIZAÇÃO BOA! (≥3% melhoria) - APLICAR!")
    elif avg_improvement > 0:
        print(f"\n   ⚠️  Melhoria marginal (<3%) - CONSIDERAR")
    else:
        print(f"\n   ❌ SEM MELHORIA - REVERTER!")
    
    print(f"{'='*70}\n")
    
    return avg_improvement


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔬 YAKE 2.0 - Análise de Otimizações")
    print("="*70)
    
    # Otimização #1
    improve1 = compare_optimizations(BASELINE, OPT1_LIST_COMP, "Otimização #1: List Comprehensions")
    
    # Otimização #2
    improve2 = compare_optimizations(OPT1_LIST_COMP, OPT2_STRING_INTERNING, "Otimização #2: String Interning (REVERTIDA)")
    
    # Otimização #3
    improve3 = compare_optimizations(OPT1_LIST_COMP, OPT3_NO_NUMPY_SMALL, "Otimização #3: Evitar NumPy em listas pequenas")
    
    # Comparação acumulada
    improve_total = compare_optimizations(BASELINE, OPT3_NO_NUMPY_SMALL, "TOTAL (OPT1 + OPT3)")
    
    print("\n📋 RESUMO DE TODAS AS OTIMIZAÇÕES:")
    print("="*70)
    print(f"1. List Comprehensions:          {'+' if improve1 > 0 else ''}{improve1:.2f}%")
    print(f"2. String Interning (REVERTIDA): {'+' if improve2 > 0 else ''}{improve2:.2f}%")
    print(f"3. Evitar NumPy (pequenas):      {'+' if improve3 > 0 else ''}{improve3:.2f}%")
    print(f"   ------------------------------------------")
    print(f"   TOTAL APLICADO (OPT1+OPT3):   {'+' if improve_total > 0 else ''}{improve_total:.2f}%")
    print("="*70)
