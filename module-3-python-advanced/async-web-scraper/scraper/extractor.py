"""
Data Extractor Module

Provides regex-based extraction of structured data from HTML content.
"""

import re
from typing import List, Dict, Any
from functools import reduce


def extract_titles(html: str) -> List[str]:
    """
    Extract all HTML title tags from content.
    
    Args:
        html: HTML content as string
        
    Returns:
        List of title texts
    """
    pattern = r'<title>(.*?)</title>'
    matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
    return [title.strip() for title in matches]


def extract_links(html: str) -> List[str]:
    """
    Extract all href links from HTML content.
    
    Args:
        html: HTML content as string
        
    Returns:
        List of URLs
    """
    pattern = r'<a[^>]+href=["\']([^"\']+)["\']'
    matches = re.findall(pattern, html, re.IGNORECASE)
    return matches


def extract_headers(html: str) -> Dict[str, List[str]]:
    """
    Extract all header tags (h1-h6) from HTML content.
    
    Args:
        html: HTML content as string
        
    Returns:
        Dict mapping header level to list of header texts
    """
    headers = {}
    for level in range(1, 7):
        pattern = f'<h{level}[^>]*>(.*?)</h{level}>'
        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
        if matches:
            headers[f'h{level}'] = [h.strip() for h in matches]
    return headers


def extract_json_data(html: str) -> List[Dict[str, Any]]:
    """
    Extract JSON data from HTML content (e.g., from API responses).
    
    Args:
        html: HTML/text content
        
    Returns:
        List of extracted JSON-like data
    """
    import json
    
    # Try to parse the entire content as JSON
    try:
        data = json.loads(html)
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            return [{"data": data}]
    except json.JSONDecodeError:
        # Not JSON, try to find JSON blocks in HTML
        json_pattern = r'\{[^{}]*\}'
        matches = re.findall(json_pattern, html)
        
        parsed_jsons = []
        for match in matches:
            try:
                parsed = json.loads(match)
                parsed_jsons.append(parsed)
            except json.JSONDecodeError:
                continue
        
        return parsed_jsons


def process_extraction_results(results: List[tuple]) -> Dict[str, Any]:
    """
    Process extraction results using functional programming patterns.
    
    Args:
        results: List of (url, content) tuples
        
    Returns:
        Processed data dictionary
    """
    # Filter out empty results
    valid_results = list(filter(lambda x: x[1] != "", results))
    
    # Map to extract data from each result
    extracted_data = list(map(
        lambda x: {
            'url': x[0],
            'titles': extract_titles(x[1]),
            'links': extract_links(x[1]),
            'headers': extract_headers(x[1]),
            'content_length': len(x[1])
        },
        valid_results
    ))
    
    # Reduce to calculate summary statistics
    summary = reduce(
        lambda acc, item: {
            'total_urls': acc['total_urls'] + 1,
            'total_links': acc['total_links'] + len(item['links']),
            'total_content': acc['total_content'] + item['content_length']
        },
        extracted_data,
        {'total_urls': 0, 'total_links': 0, 'total_content': 0}
    )
    
    return {
        'summary': summary,
        'data': extracted_data
    }


# Example usage
if __name__ == "__main__":
    sample_html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Welcome</h1>
            <h2>Section 1</h2>
            <a href="https://example.com">Link 1</a>
            <a href="https://test.com">Link 2</a>
        </body>
    </html>
    """
    
    print("Titles:", extract_titles(sample_html))
    print("Links:", extract_links(sample_html))
    print("Headers:", extract_headers(sample_html))
