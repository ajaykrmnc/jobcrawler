#!/usr/bin/env python3
"""
RSS Feed Management Utility
Helps manage RSS feeds in rss_feeds.json
"""

import sys
import json
from feed_config import FeedConfigManager, RSSFeed


def list_feeds():
    """List all configured feeds"""
    manager = FeedConfigManager()
    manager.load_from_json()
    
    if not manager.feeds:
        print("No feeds configured.")
        return
    
    print(f"\n{'='*80}")
    print(f"{'RSS FEEDS CONFIGURATION':^80}")
    print(f"{'='*80}\n")
    
    for i, feed in enumerate(manager.feeds, 1):
        status = "✅ ENABLED" if feed.enabled else "❌ DISABLED"
        print(f"{i}. {feed.name}")
        print(f"   Status: {status}")
        print(f"   URL: {feed.url}")
        print(f"   Priority: {feed.priority}")
        print(f"   Tags: {', '.join(feed.tags) if feed.tags else 'none'}")
        print(f"   Description: {feed.description or 'N/A'}")
        print()
    
    print(f"Total feeds: {len(manager.feeds)}")
    print(f"Active feeds: {len(manager.get_active_feeds())}")
    print()


def add_feed():
    """Add a new feed interactively"""
    manager = FeedConfigManager()
    manager.load_from_json()
    
    print("\n=== Add New RSS Feed ===\n")
    
    name = input("Feed name: ").strip()
    url = input("Feed URL: ").strip()
    
    if not name or not url:
        print("Error: Name and URL are required.")
        return
    
    enabled = input("Enabled? (y/n) [y]: ").strip().lower() or 'y'
    priority = input("Priority (1-10) [1]: ").strip() or '1'
    tags = input("Tags (comma-separated): ").strip()
    description = input("Description: ").strip()
    
    feed = RSSFeed(
        name=name,
        url=url,
        enabled=enabled == 'y',
        priority=int(priority),
        tags=[t.strip() for t in tags.split(',') if t.strip()],
        description=description
    )
    
    manager.add_feed(feed)
    
    if manager.save_to_json():
        print(f"\n✅ Feed '{name}' added successfully!")
    else:
        print("\n❌ Error saving feed.")


def toggle_feed():
    """Enable/disable a feed"""
    manager = FeedConfigManager()
    manager.load_from_json()
    
    if not manager.feeds:
        print("No feeds configured.")
        return
    
    list_feeds()
    
    try:
        index = int(input("Enter feed number to toggle: ")) - 1
        if 0 <= index < len(manager.feeds):
            feed = manager.feeds[index]
            feed.enabled = not feed.enabled
            status = "enabled" if feed.enabled else "disabled"
            
            if manager.save_to_json():
                print(f"\n✅ Feed '{feed.name}' {status}!")
            else:
                print("\n❌ Error saving changes.")
        else:
            print("Invalid feed number.")
    except ValueError:
        print("Invalid input.")


def test_feeds():
    """Test RSS feed connectivity"""
    import feedparser
    
    manager = FeedConfigManager()
    manager.load_from_json()
    
    active_feeds = manager.get_active_feeds()
    
    if not active_feeds:
        print("No active feeds to test.")
        return
    
    print(f"\n=== Testing {len(active_feeds)} Active Feeds ===\n")
    
    for i, feed in enumerate(active_feeds, 1):
        print(f"{i}. Testing: {feed.name}")
        print(f"   URL: {feed.url}")
        
        try:
            parsed = feedparser.parse(feed.url)
            
            if parsed.bozo:
                print(f"   ⚠️  Warning: {parsed.bozo_exception}")
            
            if parsed.entries:
                print(f"   ✅ Success: {len(parsed.entries)} entries found")
                if parsed.entries:
                    print(f"   Latest: {parsed.entries[0].get('title', 'No title')[:60]}...")
            else:
                print(f"   ⚠️  No entries found (feed might be empty)")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print()


def main():
    """Main menu"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'list':
            list_feeds()
        elif command == 'add':
            add_feed()
        elif command == 'toggle':
            toggle_feed()
        elif command == 'test':
            test_feeds()
        else:
            print(f"Unknown command: {command}")
            show_help()
    else:
        show_help()


def show_help():
    """Show help message"""
    print("""
RSS Feed Management Utility

Usage:
    python manage_feeds.py <command>

Commands:
    list    - List all configured feeds
    add     - Add a new feed interactively
    toggle  - Enable/disable a feed
    test    - Test connectivity of active feeds

Examples:
    python manage_feeds.py list
    python manage_feeds.py add
    python manage_feeds.py test
""")


if __name__ == "__main__":
    main()

