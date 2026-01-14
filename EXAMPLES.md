# RSS Feed Configuration Examples

This document provides practical examples of how to configure and use the extendible RSS feed system.

## Quick Start

### 1. Using JSON Configuration (Recommended)

Edit `rss_feeds.json`:

```json
{
  "feeds": [
    {
      "name": "Google Alerts - Python Jobs",
      "url": "https://www.google.com/alerts/feeds/12345678901234567890/9876543210987654321",
      "enabled": true,
      "priority": 1,
      "tags": ["python", "backend"],
      "description": "Python developer positions"
    },
    {
      "name": "Google Alerts - Remote Work",
      "url": "https://www.google.com/alerts/feeds/12345678901234567890/1111111111111111111",
      "enabled": true,
      "priority": 2,
      "tags": ["remote", "flexible"],
      "description": "Remote job opportunities"
    }
  ],
  "settings": {
    "max_feeds_to_process": 10,
    "respect_priority": true,
    "skip_disabled": true
  }
}
```

Set in `.env`:
```env
USE_JSON_FEEDS=true
```

### 2. Using Environment Variable (Simple)

Set in `.env`:
```env
USE_JSON_FEEDS=false
RSS_FEEDS=https://feed1.xml,https://feed2.xml,https://feed3.xml
```

## Common Scenarios

### Scenario 1: Multiple Job Searches by Technology

```json
{
  "feeds": [
    {
      "name": "Python Developer Jobs",
      "url": "https://www.google.com/alerts/feeds/USER_ID/PYTHON_ALERT",
      "enabled": true,
      "priority": 1,
      "tags": ["python", "backend", "high-priority"]
    },
    {
      "name": "JavaScript Developer Jobs",
      "url": "https://www.google.com/alerts/feeds/USER_ID/JS_ALERT",
      "enabled": true,
      "priority": 2,
      "tags": ["javascript", "frontend"]
    },
    {
      "name": "DevOps Engineer Jobs",
      "url": "https://www.google.com/alerts/feeds/USER_ID/DEVOPS_ALERT",
      "enabled": true,
      "priority": 3,
      "tags": ["devops", "infrastructure"]
    }
  ]
}
```

### Scenario 2: Multiple Locations

```json
{
  "feeds": [
    {
      "name": "Jobs in San Francisco",
      "url": "https://www.google.com/alerts/feeds/USER_ID/SF_ALERT",
      "enabled": true,
      "priority": 1,
      "tags": ["san-francisco", "local"]
    },
    {
      "name": "Jobs in New York",
      "url": "https://www.google.com/alerts/feeds/USER_ID/NY_ALERT",
      "enabled": true,
      "priority": 1,
      "tags": ["new-york", "local"]
    },
    {
      "name": "Remote Jobs Worldwide",
      "url": "https://www.google.com/alerts/feeds/USER_ID/REMOTE_ALERT",
      "enabled": true,
      "priority": 2,
      "tags": ["remote", "worldwide"]
    }
  ]
}
```

### Scenario 3: Different Seniority Levels

```json
{
  "feeds": [
    {
      "name": "Senior Engineer Positions",
      "url": "https://www.google.com/alerts/feeds/USER_ID/SENIOR_ALERT",
      "enabled": true,
      "priority": 1,
      "tags": ["senior", "high-priority"],
      "description": "Senior and lead engineering roles"
    },
    {
      "name": "Mid-Level Positions",
      "url": "https://www.google.com/alerts/feeds/USER_ID/MID_ALERT",
      "enabled": true,
      "priority": 2,
      "tags": ["mid-level"],
      "description": "Mid-level engineering positions"
    },
    {
      "name": "Entry Level Jobs",
      "url": "https://www.google.com/alerts/feeds/USER_ID/ENTRY_ALERT",
      "enabled": false,
      "priority": 3,
      "tags": ["entry-level"],
      "description": "Entry-level positions (disabled for now)"
    }
  ]
}
```

### Scenario 4: Mixed Sources

