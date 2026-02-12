"""
Decorators for Async Functions

Provides retry and rate-limiting decorators for async HTTP requests.
"""

import asyncio
import functools
import time
from typing import Callable, Any


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry an async function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay on each retry
    
    Example:
        @retry(max_attempts=3, delay=1.0, backoff=2.0)
        async def fetch_data(url):
            # async code here
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_attempts:
                        print(f"✗ Max retries ({max_attempts}) reached for {func.__name__}")
                        raise
                    
                    print(f"⚠ Attempt {attempt}/{max_attempts} failed: {str(e)}")
                    print(f"  Retrying in {current_delay:.1f}s...")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator


def rate_limit(calls_per_second: float = 2.0):
    """
    Decorator to rate-limit async function calls.
    
    Args:
        calls_per_second: Maximum number of calls allowed per second
        
    Example:
        @rate_limit(calls_per_second=2.0)
        async def fetch_data(url):
            # async code here
            pass
    """
    min_interval = 1.0 / calls_per_second
    last_called = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Use function name as key for tracking
            key = func.__name__
            
            now = time.time()
            if key in last_called:
                elapsed = now - last_called[key]
                if elapsed < min_interval:
                    wait_time = min_interval - elapsed
                    await asyncio.sleep(wait_time)
            
            last_called[key] = time.time()
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    import aiohttp
    
    @retry(max_attempts=3, delay=0.5)
    @rate_limit(calls_per_second=2)
    async def fetch_with_decorators(url: str):
        """Example function with both decorators applied."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    
    async def test_decorators():
        urls = [
            "https://httpbin.org/status/200",
            "https://httpbin.org/delay/1",
        ]
        
        tasks = [fetch_with_decorators(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print(f"Fetched {len(results)} URLs with decorators")
    
    asyncio.run(test_decorators())
