# pylint: skip-file
"""
Benchmark: Built-in Functions Optimization
Testing truthiness vs len() comparisons
"""

import time
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from yake import KeywordExtractor


def load_test_texts():
    """Load test texts of different sizes"""
    return {
        'small': """
        Artificial intelligence and machine learning are transforming technology.
        Deep learning models can process natural language with high accuracy.
        """,
        'medium': """
        Artificial intelligence and machine learning are transforming the technology 
        landscape in unprecedented ways. Deep learning models powered by neural networks 
        can process natural language with remarkable accuracy and efficiency. These 
        systems are being deployed across various industries including healthcare, 
        finance, and autonomous vehicles. The ability to analyze vast amounts of data 
        and extract meaningful patterns has become crucial for modern applications.
        Computer vision techniques enable machines to understand and interpret visual 
        information from the world around us.
        """,
        'large': """
        Artificial intelligence and machine learning are transforming the technology 
        landscape in unprecedented ways. Deep learning models powered by neural networks 
        can process natural language with remarkable accuracy and efficiency. These 
        advanced systems are being deployed across various industries including healthcare, 
        finance, autonomous vehicles, and smart city infrastructure. The ability to 
        analyze vast amounts of data and extract meaningful patterns has become crucial 
        for modern applications and decision-making processes.
        
        Computer vision techniques enable machines to understand and interpret visual 
        information from the world around us. Natural language processing allows systems 
        to comprehend human communication in multiple languages. Reinforcement learning 
        helps agents learn optimal strategies through interaction with their environment.
        Transfer learning enables models to leverage knowledge from one domain to improve 
        performance in another.
        
        The convergence of big data, cloud computing, and advanced algorithms has 
        accelerated the pace of innovation in artificial intelligence research and 
        development. Organizations are investing heavily in AI infrastructure and talent 
        to remain competitive in the digital economy. Ethical considerations around bias, 
        privacy, and transparency have become central to the responsible development and 
        deployment of AI systems.
        """
    }


def benchmark_extraction(text, size_name, iterations=10):
    """Benchmark keyword extraction"""
    extractor = KeywordExtractor(lan="en", n=3, top=20)
    
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        keywords = extractor.extract_keywords(text)
        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)  # Convert to milliseconds
    
    return {
        'size': size_name,
        'mean': sum(times) / len(times),
        'min': min(times),
        'max': max(times),
        'keywords': len(keywords)
    }


def main():
    print("=" * 70)
    print("BENCHMARK: Built-in Functions Optimization")
    print("Testing: truthiness vs len() comparisons")
    print("=" * 70)
    
    texts = load_test_texts()
    results = {}
    
    for size_name, text in texts.items():
        print(f"\n{size_name.upper()} text ({len(text.split())} words)...")
        result = benchmark_extraction(text, size_name, iterations=20)
        results[size_name] = result
        
        print(f"  Mean: {result['mean']:.2f}ms")
        print(f"  Min:  {result['min']:.2f}ms")
        print(f"  Max:  {result['max']:.2f}ms")
        print(f"  Keywords extracted: {result['keywords']}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for size_name, result in results.items():
        print(f"{size_name:10s}: {result['mean']:7.2f}ms")
    
    avg_time = sum(r['mean'] for r in results.values()) / len(results)
    print(f"{'Average':10s}: {avg_time:7.2f}ms")
    print("=" * 70)


if __name__ == "__main__":
    main()
