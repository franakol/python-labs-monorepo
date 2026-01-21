"""
Async HTTP Fetcher Module

Provides async functions for fetching web pages using aiohttp and asyncio.
"""

import asyncio
import aiohttp
from typing import List, Tuple
import time


async def fetch_url(session: aiohttp.ClientSession, url: str) -> Tuple[str, str, float]:
    """
    Fetch a single URL asynchronously.
    
    Args:
        session: aiohttp ClientSession instance
        url: URL to fetch
        
    Returns:
        Tuple of (url, content, fetch_time)
    """
    start_time = time.time()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            content = await response.text()
            fetch_time = time.time() - start_time
            print(f"✓ Fetched {url} in {fetch_time:.2f}s (status: {response.status})")
            return (url, content, fetch_time)
    except asyncio.TimeoutError:
        fetch_time = time.time() - start_time
        print(f"✗ Timeout fetching {url} after {fetch_time:.2f}s")
        return (url, "", fetch_time)
    except Exception as e:
        fetch_time =time.time() - start_time
        print(f"✗ Error fetching {url}: {str(e)}")
        return (url, "", fetch_time)


async def fetch_multiple_urls(urls: List[str]) -> List[Tuple[str, str, float]]:
    """
    Fetch multiple URLs concurrently using asyncio.gather().
    
    Args:
        urls: List of URLs to fetch
        
    Returns:
        List of tuples (url, content, fetch_time)
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, tuple):
                valid_results.append(result)
            else:
                print(f"✗ Exception occurred: {result}")
                
        return valid_results


async def main():
    """Main entry point for testing the async fetcher."""
    # Sample URLs for testing
    test_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/html",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/users/1",
    ]
    
    print("Starting async fetch...")
    start = time.time()
    
    results = await fetch_multiple_urls(test_urls)
    
    total_time = time.time() - start
    print(f"\n{'='*60}")
    print(f"Fetched {len(results)} URLs in {total_time:.2f}s")
    print(f"Average time per URL: {total_time/len(results):.2f}s")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
