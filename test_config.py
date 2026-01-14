#!/usr/bin/env python3
"""
Test script to validate configuration files
"""

import json
import os
from user_config import UserConfigManager
from feed_config import FeedConfigManager


def test_user_profile():
    """Test user profile configuration"""
    print("\n" + "="*60)
    print("Testing User Profile Configuration")
    print("="*60)
    
    manager = UserConfigManager('user_profile.json')
    
    if manager.load_from_json():
        print("✅ Successfully loaded user_profile.json")
        print(f"\nProfile Details:")
        print(f"  Name: {manager.profile.name}")
        print(f"  Skills: {', '.join(manager.profile.skills[:5])}{'...' if len(manager.profile.skills) > 5 else ''}")
        print(f"  Experience: {manager.profile.experience_years} years")
        print(f"  Locations: {', '.join(manager.profile.preferred_locations)}")
        print(f"  Job Titles: {', '.join(manager.profile.job_titles)}")
        
        if manager.preferences:
            print(f"\nPreferences:")
            print(f"  Company Size: {', '.join(manager.preferences.company_size)}")
            print(f"  Industries: {', '.join(manager.preferences.industries)}")
            print(f"  Avoid Keywords: {', '.join(manager.preferences.avoid_keywords)}")
        
        if manager.settings:
            print(f"\nSettings:")
            print(f"  Min Match Score: {manager.settings.get('min_match_score', 60)}")
            print(f"  Max Jobs to Analyze: {manager.settings.get('max_jobs_to_analyze', 20)}")
            print(f"  Days Back: {manager.settings.get('days_back', 1)}")
        
        return True
    else:
        print("❌ Failed to load user_profile.json")
        return False


def test_rss_feeds():
    """Test RSS feeds configuration"""
    print("\n" + "="*60)
    print("Testing RSS Feeds Configuration")
    print("="*60)
    
    manager = FeedConfigManager('rss_feeds.json')
    
    if manager.load_from_json():
        print("✅ Successfully loaded rss_feeds.json")
        print(f"\nTotal Feeds: {len(manager.feeds)}")
        
        active_feeds = manager.get_active_feeds()
        print(f"Active Feeds: {len(active_feeds)}")
        
        print(f"\nFeed Details:")
        for feed in manager.feeds[:5]:
            status = "✓" if feed.enabled else "✗"
            print(f"  [{status}] {feed.name} (Priority: {feed.priority})")
            print(f"      Tags: {', '.join(feed.tags) if feed.tags else 'none'}")
        
        if len(manager.feeds) > 5:
            print(f"  ... and {len(manager.feeds) - 5} more")
        
        return True
    else:
        print("❌ Failed to load rss_feeds.json")
        return False


def test_json_validity():
    """Test JSON file validity"""
    print("\n" + "="*60)
    print("Testing JSON File Validity")
    print("="*60)
    
    files = ['user_profile.json', 'rss_feeds.json']
    all_valid = True
    
    for filename in files:
        try:
            with open(filename, 'r') as f:
                json.load(f)
            print(f"✅ {filename} is valid JSON")
        except FileNotFoundError:
            print(f"⚠️  {filename} not found")
            all_valid = False
        except json.JSONDecodeError as e:
            print(f"❌ {filename} has invalid JSON: {e}")
            all_valid = False
    
    return all_valid


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Configuration Test Suite")
    print("="*60)
    
    results = []
    
    # Test JSON validity
    results.append(("JSON Validity", test_json_validity()))
    
    # Test user profile
    results.append(("User Profile", test_user_profile()))
    
    # Test RSS feeds
    results.append(("RSS Feeds", test_rss_feeds()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Configuration is valid.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the configuration files.")
        return 1


if __name__ == "__main__":
    exit(main())