```json
{
  "feeds": [
    {
      "name": "Google Alerts - Software Engineer",
      "url": "https://www.google.com/alerts/feeds/USER_ID/ALERT_ID",
      "enabled": true,
      "priority": 1,
      "tags": ["google-alerts", "primary"]
    },
    {
      "name": "Indeed RSS - Python Jobs",
      "url": "https://www.indeed.com/rss?q=python+developer&l=remote",
      "enabled": true,
      "priority": 2,
      "tags": ["indeed", "aggregator"]
    },
    {
      "name": "Stack Overflow Jobs",
      "url": "https://stackoverflow.com/jobs/feed?q=python",
      "enabled": false,
      "priority": 3,
      "tags": ["stackoverflow", "tech-focused"],
      "description": "Disabled - testing feed quality"
    }
  ]
}
```

## Using the Management CLI

### List all feeds
```bash
python manage_feeds.py list
```

### Add a new feed interactively
```bash
python manage_feeds.py add
```

Example session:
```
=== Add New RSS Feed ===

Feed name: Google Alerts - React Developer
Feed URL: https://www.google.com/alerts/feeds/12345/67890
Enabled? (y/n) [y]: y
Priority (1-10) [1]: 2
Tags (comma-separated): react, frontend, javascript
Description: React and frontend developer positions

✅ Feed 'Google Alerts - React Developer' added successfully!
```

### Enable/disable a feed
```bash
python manage_feeds.py toggle
```

### Test feed connectivity
```bash
python manage_feeds.py test
```

Output:
```
=== Testing 3 Active Feeds ===

1. Testing: Google Alerts - Python Jobs
   URL: https://www.google.com/alerts/feeds/...
   ✅ Success: 15 entries found
   Latest: Senior Python Developer - Remote - $150k-$200k...

2. Testing: Google Alerts - Remote Work
   URL: https://www.google.com/alerts/feeds/...
   ✅ Success: 23 entries found
   Latest: Remote Software Engineer - Full Stack...
```

## Programmatic Usage

### Using FeedConfigManager in Python

```python
from feed_config import FeedConfigManager, RSSFeed

# Load feeds
manager = FeedConfigManager('rss_feeds.json')
manager.load_feeds(prefer_json=True)

# Get active feeds
active_feeds = manager.get_active_feeds(respect_priority=True)
print(f"Found {len(active_feeds)} active feeds")

# Get feeds by tag
python_feeds = manager.get_feeds_by_tag('python')
print(f"Found {len(python_feeds)} Python-related feeds")

# Add a new feed programmatically
new_feed = RSSFeed(
    name="New Job Feed",
    url="https://example.com/feed.xml",
    enabled=True,
    priority=5,
    tags=["example", "test"],
    description="Example feed"
)
manager.add_feed(new_feed)
manager.save_to_json()
```

### Using with RSSParser

```python
from feed_config import FeedConfigManager
from rss_parser import RSSParser

# Load feeds
manager = FeedConfigManager()
manager.load_feeds()
active_feeds = manager.get_active_feeds()

# Parse feeds
parser = RSSParser(active_feeds)
jobs = parser.parse_feeds(days_back=1)

print(f"Found {len(jobs)} jobs from {len(active_feeds)} feeds")
```

## Best Practices

1. **Start with high-priority feeds**: Set priority=1 for your most important job searches
2. **Use descriptive names**: Make it clear what each feed is for
3. **Tag consistently**: Use consistent tag names across feeds
4. **Disable, don't delete**: Keep feeds for future reference by setting `enabled: false`
5. **Test before deploying**: Use `python manage_feeds.py test` to verify feeds work
6. **Document your feeds**: Use the description field to explain each feed's purpose

## Migration from Environment Variable

If you're currently using `RSS_FEEDS` environment variable, here's how to migrate:

1. Run the system once to see which feeds you have:
   ```bash
   python test_setup.py
   ```

2. Create `rss_feeds.json` with your feeds:
   ```json
   {
     "feeds": [
       {
         "name": "Feed 1",
         "url": "YOUR_FIRST_FEED_URL",
         "enabled": true,
         "priority": 1
       },
       {
         "name": "Feed 2",
         "url": "YOUR_SECOND_FEED_URL",
         "enabled": true,
         "priority": 2
       }
     ]
   }
   ```

3. Update `.env`:
   ```env
   USE_JSON_FEEDS=true
   ```

4. Test the new configuration:
   ```bash
   python manage_feeds.py test
   ```

5. Run the system:
   ```bash
   python main.py
   ```

