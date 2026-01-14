"""
Test Setup Script
Verifies that all components are configured correctly
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    print("Testing environment configuration...")
    load_dotenv()
    
    required_vars = [
        'GEMINI_API_KEY',
        'SMTP_USERNAME',
        'SMTP_PASSWORD',
        'EMAIL_TO',
        'RSS_FEEDS'
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            print(f"  ❌ {var}: Not set")
        else:
            # Show partial value for security
            if 'PASSWORD' in var or 'KEY' in var:
                display = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
            else:
                display = value[:50] + '...' if len(value) > 50 else value
            print(f"  ✅ {var}: {display}")
    
    if missing:
        print(f"\n❌ Missing required variables: {', '.join(missing)}")
        return False
    
    print("\n✅ All required environment variables are set!")
    return True


def test_imports():
    """Test that all required packages are installed"""
    print("\nTesting package imports...")
    
    packages = [
        ('feedparser', 'feedparser'),
        ('readability', 'readability-lxml'),
        ('requests', 'requests'),
        ('google.generativeai', 'google-generativeai'),
        ('dotenv', 'python-dotenv'),
        ('lxml', 'lxml'),
        ('bs4', 'beautifulsoup4')
    ]
    
    missing = []
    for module, package in packages:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All required packages are installed!")
    return True


def test_rss_feeds():
    """Test RSS feed connectivity"""
    print("\nTesting RSS feeds...")
    load_dotenv()

    # Try to load feeds using FeedConfigManager
    try:
        from feed_config import FeedConfigManager

        use_json = os.getenv('USE_JSON_FEEDS', 'true').lower() == 'true'

        if use_json:
            print("  Using JSON configuration (rss_feeds.json)")
            manager = FeedConfigManager('rss_feeds.json')
            manager.load_feeds(prefer_json=True)
            feeds = manager.get_active_feeds()

            if not feeds:
                print("  ⚠️  No active feeds in rss_feeds.json, trying environment variable...")
                # Fall back to environment variable
                feed_urls = os.getenv('RSS_FEEDS', '').split(',')
                feed_urls = [f.strip() for f in feed_urls if f.strip()]
                if not feed_urls:
                    print("  ❌ No RSS feeds configured")
                    return False
                feeds = feed_urls
            else:
                print(f"  Found {len(feeds)} active feed(s) in JSON config")
                for feed in feeds[:3]:
                    print(f"    - {feed.name} (Priority: {feed.priority})")
        else:
            print("  Using environment variable (RSS_FEEDS)")
            feed_urls = os.getenv('RSS_FEEDS', '').split(',')
            feeds = [f.strip() for f in feed_urls if f.strip()]

            if not feeds:
                print("  ❌ No RSS feeds configured")
                return False

            print(f"  Found {len(feeds)} RSS feed(s)")
    except ImportError:
        # Fall back to simple environment variable method
        print("  Using environment variable (RSS_FEEDS)")
        feed_urls = os.getenv('RSS_FEEDS', '').split(',')
        feeds = [f.strip() for f in feed_urls if f.strip()]

        if not feeds:
            print("  ❌ No RSS feeds configured")
            return False

        print(f"  Found {len(feeds)} RSS feed(s)")

    # Test feed connectivity
    try:
        import feedparser
        test_count = min(3, len(feeds))
        print(f"\n  Testing first {test_count} feed(s)...")

        for i in range(test_count):
            feed_item = feeds[i]

            # Handle both RSSFeed objects and URL strings
            if hasattr(feed_item, 'url'):
                feed_url = feed_item.url
                feed_name = feed_item.name
            else:
                feed_url = feed_item
                feed_name = f"Feed {i+1}"

            print(f"\n  {i+1}. {feed_name}")
            print(f"     URL: {feed_url[:60]}...")

            parsed = feedparser.parse(feed_url)

            if parsed.bozo:
                print(f"     ⚠️  Warning: {str(parsed.bozo_exception)[:50]}")

            if parsed.entries:
                print(f"     ✅ {len(parsed.entries)} entries found")
            else:
                print(f"     ⚠️  No entries found (feed might be empty)")

    except Exception as e:
        print(f"  ❌ Error testing feeds: {str(e)}")
        return False

    print("\n✅ RSS feeds are accessible!")
    return True


def test_gemini_api():
    """Test Gemini API connectivity"""
    print("\nTesting Gemini API...")
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("  ❌ GEMINI_API_KEY not set")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Simple test
        response = model.generate_content("Say 'API test successful' if you can read this.")
        print(f"  ✅ API Response: {response.text[:50]}...")
        print("\n✅ Gemini API is working!")
        return True
    except Exception as e:
        print(f"  ❌ Error testing Gemini API: {str(e)}")
        return False


def test_smtp():
    """Test SMTP connectivity"""
    print("\nTesting SMTP connection...")
    load_dotenv()
    
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    username = os.getenv('SMTP_USERNAME')
    password = os.getenv('SMTP_PASSWORD')
    
    if not username or not password:
        print("  ❌ SMTP credentials not set")
        return False
    
    try:
        import smtplib
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(username, password)
        print(f"  ✅ Connected to {smtp_server}:{smtp_port}")
        print("\n✅ SMTP authentication successful!")
        return True
    except Exception as e:
        print(f"  ❌ Error testing SMTP: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Job Automation System - Setup Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Environment Variables", test_environment),
        ("Package Imports", test_imports),
        ("RSS Feeds", test_rss_feeds),
        ("Gemini API", test_gemini_api),
        ("SMTP Connection", test_smtp)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {str(e)}")
            results.append((name, False))
        print()
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("🎉 All tests passed! Your system is ready to run.")
        print("\nRun the automation with: python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nRefer to QUICKSTART.md for setup instructions.")
    
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

