#!/usr/bin/env python3
# pylint: skip-file
"""
Lightweight Robust Benchmark for YAKE
====================================

A simplified version of the robust benchmark that works without heavy dependencies
while still providing statistical rigor and useful metrics.
"""

import gc
import json
import os
import platform
import statistics
import sys
import time
import tracemalloc
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Project imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("⚠️  psutil not available - system monitoring disabled")


@dataclass
class SimpleBenchmarkConfig:
    """Simplified configuration for lightweight benchmarking."""
    
    num_iterations: int = 50
    warmup_iterations: int = 5
    confidence_level: float = 0.95
    outlier_threshold: float = 2.0
    
    disable_gc_during_test: bool = True
    profile_memory: bool = True
    monitor_system: bool = HAS_PSUTIL
    
    test_languages: List[str] = None
    max_ngram_sizes: List[int] = None
    
    save_raw_data: bool = True
    verbose: bool = True
    export_formats: List[str] = None
    
    def __post_init__(self):
        if self.test_languages is None:
            self.test_languages = ['en', 'pt', 'es']
        if self.max_ngram_sizes is None:
            self.max_ngram_sizes = [1, 2, 3, 4]
        if self.export_formats is None:
            self.export_formats = ['json']


@dataclass
class SimpleBenchmarkResult:
    """Results from a lightweight benchmark run."""
    
    test_name: str
    language: str
    ngram_size: int
    text_length: int
    
    execution_times: List[float]
    memory_peak: Optional[int] = None
    
    num_keywords: int = 0
    keywords_sample: List[Tuple[str, float]] = None
    
    # Statistical analysis
    mean_time: Optional[float] = None
    median_time: Optional[float] = None
    std_time: Optional[float] = None
    min_time: Optional[float] = None
    max_time: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    outliers_removed: int = 0
    
    # Performance metrics
    throughput_chars_per_sec: Optional[float] = None
    throughput_words_per_sec: Optional[float] = None
    
    # System info
    cpu_percent: Optional[float] = None
    memory_percent: Optional[float] = None
    
    def __post_init__(self):
        if self.keywords_sample is None:
            self.keywords_sample = []


class SimpleSystemMonitor:
    """Simple system monitor without external dependencies."""
    
    def __init__(self):
        self.monitoring = False
        self.cpu_samples = []
        self.memory_samples = []
        self.has_psutil = HAS_PSUTIL
    
    def start_monitoring(self):
        """Start basic monitoring if psutil is available."""
        if not self.has_psutil:
            return
        
        self.monitoring = True
        self.cpu_samples.clear()
        self.memory_samples.clear()
    
    def stop_monitoring(self):
        """Stop monitoring and return basic stats."""
        self.monitoring = False
        
        if not self.has_psutil:
            return {}
        
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
            }
        except Exception:
            return {}


