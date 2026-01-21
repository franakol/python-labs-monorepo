"""
Sequential Web Scraper

Non-async version for performance comparison.
"""

import requests
import time
from typing import List, Tuple


def fetch_url_sequential(url: str) -> Tuple[str, str, float]:
    """
    Fetch a single URL synchronously.
    
    Args:
        url: URL to fetch
        
    Returns:
        Tuple of (url, content, fetch_time)
    """
    start_time = time.time()
    try:
        response = requests.get(url, timeout=30)
        content = response.text
        fetch_time = time.time() - start_time
        print(f"✓ Fetched {url} in {fetch_time:.2f}s")
        return (url, content, fetch_time)
    except Exception as e:
        fetch_time = time.time() - start_time
        print(f"✗ Error fetching {url}: {str(e)}")
        return (url, "", fetch_time)


def fetch_multiple_urls_sequential(urls: List[str]) -> List[Tuple[str, str, float]]:
    """
    Fetch multiple URLs sequentially (one after another).
    
    Args:
        urls: List of URLs to fetch
        
    Returns:
        List of tuples (url, content, fetch_time)
    """
    results = []
    for url in urls:
        result = fetch_url_sequential(url)
        results.append(result)
    return results


def main():
    """Main entry point for testing sequential scraper."""
    test_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/html",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/users/1",
    ]
    
    print("Starting sequential fetch...")
    start = time.time()
    
    results = fetch_multiple_urls_sequential(test_urls)
    
    total_time = time.time() - start
    print(f"\n{'='*60}")
    print(f"Fetched {len(results)} URLs in {total_time:.2f}s (Sequential)")
    print(f"Average time per URL: {total_time/len(results):.2f}s")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
