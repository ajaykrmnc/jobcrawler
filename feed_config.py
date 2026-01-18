"""
RSS Feed Configuration Manager
Handles loading and managing RSS feed configurations from multiple sources
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from logger import get_logger

logger = get_logger(__name__)


@dataclass
class RSSFeed:
    """Represents a single RSS feed configuration"""
    name: str
    url: str
    enabled: bool = True
    priority: int = 1
    tags: List[str] = field(default_factory=list)
    description: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'url': self.url,
            'enabled': self.enabled,
            'priority': self.priority,
            'tags': self.tags,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RSSFeed':
        """Create from dictionary"""
        return cls(
            name=data.get('name', 'Unnamed Feed'),
            url=data['url'],
            enabled=data.get('enabled', True),
            priority=data.get('priority', 1),
            tags=data.get('tags', []),
            description=data.get('description', '')
        )


class FeedConfigManager:
    """Manages RSS feed configurations from multiple sources"""
    
    def __init__(self, config_file: str = 'rss_feeds.json'):
        """
        Initialize feed configuration manager
        
        Args:
            config_file: Path to JSON configuration file
        """
        self.config_file = config_file
        self.feeds: List[RSSFeed] = []
        self.settings: Dict = {}
    
    def load_from_json(self) -> bool:
        """
        Load feeds from JSON configuration file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.config_file):
                logger.warning(f"Config file {self.config_file} not found")
                return False
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            self.settings = config.get('settings', {})
            
            for feed_data in config.get('feeds', []):
                try:
                    feed = RSSFeed.from_dict(feed_data)
                    self.feeds.append(feed)
                except Exception as e:
                    logger.error(f"Error loading feed {feed_data.get('name', 'unknown')}: {e}")
            
            logger.info(f"Loaded {len(self.feeds)} feeds from {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return False
    
    def load_from_env(self, env_var: str = 'RSS_FEEDS') -> bool:
        """
        Load feeds from environment variable (comma-separated URLs)
        
        Args:
            env_var: Name of environment variable
            
        Returns:
            True if successful, False otherwise
        """
        try:
            feeds_str = os.getenv(env_var, '')
            if not feeds_str:
                logger.warning(f"Environment variable {env_var} not set")
                return False
            
            urls = [url.strip() for url in feeds_str.split(',') if url.strip()]
            
            for i, url in enumerate(urls, 1):
                feed = RSSFeed(
                    name=f"Feed {i}",
                    url=url,
                    enabled=True,
                    priority=i
                )
                self.feeds.append(feed)
            
            logger.info(f"Loaded {len(urls)} feeds from environment variable")
            return True
            
        except Exception as e:
            logger.error(f"Error loading from environment: {e}")
            return False
    
    def load_feeds(self, prefer_json: bool = True) -> List[RSSFeed]:
        """
        Load feeds from available sources
        
        Args:
            prefer_json: If True, try JSON file first, then fall back to env var
            
        Returns:
            List of RSSFeed objects
        """
        self.feeds = []
        
        if prefer_json:
            # Try JSON first
            if self.load_from_json():
                logger.info("Using feeds from JSON configuration")
            else:
                # Fall back to environment variable
                logger.info("Falling back to environment variable configuration")
                self.load_from_env()
        else:
            # Try environment variable first
            if self.load_from_env():
                logger.info("Using feeds from environment variable")
            else:
                # Fall back to JSON
                logger.info("Falling back to JSON configuration")
                self.load_from_json()
        
        return self.feeds
    
    def get_active_feeds(self, respect_priority: bool = True) -> List[RSSFeed]:
        """
        Get list of active (enabled) feeds
        
        Args:
            respect_priority: If True, sort by priority
            
        Returns:
            List of active RSSFeed objects
        """
        active_feeds = [f for f in self.feeds if f.enabled]
        
        if respect_priority:
            active_feeds.sort(key=lambda f: f.priority)
        
        return active_feeds
    
    def get_feed_urls(self, only_enabled: bool = True) -> List[str]:
        """
        Get list of feed URLs
        
        Args:
            only_enabled: If True, only return enabled feeds
            
        Returns:
            List of feed URLs
        """
        if only_enabled:
            return [f.url for f in self.feeds if f.enabled]
        return [f.url for f in self.feeds]
    
    def get_feeds_by_tag(self, tag: str) -> List[RSSFeed]:
        """
        Get feeds filtered by tag
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of RSSFeed objects with the specified tag
        """
        return [f for f in self.feeds if tag in f.tags and f.enabled]
    
    def add_feed(self, feed: RSSFeed) -> None:
        """Add a new feed to the configuration"""
        self.feeds.append(feed)
    
    def save_to_json(self) -> bool:
        """
        Save current feeds to JSON file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            config = {
                'feeds': [f.to_dict() for f in self.feeds],
                'settings': self.settings
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Saved {len(self.feeds)} feeds to {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving config file: {e}")
            return False

