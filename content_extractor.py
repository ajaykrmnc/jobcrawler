"""
Content Extractor Module
Uses readability-lxml to extract clean content from job posting pages
"""

import requests
from readability import Document
from typing import Optional
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger(__name__)


class ContentExtractor:
    """Extract clean content from web pages using readability"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize content extractor
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract_content(self, url: str) -> Optional[dict]:
        """
        Extract clean content from a URL
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dictionary with title and content, or None if extraction fails
        """
        try:
            logger.info(f"Extracting content from: {url}")
            
            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Use readability to extract main content
            doc = Document(response.content)
            
            # Get clean HTML
            clean_html = doc.summary()
            
            # Convert to plain text
            soup = BeautifulSoup(clean_html, 'lxml')
            text_content = soup.get_text(separator='\n', strip=True)
            
            # Clean up extra whitespace
            text_content = '\n'.join(line.strip() for line in text_content.split('\n') if line.strip())
            
            result = {
                'title': doc.title(),
                'content': text_content,
                'url': url
            }
            
            logger.info(f"Successfully extracted content from {url}")
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while fetching {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return None
    
    def extract_multiple(self, urls: list) -> list:
        """
        Extract content from multiple URLs
        
        Args:
            urls: List of URLs to extract content from
            
        Returns:
            List of extracted content dictionaries
        """
        results = []
        for url in urls:
            content = self.extract_content(url)
            if content:
                results.append(content)
        
        logger.info(f"Successfully extracted {len(results)} out of {len(urls)} pages")
        return results

