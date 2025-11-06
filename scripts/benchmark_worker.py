# pylint: skip-file
"""
Benchmark worker para versões antigas do YAKE
Executa em processo isolado para evitar conflitos de import
"""

import sys
import time
import tracemalloc
from pathlib import Path

def run_benchmark(version, text, iterations=15):
    """Run benchmark for specific version"""
    BASE_PATH = Path(__file__).parent.parent
    
    # Setup path based on version
    if version == "v0.1.0":
        sys.path.insert(0, str(BASE_PATH / "yake"))
        from yake_1.0.0 import yake
        KeywordExtractor = yake.KeywordExtractor
    elif version == "v0.6.0":
        sys.path.insert(0, str(BASE_PATH / "yake"))
        from yake_0.6.0.core import yake
        KeywordExtractor = yake.KeywordExtractor
    elif version == "v2.0":
        sys.path.insert(0, str(BASE_PATH))
        from yake import KeywordExtractor
    else:
        raise ValueError(f"Unknown version: {version}")
    
    times = []
    memory_usages = []
    
    for _ in range(iterations):
        tracemalloc.start()
        start = time.perf_counter()
        
        extractor = KeywordExtractor(lan="en", n=3, top=20)
        keywords = extractor.extract_keywords(text)
        
        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        times.append(elapsed * 1000)
        memory_usages.append(peak / 1024 / 1024)
    
    return {
        'mean_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'mean_memory': sum(memory_usages) / len(memory_usages),
        'keywords_count': len(keywords)
    }


if __name__ == "__main__":
    import json
    
    version = sys.argv[1]
    text = sys.argv[2]
    iterations = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    
    result = run_benchmark(version, text, iterations)
    print(json.dumps(result))
