"""
Async Generators for Response Processing

Provides async generators for memory-efficient processing of HTTP responses.
"""

import asyncio
import aiohttp
from typing import AsyncGenerator, Tuple


async def fetch_and_yield(session: aiohttp.ClientSession, url: str) -> AsyncGenerator[Tuple[str, str], None]:
    """
    Async generator that fetches a URL and yields the response.
    
    Args:
        session: aiohttp ClientSession
        url: URL to fetch
        
    Yields:
        Tuple of (url, content)
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            content = await response.text()
            yield (url, content)
    except Exception as e:
        print(f"Error in generator for {url}: {str(e)}")
        yield (url, "")


async def process_urls_generator(urls: list[str]) -> AsyncGenerator[Tuple[str, str], None]:
    """
    Async generator that processes multiple URLs concurrently.
    
    Args:
        urls: List of URLs to process
        
    Yields:
        Tuples of (url, content) as they complete
    """
    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_single_url_for_generator(session, url))
            tasks.append(task)
        
        # Yield results as they complete
        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                yield result


async def fetch_single_url_for_generator(session: aiohttp.ClientSession, url: str) -> Tuple[str, str]:
    """
    Helper function to fetch a single URL for the generator.
    
    Args:
        session: aiohttp ClientSession
        url: URL to fetch
        
    Returns:
        Tuple of (url, content)
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            content = await response.text()
            print(f"✓ Generator fetched: {url}")
            return (url, content)
    except Exception as e:
        print(f"✗ Generator error for {url}: {str(e)}")
        return (url, "")


# Example usage
if __name__ == "__main__":
    async def main():
        urls = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2",
            "https://httpbin.org/html",
        ]
        
        print("Processing URLs with async generator...")
        
        # Using async for loop with generator
        async for url, content in process_urls_generator(urls):
            print(f"Received {url}: {len(content)} bytes")
        
        print("Done!")
    
    asyncio.run(main())
