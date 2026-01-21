# Lab 5: Async Web Scraper with asyncio Fundamentals

A high-performance web scraper that uses Python's asyncio for concurrent HTTP requests. This project demonstrates async/await patterns, task coordination, and performance comparison between async, threaded, and sequential approaches.

## Features

- **Async HTTP Requests**: Concurrent fetching using `aiohttp` and `asyncio.gather()`
- **Smart Retry Logic**: Automatic retry with exponential backoff for failed requests
- **Rate Limiting**: Configurable rate limiter to respect server limits
- **Async Generators**: Memory-efficient response processing
- **Data Extraction**: Regex-based content extraction
- **Performance Benchmarks**: Compare async vs threaded vs sequential execution

## Project Structure

```
async-web-scraper/
├── scraper/
│   ├── __init__.py
│   ├── fetcher.py          # Async HTTP client
│   ├── decorators.py       # Retry and rate-limit decorators
│   ├── async_generator.py  # Async response processing
│   ├── extractor.py        # Data extraction with regex
│   ├── sequential.py       # Sequential implementation
│   └── threaded.py         # Threaded implementation
├── tests/
│   └── test_scraper.py
├── output/
│   └── results.json
├── urls.txt
├── benchmark.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run async scraper
python -m scraper.fetcher

# Run performance benchmark
python benchmark.py
```

## Asyncio Concepts

### Event Loop
The event loop is the core of asyncio, managing and distributing tasks:
```python
import asyncio

async def main():
    # Your async code here
    pass

# Run the event loop
asyncio.run(main())
```

### Coroutines
Functions defined with `async def` that can be paused and resumed:
```python
async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### Concurrent Execution
Use `asyncio.gather()` to run multiple coroutines concurrently:
```python
results = await asyncio.gather(
    fetch_url(url1),
    fetch_url(url2),
    fetch_url(url3)
)
```

## Performance Comparison

Performance results will be documented here after benchmarking.

## Development

This lab was developed following a structured Git workflow:
- Feature branches for each phase
- Pull requests to `development` branch
- Final release PR to `main` branch

## Author

Lab 5 - Python Advanced Course
