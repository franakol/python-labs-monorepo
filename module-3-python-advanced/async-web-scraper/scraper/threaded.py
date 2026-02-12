"""
Threaded Web Scraper

Multi-threaded version for performance comparison.
"""

import requests
import time
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_url_threaded(url: str) -> Tuple[str, str, float]:
    """
    Fetch a single URL (for use in threading).
    
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


def fetch_multiple_urls_threaded(urls: List[str], max_workers: int = 10) -> List[Tuple[str, str, float]]:
    """
    Fetch multiple URLs using threading.
    
    Args:
        urls: List of URLs to fetch
        max_workers: Maximum number of threads
        
    Returns:
        List of tuples (url, content, fetch_time)
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_url_threaded, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                url = future_to_url[future]
                print(f"✗ Exception for {url}: {str(e)}")
    
    return results


def main():
    """Main entry point for testing threaded scraper."""
    test_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/html",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/users/1",
    ]
    
    print("Starting threaded fetch...")
    start = time.time()
    
    results = fetch_multiple_urls_threaded(test_urls)
    
    total_time = time.time() - start
    print(f"\n{'='*60}")
    print(f"Fetched {len(results)} URLs in {total_time:.2f}s (Threaded)")
    print(f"Average time per URL: {total_time/len(results):.2f}s")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
