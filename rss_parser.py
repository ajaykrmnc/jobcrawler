"""
RSS Feed Parser Module
Parses RSS feeds and extracts job posting URLs
"""

import feedparser
import logging
from typing import List, Dict
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSParser:
    """Parse RSS feeds and extract job posting information"""

    def __init__(self, feed_urls: List[str]):
        """
        Initialize RSS parser with feed URLs

        Args:
            feed_urls: List of RSS feed URLs to parse
        """
        self.feed_urls = feed_urls

    def parse_feeds(self, days_back: int = 1) -> List[Dict]:
        """
        Parse all RSS feeds and extract job postings

        Args:
            days_back: Number of days to look back for job postings

        Returns:
            List of job posting dictionaries with title, link, published date
        """
        all_jobs = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        for feed_url in self.feed_urls:
            try:
                logger.info(f"Parsing RSS feed: {feed_url}")
                feed = feedparser.parse(feed_url)

                if feed.bozo:
                    logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_exception}")

                for entry in feed.entries:
                    job_data = self._extract_job_data(entry, cutoff_date)
                    if job_data:
                        all_jobs.append(job_data)

                logger.info(f"Found {len(feed.entries)} entries in {feed_url}")

            except Exception as e:
                logger.error(f"Error parsing feed {feed_url}: {str(e)}")
                continue

        logger.info(f"Total jobs found: {len(all_jobs)}")
        return all_jobs

    def _extract_job_data(self, entry, cutoff_date: datetime) -> Dict:
        """
        Extract job data from RSS entry

        Args:
            entry: RSS feed entry
            cutoff_date: Only include jobs published after this date

        Returns:
            Dictionary with job data or None if too old
        """
        try:
            # Extract published date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])

            # Skip if too old
            if published and published < cutoff_date:
                return None

            job_data = {
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', ''),
                'published': published.isoformat() if published else None,
                'summary': entry.get('summary', ''),
                'source_feed': entry.get('source', {}).get('href', 'Unknown')
            }

            return job_data

        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
            return None

