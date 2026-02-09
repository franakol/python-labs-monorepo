"""
Performance Benchmark Script

Compares async, threaded, and sequential approaches to web scraping.
"""

import asyncio
import time
import json
from pathlib import Path

# Import our three implementations
from scraper.fetcher import fetch_multiple_urls
from scraper.sequential import fetch_multiple_urls_sequential
from scraper.threaded import fetch_multiple_urls_threaded


def load_urls(filename: str = "urls.txt") -> list[str]:
    """Load URLs from file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def benchmark_async(urls: list[str]) -> dict:
    """Benchmark async implementation."""
    print("\n" + "="*60)
    print("ASYNC BENCHMARK")
    print("="*60)
    
    start = time.time()
    results = asyncio.run(fetch_multiple_urls(urls))
    total_time = time.time() - start
    
    return {
        'method': 'async',
        'total_time': total_time,
        'num_urls': len(results),
        'avg_time': total_time / len(results) if results else 0
    }


def benchmark_threaded(urls: list[str]) -> dict:
    """Benchmark threaded implementation."""
    print("\n" + "="*60)
    print("THREADED BENCHMARK")
    print("="*60)
    
    start = time.time()
    results = fetch_multiple_urls_threaded(urls, max_workers=10)
    total_time = time.time() - start
    
    return {
        'method': 'threaded',
        'total_time': total_time,
        'num_urls': len(results),
        'avg_time': total_time / len(results) if results else 0
    }


def benchmark_sequential(urls: list[str]) -> dict:
    """Benchmark sequential implementation."""
    print("\n" + "="*60)
    print("SEQUENTIAL BENCHMARK")
    print("="*60)
    
    start = time.time()
    results = fetch_multiple_urls_sequential(urls)
    total_time = time.time() - start
    
    return {
        'method': 'sequential',
        'total_time': total_time,
        'num_urls': len(results),
        'avg_time': total_time / len(results) if results else 0
    }


def print_comparison(results: list[dict]):
    """Print comparison of all methods."""
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    # Sort by total time
    sorted_results = sorted(results, key=lambda x: x['total_time'])
    
    fastest = sorted_results[0]
    
    print(f"\n{'Method':<15} {'Total Time':<15} {'Avg/URL':<15} {'Speedup':<10}")
    print("-" * 60)
    
    for result in sorted_results:
        speedup = fastest['total_time'] / result['total_time']
        print(f"{result['method']:<15} "
              f"{result['total_time']:<15.2f} "
              f"{result['avg_time']:<15.2f} "
              f"{speedup:<10.2f}x")
    
    print("\n" + "="*60)
    print(f"Winner: {fastest['method'].upper()}")
    print(f"Improvement over sequential: "
          f"{sorted_results[-1]['total_time'] / fastest['total_time']:.2f}x faster")
    print("="*60)
    
    # Save results to JSON
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "benchmark_results.json", 'w') as f:
        json.dump({
            'results': results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'num_urls': results[0]['num_urls'] if results else 0
        }, f, indent=2)
    
    print(f"\nResults saved to: {output_dir / 'benchmark_results.json'}")


def main():
    """Main benchmark execution."""
    # Load test URLs
    urls = load_urls()
    print(f"Loaded {len(urls)} URLs for benchmarking\n")
    
    # Run all benchmarks
    results = []
    
    # Async
    async_result = benchmark_async(urls)
    results.append(async_result)
    
    # Threaded
    threaded_result = benchmark_threaded(urls)
    results.append(threaded_result)
    
    # Sequential
    sequential_result = benchmark_sequential(urls)
    results.append(sequential_result)
    
    # Print comparison
    print_comparison(results)


if __name__ == "__main__":
    main()