class LightweightBenchmark:
    """Lightweight benchmark system that works without heavy dependencies."""
    
    def __init__(self, config: Optional[SimpleBenchmarkConfig] = None):
        self.config = config or SimpleBenchmarkConfig()
        self.results: List[SimpleBenchmarkResult] = []
        self.system_info = self._get_system_info()
        self.monitor = SimpleSystemMonitor()
        
        # Import YAKE
        self._import_yake()
    
    def _import_yake(self):
        """Import YAKE from local code."""
        try:
            from yake.core.yake import KeywordExtractor
            self.yake_path = str(project_root / "yake" / "core" / "yake.py")
            self.is_local = True
        except ImportError as e:
            raise ImportError(f"Could not import local YAKE: {e}")
        
        self.KeywordExtractor = KeywordExtractor
        
        if self.config.verbose:
            print(f"🔍 Using YAKE from: {self.yake_path}")
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        if HAS_PSUTIL:
            info.update({
                'cpu_count': psutil.cpu_count(logical=False),
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'memory_total': psutil.virtual_memory().total,
            })
        
        return info
    
    def _remove_outliers_simple(self, times: List[float]) -> Tuple[List[float], int]:
        """Remove outliers using simple statistical method."""
        if len(times) < 3:
            return times, 0
        
        mean_time = statistics.mean(times)
        std_time = statistics.stdev(times)
        
        if std_time == 0:
            return times, 0
        
        threshold = self.config.outlier_threshold
        filtered_times = []
        outliers_count = 0
        
        for t in times:
            z_score = abs((t - mean_time) / std_time)
            if z_score <= threshold:
                filtered_times.append(t)
            else:
                outliers_count += 1
        
        # Keep at least half the measurements
        if len(filtered_times) < len(times) // 2:
            return times, 0
        
        return filtered_times, outliers_count
    
    def _calculate_statistics_simple(self, times: List[float]) -> Dict[str, float]:
        """Calculate statistics using only standard library."""
        if not times:
            return {}
        
        # Remove outliers
        clean_times, outliers_removed = self._remove_outliers_simple(times)
        
        # Basic statistics
        stats_dict = {
            'mean': statistics.mean(clean_times),
            'median': statistics.median(clean_times),
            'min': min(clean_times),
            'max': max(clean_times),
            'outliers_removed': outliers_removed,
        }
        
        # Standard deviation
        if len(clean_times) > 1:
            stats_dict['std'] = statistics.stdev(clean_times)
            
            # Simple confidence interval (assuming normal distribution)
            n = len(clean_times)
            se = stats_dict['std'] / (n ** 0.5)
            # Using t=1.96 for 95% CI (approximate)
            margin = 1.96 * se
            
            stats_dict['confidence_interval'] = (
                stats_dict['mean'] - margin,
                stats_dict['mean'] + margin
            )
        else:
            stats_dict['std'] = 0.0
            stats_dict['confidence_interval'] = (stats_dict['mean'], stats_dict['mean'])
        
        return stats_dict
    
    def _classify_text_size(self, text: str) -> str:
        """Classify text size based on character count."""
        char_count = len(text)
        if char_count < 500:
            return "small"
        elif char_count < 2000:
            return "medium"
        else:
            return "large"
    
    def benchmark_extraction(self, text: str, test_name: str, language: str = "en", 
                           ngram_size: int = 3) -> SimpleBenchmarkResult:
        """Benchmark keyword extraction with lightweight metrics."""
        
        text_size = self._classify_text_size(text)
        
        if self.config.verbose:
            print(f"\n🧪 {test_name} (n={ngram_size}, lang={language})")
            print(f"📏 Text length: {len(text):,} chars, {len(text.split()):,} words ({text_size})")
        
        # Create extractor
        extractor = self.KeywordExtractor(lan=language, n=ngram_size)
        
        # Warm-up runs
        if self.config.verbose:
            print("🔥 Warming up...", end=" ")
        for _ in range(self.config.warmup_iterations):
            _ = extractor.extract_keywords(text)
        if self.config.verbose:
            print("✓")
        
        # Setup memory profiling
        if self.config.profile_memory:
            tracemalloc.start()
        
        # Setup GC control
        if self.config.disable_gc_during_test:
            gc.disable()
        
        # Start system monitoring
        if self.config.monitor_system:
            self.monitor.start_monitoring()
        
        # Benchmark runs
        execution_times = []
        keywords_result = None
        
        try:
            if self.config.verbose:
                print(f"⏱️  Running {self.config.num_iterations} iterations...", end=" ")
            
            for i in range(self.config.num_iterations):
                if self.config.disable_gc_during_test:
                    gc.collect()
                
                start_time = time.perf_counter()
                keywords_result = extractor.extract_keywords(text)
                end_time = time.perf_counter()
                
                execution_times.append(end_time - start_time)
                
                if self.config.verbose and (i + 1) % 10 == 0:
                    print(f"{i+1}", end=" ")
            
            if self.config.verbose:
                print("✓")
                
        finally:
            # Stop monitoring
            system_metrics = {}
            if self.config.monitor_system:
                system_metrics = self.monitor.stop_monitoring()
            
            # Re-enable GC
            if self.config.disable_gc_during_test:
                gc.enable()
            
            # Get memory info
            memory_peak = None
            if self.config.profile_memory:
                current, peak = tracemalloc.get_traced_memory()
                memory_peak = peak
                tracemalloc.stop()
        
        # Calculate statistics
        stats_dict = self._calculate_statistics_simple(execution_times)
        
        # Calculate throughput
        mean_time = stats_dict.get('mean', 0)
        chars_per_sec = len(text) / mean_time if mean_time > 0 else 0
        words_per_sec = len(text.split()) / mean_time if mean_time > 0 else 0
        
        # Create result
        result = SimpleBenchmarkResult(
            test_name=test_name,
            language=language,
            ngram_size=ngram_size,
            text_length=len(text),
            execution_times=execution_times if self.config.save_raw_data else [],
            memory_peak=memory_peak,
            num_keywords=len(keywords_result) if keywords_result else 0,
            keywords_sample=keywords_result[:5] if keywords_result else [],
            mean_time=stats_dict.get('mean'),
            median_time=stats_dict.get('median'),
            std_time=stats_dict.get('std'),
            min_time=stats_dict.get('min'),
            max_time=stats_dict.get('max'),
            confidence_interval=stats_dict.get('confidence_interval'),
            outliers_removed=stats_dict.get('outliers_removed', 0),
            throughput_chars_per_sec=chars_per_sec,
            throughput_words_per_sec=words_per_sec,
            cpu_percent=system_metrics.get('cpu_percent'),
            memory_percent=system_metrics.get('memory_percent')
        )
        
        # Print summary
        if self.config.verbose:
            self._print_result_summary(result)
        
        self.results.append(result)
        return result
    
    def _print_result_summary(self, result: SimpleBenchmarkResult):
        """Print a summary of benchmark result."""
        print(f"   📊 Results:")
        print(f"      Mean: {result.mean_time*1000:.2f}ms ± {result.std_time*1000:.2f}ms")
        print(f"      Median: {result.median_time*1000:.2f}ms")
        print(f"      Range: {result.min_time*1000:.2f}ms - {result.max_time*1000:.2f}ms")
        if result.confidence_interval:
            ci_low, ci_high = result.confidence_interval
            print(f"      95% CI: [{ci_low*1000:.2f}, {ci_high*1000:.2f}]ms")
        print(f"      Outliers removed: {result.outliers_removed}")
        print(f"      Keywords: {result.num_keywords}")
        print(f"      Throughput: {result.throughput_words_per_sec:.0f} words/sec")
        
        if result.memory_peak:
            print(f"      Memory peak: {result.memory_peak / 1024 / 1024:.1f} MB")
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a human-readable summary of benchmark results."""
        if not self.results:
            return {"message": "No results available"}
        
        # Calculate overall statistics
        all_times = [r.mean_time for r in self.results if r.mean_time]
        total_keywords = sum(r.num_keywords for r in self.results)
        
        # Performance by n-gram size
        ngram_stats = {}
        for result in self.results:
            ngram = result.ngram_size
            if ngram not in ngram_stats:
                ngram_stats[ngram] = []
            ngram_stats[ngram].append(result.mean_time)
        
        ngram_summary = {}
        for ngram, times in ngram_stats.items():
            ngram_summary[f"ngram_{ngram}"] = {
                "average_time_ms": round(statistics.mean(times) * 1000, 2),
                "test_count": len(times),
                "fastest_ms": round(min(times) * 1000, 2),
                "slowest_ms": round(max(times) * 1000, 2)
            }
        
        # Text size analysis
        size_categories = {"small": [], "medium": [], "large": []}
        for result in self.results:
            if result.text_length < 500:
                size_categories["small"].append(result.mean_time)
            elif result.text_length < 2000:
                size_categories["medium"].append(result.mean_time)
            else:
                size_categories["large"].append(result.mean_time)
        
        size_summary = {}
        for size, times in size_categories.items():
            if times:
                size_summary[f"{size}_text"] = {
                    "average_time_ms": round(statistics.mean(times) * 1000, 2),
                    "test_count": len(times)
                }
        
        return {
            "overall_performance": {
                "total_tests": len(self.results),
                "total_keywords_extracted": total_keywords,
                "average_time_all_tests_ms": round(statistics.mean(all_times) * 1000, 2) if all_times else 0,
                "fastest_test_ms": round(min(all_times) * 1000, 2) if all_times else 0,
                "slowest_test_ms": round(max(all_times) * 1000, 2) if all_times else 0,
                "total_runtime_estimate_ms": round(sum(all_times) * 1000, 2) if all_times else 0
            },
            "performance_by_ngram": ngram_summary,
            "performance_by_text_size": size_summary,
            "languages_tested": list(set(r.language for r in self.results)),
            "memory_usage": {
                "peak_mb": max((r.memory_peak or 0) for r in self.results) / 1024 / 1024,
                "average_mb": statistics.mean((r.memory_peak or 0) for r in self.results) / 1024 / 1024
            } if any(r.memory_peak for r in self.results) else {"message": "Memory profiling not available"}
        }

    def save_results(self, output_dir: Optional[Path] = None, prefix: str = "yake_benchmark_lightweight") -> Path:
        """Save benchmark results with configurable filename prefix and descriptive info."""
        if output_dir is None:
            # Use same directory as benchmark_definitivo for consistency
            output_dir = project_root / "scripts" / "results"
        
        output_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Create more descriptive filename
        num_tests = len(self.results)
        languages = "_".join(sorted(set(r.language for r in self.results))) if self.results else "unknown"
        iterations = self.config.num_iterations
        
        # Generate hash for consistency with benchmark_definitivo
        import hashlib
        results_str = json.dumps([asdict(result) for result in self.results], sort_keys=True, default=str)
        results_hash = hashlib.md5(results_str.encode()).hexdigest()[:8]
        
        filename = f"{prefix}_{timestamp}_{results_hash}.json"
        
        # Prepare data with summary - match benchmark_definitivo structure
        summary = self._generate_summary()
        
        data = {
            "benchmark_type": "lightweight_robusto",
            "version": "2.0", 
            "timestamp": timestamp,
            "results_hash": results_hash,
            "data": {
                "summary": summary,
                "execution_metadata": {
                    "timestamp": timestamp,
                    "human_readable_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "benchmark_type": "lightweight",
                    "total_tests": num_tests,
                    "languages_tested": languages.split('_') if languages != 'unknown' else [],
                    "iterations_per_test": iterations,
                    "config": asdict(self.config),
                    "system_info": self.system_info,
                    "yake_path": self.yake_path,
                    "is_local_code": self.is_local
                },
                "detailed_results": [asdict(result) for result in self.results]
            }
        }
        
        # Save JSON with same encoding as benchmark_definitivo
        json_file = output_dir / filename
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        # Create latest link for consistency with benchmark_definitivo
        latest_path = output_dir / "latest_benchmark_lightweight.json"
        try:
            if latest_path.exists():
                latest_path.unlink()
            with open(latest_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception:
            pass  # Silent failure if can't create link
        
        if self.config.verbose:
            print(f"\n💾 Results saved to: {json_file}")
            print(f"🔗 Latest link: {latest_path}")
        
        return json_file


if __name__ == "__main__":
    # Quick test
    config = SimpleBenchmarkConfig(
        num_iterations=20,
        warmup_iterations=3,
        verbose=True
    )
    
    benchmark = LightweightBenchmark(config)
    
    # Test text
    test_text = """
    Machine learning and artificial intelligence are revolutionizing technology.
    Deep learning algorithms process vast amounts of data to identify patterns.
    Natural language processing enables computers to understand human language.
    """
    
    # Run benchmark
    result = benchmark.benchmark_extraction(test_text, "Lightweight Test")
    
    # Save results
    benchmark.save_results()
    
    print(f"\n✅ Lightweight benchmark completed!")
    print(f"⏱️  Mean time: {result.mean_time*1000:.2f}ms")
    print(f"📊 Keywords: {result.num_keywords}")