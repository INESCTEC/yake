#!/usr/bin/env python3
# pylint: skip-file
"""
Benchmark isolado para YAKE v0.6.0
Executa dentro do contexto da pasta yake_0.6.0
"""

import sys
import time
import json
from pathlib import Path

# Add yake_0.6.0 to path - this version has proper package structure
v060_path = Path(__file__).parent.parent / "yake" / "yake_0.6.0"
sys.path.insert(0, str(v060_path))

# Need to make it a proper package by setting up the import path correctly
import importlib.util

# Create a yake package namespace
yake_init = v060_path / "__init__.py"
spec = importlib.util.spec_from_file_location("yake_v060", yake_init)
yake_pkg = importlib.util.module_from_spec(spec)
sys.modules['yake_v060'] = yake_pkg

# Add subdirectories
sys.modules['yake_v060.core'] = type(sys)('core')
sys.modules['yake_v060.data'] = type(sys)('data')

# Load data module first
data_core_path = v060_path / "data" / "core.py"
data_spec = importlib.util.spec_from_file_location("yake_v060.data.core", data_core_path)
data_module = importlib.util.module_from_spec(data_spec)
sys.modules['yake_v060.data.core'] = data_module
data_spec.loader.exec_module(data_module)

# Load other data modules
for data_file in ["single_word.py", "composed_word.py", "utils.py"]:
    data_file_path = v060_path / "data" / data_file
    if data_file_path.exists():
        module_name = f"yake_v060.data.{data_file[:-3]}"
        data_spec = importlib.util.spec_from_file_location(module_name, data_file_path)
        data_mod = importlib.util.module_from_spec(data_spec)
        sys.modules[module_name] = data_mod
        data_spec.loader.exec_module(data_mod)

# Load Levenshtein
lev_path = v060_path / "core" / "Levenshtein.py"
lev_spec = importlib.util.spec_from_file_location("yake_v060.core.Levenshtein", lev_path)
lev_module = importlib.util.module_from_spec(lev_spec)
sys.modules['yake_v060.core.Levenshtein'] = lev_module
lev_spec.loader.exec_module(lev_module)

# Now load yake with all dependencies in place
# Patch the imports in yake.py
yake_path = v060_path / "core" / "yake.py"
yake_code = yake_path.read_text(encoding='utf-8')
yake_code = yake_code.replace("from yake.data import", "from yake_v060.data import")
yake_code = yake_code.replace("from yake.core.Levenshtein import", "from yake_v060.core.Levenshtein import")

# Compile and execute
import types
yake_module = types.ModuleType("yake_v060.core.yake")
exec(yake_code, yake_module.__dict__)
sys.modules['yake_v060.core.yake'] = yake_module

KeywordExtractor = yake_module.KeywordExtractor

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

def benchmark_v060():
    """Executa benchmark na versão 0.6.0"""
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
        "version": "0.6.0",
        "results": results,
        "overall_avg": sum(r["avg_time_ms"] for r in results) / len(results)
    }

if __name__ == "__main__":
    try:
        result = benchmark_v060()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e), "version": "0.6.0"}), file=sys.stderr)
        sys.exit(1)
