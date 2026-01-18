#!/usr/bin/env python3
"""
Script to run the RSS parser and count jobs from all feeds
This is a standalone script to test the RSS parsing and logging functionality
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logger import get_logger, log_section, log_separator, setup_logging
from feed_config import FeedConfigManager
from rss_parser import RSSParser

# Initialize logging
setup_logging()
logger = get_logger(__name__)


def main():
    """Run the RSS parser and display job counts"""
    try:
        log_section(logger, "RSS FEED JOB COUNT TEST")
        logger.info("Loading RSS feed configuration...")
        
        # Load feeds from config
        feed_manager = FeedConfigManager('rss_feeds.json')
        feeds = feed_manager.load_feeds(prefer_json=True)
        
        if not feeds:
            logger.error("No RSS feeds configured!")
            return
        
        # Get active feeds
        active_feeds = feed_manager.get_active_feeds(respect_priority=True)
        
        logger.info(f"Found {len(feeds)} total feeds, {len(active_feeds)} active feeds")
        logger.info("")
        logger.info("Active Feeds:")
        for idx, feed in enumerate(active_feeds, 1):
            logger.info(f"  {idx}. {feed.name}")
            logger.info(f"     URL: {feed.url}")
            logger.info(f"     Priority: {feed.priority}, Tags: {', '.join(feed.tags) if feed.tags else 'none'}")
        
        log_separator(logger)
        
        # Parse feeds with extended date range to get more jobs
        logger.info("Parsing RSS feeds (looking back 30 days for more results)...")
        rss_parser = RSSParser(active_feeds)
        jobs = rss_parser.parse_feeds(days_back=30)
        
        # Display detailed job list
        if jobs:
            log_section(logger, "ALL JOBS FOUND")
            for idx, job in enumerate(jobs, 1):
                logger.info(f"{idx}. {job['title']}")
                logger.info(f"   Source: {job['source_feed']}")
                logger.info(f"   Link: {job['link']}")
                logger.info(f"   Published: {job['published']}")
                logger.info("")
        else:
            logger.warning("No jobs found in any of the RSS feeds!")
        
        log_section(logger, "FINAL SUMMARY")
        logger.info(f"Total active feeds processed: {len(active_feeds)}")
        logger.info(f"Total jobs found: {len(jobs)}")
        
        # Group by source
        source_counts = {}
        for job in jobs:
            source = job['source_feed']
            source_counts[source] = source_counts.get(source, 0) + 1
        
        logger.info("")
        logger.info("Jobs by source:")
        for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  - {source}: {count} jobs")
        
        log_separator(logger, "=")
        
    except Exception as e:
        logger.error(f"Error running RSS parser: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

