"""
RSS Feed Parser Module
Parses RSS feeds and extracts job posting URLs
"""

import feedparser
from typing import List, Dict
from datetime import datetime, timedelta
from logger import get_logger, log_job_summary, log_section, log_total_summary

logger = get_logger(__name__)


class RSSParser:
    """Parse RSS feeds and extract job posting information"""

    def __init__(self, feeds):
        """
        Initialize RSS parser with feed URLs or RSSFeed objects

        Args:
            feeds: List of RSS feed URLs (strings) or RSSFeed objects to parse
        """
        self.feeds = feeds

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
        feed_stats = {}  # Track jobs per feed

        log_section(logger, "RSS FEED PARSING")
        logger.info(f"Parsing {len(self.feeds)} RSS feeds (looking back {days_back} day(s))")
        logger.info(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("")

        for feed_idx, feed_item in enumerate(self.feeds, 1):
            try:
                # Handle both RSSFeed objects and plain URL strings
                if hasattr(feed_item, 'url'):
                    feed_url = feed_item.url
                    feed_name = getattr(feed_item, 'name', feed_url)
                else:
                    feed_url = feed_item
                    feed_name = feed_url

                logger.info(f"[Feed {feed_idx}/{len(self.feeds)}] Processing: {feed_name}")
                logger.info(f"  URL: {feed_url}")

                feed = feedparser.parse(feed_url)

                if feed.bozo:
                    logger.warning(f"  ⚠ Feed parsing warning: {feed.bozo_exception}")

                feed_job_count = 0
                total_entries = len(feed.entries)
                logger.info(f"  Total entries in feed: {total_entries}")

                for entry_idx, entry in enumerate(feed.entries, 1):
                    job_data = self._extract_job_data(entry, cutoff_date, feed_name)
                    if job_data:
                        all_jobs.append(job_data)
                        feed_job_count += 1
                        logger.info(f"    [{entry_idx}] ✓ Job: {job_data['title'][:60]}{'...' if len(job_data['title']) > 60 else ''}")
                        logger.debug(f"        Link: {job_data['link']}")
                        logger.debug(f"        Published: {job_data['published']}")
                    else:
                        # Log skipped entries at debug level
                        entry_title = entry.get('title', 'No Title')[:40]
                        logger.debug(f"    [{entry_idx}] ✗ Skipped (too old): {entry_title}...")

                feed_stats[feed_name] = {
                    'total_entries': total_entries,
                    'jobs_found': feed_job_count,
                    'url': feed_url
                }

                logger.info(f"  Summary: {feed_job_count} jobs found from {total_entries} entries")
                logger.info("")

            except Exception as e:
                logger.error(f"  ✗ Error parsing feed {feed_name}: {str(e)}")
                feed_stats[feed_name] = {'total_entries': 0, 'jobs_found': 0, 'url': feed_url, 'error': str(e)}
                continue

        # Log final summary
        log_section(logger, "FEED PARSING SUMMARY")
        for feed_name, stats in feed_stats.items():
            if 'error' in stats:
                logger.info(f"  ✗ {feed_name}: ERROR - {stats['error']}")
            else:
                logger.info(f"  ✓ {feed_name}: {stats['jobs_found']} jobs from {stats['total_entries']} entries")

        log_total_summary(logger, len(all_jobs), len(self.feeds))

        return all_jobs

    def _extract_job_data(self, entry, cutoff_date: datetime, feed_name: str = 'Unknown') -> Dict:
        """
        Extract job data from RSS entry

        Args:
            entry: RSS feed entry
            cutoff_date: Only include jobs published after this date
            feed_name: Name of the source feed

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
                'source_feed': feed_name
            }

            return job_data

        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
            return None

