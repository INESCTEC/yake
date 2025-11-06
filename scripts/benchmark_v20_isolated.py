#!/usr/bin/env python3
# pylint: skip-file
"""
Benchmark isolado para YAKE v2.0 (current)
"""

import sys
import time
import json
from pathlib import Path

# Add current yake to path
v20_path = Path(__file__).parent.parent
sys.path.insert(0, str(v20_path))

# Import YAKE v2.0
from yake.core.yake import KeywordExtractor

# Test datasets
datasets = [
    {
        "name": "small",
        "text": """
        Inteligência artificial e machine learning estão revolucionando a tecnologia moderna.
        Algoritmos de deep learning permitem análise avançada de dados e reconhecimento de padrões.
        Cloud computing oferece infraestrutura escalável para aplicações empresariais.
        """
    },
    {
        "name": "medium",
        "text": """
        A ciência de dados combina estatística, programação e conhecimento de domínio para extrair 
        insights valiosos de grandes volumes de dados. Python e R são linguagens predominantes 
        nesta área, oferecendo bibliotecas especializadas como pandas, scikit-learn e ggplot2.
        
        O processo de análise de dados inclui coleta, limpeza, exploração, modelagem e visualização.
        Técnicas de machine learning supervisionado e não supervisionado permitem descobrir padrões
        ocultos e fazer previsões precisas. A visualização de dados é crucial para comunicar
        resultados de forma clara e impactante.
        """
    },
    {
        "name": "large",
        "text": """
        Artificial intelligence and machine learning have fundamentally transformed the landscape
        of modern technology and business operations. Deep learning algorithms, powered by neural
        networks with multiple hidden layers, enable computers to recognize complex patterns in
        data that were previously impossible to detect using traditional programming approaches.
        
        Natural language processing has revolutionized how machines understand and generate human
        language. Large language models like GPT and BERT have demonstrated remarkable capabilities
        in text generation, translation, summarization, and question answering. These models are
        trained on massive datasets containing billions of text samples from diverse sources.
        
        Computer vision applications have reached superhuman performance in many domains, including
        medical image analysis, autonomous driving, and facial recognition. Convolutional neural
        networks excel at extracting hierarchical features from images, enabling precise object
        detection and classification.
        """
    }
]

def benchmark_v20():
    """Executa benchmark na versão 2.0"""
    results = []
    
    for dataset in datasets:
        # Criar extractor
        extractor = KeywordExtractor(n=3, top=20)
        
        # Warmup
        _ = extractor.extract_keywords(dataset["text"])
        
        # Benchmark
        times = []
        iterations = 10
        
        for _ in range(iterations):
            start = time.perf_counter()
            keywords = extractor.extract_keywords(dataset["text"])
            end = time.perf_counter()
            times.append((end - start) * 1000)
        
        # Calcular estatísticas
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        median_time = sorted(times)[len(times) // 2]
        
        results.append({
            "size": dataset["name"],
            "avg_time_ms": avg_time,
            "median_time_ms": median_time,
            "min_time_ms": min_time,
            "max_time_ms": max_time,
            "iterations": iterations,
            "keywords_count": len(keywords)
        })
    
    return {
        "version": "2.0",
        "results": results,
        "overall_avg": sum(r["avg_time_ms"] for r in results) / len(results)
    }

if __name__ == "__main__":
    try:
        result = benchmark_v20()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e), "version": "2.0"}), file=sys.stderr)
        sys.exit(1)
