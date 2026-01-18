"""
Main Job Automation Script
Orchestrates RSS parsing, content extraction, job analysis, and email notifications
"""

import os
import sys
from dotenv import load_dotenv
from rss_parser import RSSParser
from content_extractor import ContentExtractor
from job_analyzer import JobAnalyzer
from email_sender import EmailSender
from feed_config import FeedConfigManager
from user_config import UserConfigManager
from logger import get_logger, log_section, log_separator

logger = get_logger(__name__)


def load_config():
    """Load configuration from environment variables and JSON config files"""
    load_dotenv()

    config = {
        'gemini_api_key': os.getenv('GEMINI_API_KEY'),
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'smtp_username': os.getenv('SMTP_USERNAME'),
        'smtp_password': os.getenv('SMTP_PASSWORD'),
        'email_to': os.getenv('EMAIL_TO')
    }

    # Load RSS feeds using FeedConfigManager
    feed_manager = FeedConfigManager('rss_feeds.json')

    # Try to load from JSON first, fall back to environment variable
    prefer_json = os.getenv('USE_JSON_FEEDS', 'true').lower() == 'true'
    feeds = feed_manager.load_feeds(prefer_json=prefer_json)

    if not feeds:
        raise ValueError("No RSS feeds configured. Please configure feeds in rss_feeds.json or set RSS_FEEDS in .env file")

    # Get active feeds
    active_feeds = feed_manager.get_active_feeds(respect_priority=True)
    config['rss_feeds'] = active_feeds
    config['feed_manager'] = feed_manager

    # Load user profile using UserConfigManager
    user_manager = UserConfigManager('user_profile.json')

    # Try to load from JSON first, fall back to environment variables
    prefer_json_profile = os.getenv('USE_JSON_PROFILE', 'true').lower() == 'true'

    if prefer_json_profile:
        if not user_manager.load_from_json():
            logger.warning("Failed to load user profile from JSON, falling back to environment variables")
            user_manager.load_from_env()
    else:
        if not user_manager.load_from_env():
            logger.warning("Failed to load user profile from environment, falling back to JSON")
            user_manager.load_from_json()

    if not user_manager.profile:
        raise ValueError("No user profile configured. Please configure user_profile.json or set YOUR_SKILLS, YOUR_EXPERIENCE_YEARS, etc. in .env file")

    config['user_profile'] = user_manager.profile.to_dict()
    config['user_preferences'] = user_manager.preferences
    config['user_settings'] = user_manager.settings
    config['user_manager'] = user_manager

    # Validate required fields
    required_fields = ['gemini_api_key', 'smtp_username', 'smtp_password', 'email_to']
    missing_fields = [field for field in required_fields if not config.get(field)]

    if missing_fields:
        raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")

    return config


def main():
    """Main execution function"""
    try:
        logger.info("=" * 60)
        logger.info("Starting Job Automation System")
        logger.info("=" * 60)
        
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        logger.info(f"Configured {len(config['rss_feeds'])} RSS feeds")

        # Log feed details
        for feed in config['rss_feeds']:
            logger.info(f"  - {feed.name} (Priority: {feed.priority}, Tags: {', '.join(feed.tags) if feed.tags else 'none'})")

        # Log user profile details
        user_profile = config['user_manager'].profile
        logger.info(f"\nUser Profile:")
        logger.info(f"  Skills: {', '.join(user_profile.skills[:5])}{'...' if len(user_profile.skills) > 5 else ''}")
        logger.info(f"  Experience: {user_profile.experience_years} years")
        logger.info(f"  Locations: {', '.join(user_profile.preferred_locations)}")

        # Get settings from user profile
        days_back = config['user_settings'].get('days_back', 1)
        max_jobs = config['user_settings'].get('max_jobs_to_analyze', 20)

        # Step 1: Parse RSS feeds
        logger.info("\nStep 1: Parsing RSS feeds...")
        rss_parser = RSSParser(config['rss_feeds'])
        jobs = rss_parser.parse_feeds(days_back=days_back)
        
        if not jobs:
            logger.warning("No jobs found in RSS feeds")
            # Still send email with empty results
            email_sender = EmailSender(
                config['smtp_server'],
                config['smtp_port'],
                config['smtp_username'],
                config['smtp_password']
            )
            email_sender.send_job_report(config['email_to'], [], 0)
            return
        
        logger.info(f"Found {len(jobs)} job postings")
        
        # Step 2: Extract content from job postings
        logger.info("\nStep 2: Extracting content from job postings...")
        content_extractor = ContentExtractor(timeout=15)

        job_contents = []
        for job in jobs[:max_jobs]:  # Limit based on user settings
            content = content_extractor.extract_content(job['link'])
            if content:
                job_contents.append(content)
        
        logger.info(f"Successfully extracted content from {len(job_contents)} job postings")
        
        if not job_contents:
            logger.warning("No content could be extracted from job postings")
            return
        
        # Step 3: Analyze jobs with Gemini API
        logger.info("\nStep 3: Analyzing jobs with Gemini API...")
        job_analyzer = JobAnalyzer(config['gemini_api_key'], config['user_profile'])
        analyses = job_analyzer.analyze_multiple_jobs(job_contents)
        
        logger.info(f"Analyzed {len(analyses)} jobs")
        suitable_jobs = [a for a in analyses if a.get('suitable', False)]
        logger.info(f"Found {len(suitable_jobs)} suitable jobs")
        
        # Step 4: Send email report
        logger.info("\nStep 4: Sending email report...")
        email_sender = EmailSender(
            config['smtp_server'],
            config['smtp_port'],
            config['smtp_username'],
            config['smtp_password']
        )
        
        success = email_sender.send_job_report(
            config['email_to'],
            analyses,
            len(jobs)
        )
        
        if success:
            logger.info("Email report sent successfully!")
        else:
            logger.error("Failed to send email report")
        
        logger.info("=" * 60)
        logger.info("Job Automation System completed successfully")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Fatal error in main execution: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

