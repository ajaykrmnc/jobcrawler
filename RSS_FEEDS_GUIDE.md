# RSS Feeds Configuration Guide

This guide explains how to configure and manage multiple RSS feeds for the job automation system.

## Overview

The system supports two methods for configuring RSS feeds:

1. **JSON Configuration File** (Recommended) - `rss_feeds.json`
2. **Environment Variable** (Simple) - `RSS_FEEDS` in `.env`

## Method 1: JSON Configuration (Recommended)

### Why Use JSON Configuration?

- ✅ Support for multiple feeds with metadata
- ✅ Enable/disable feeds without deleting them
- ✅ Set priorities for feed processing
- ✅ Tag feeds for organization
- ✅ Add descriptions for documentation
- ✅ Easy to manage and version control

### Configuration File Structure

The `rss_feeds.json` file has the following structure:

```json
{
  "feeds": [
    {
      "name": "Google Alerts - Software Engineer",
      "url": "https://www.google.com/alerts/feeds/YOUR_USER_ID/YOUR_ALERT_ID",
      "enabled": true,
      "priority": 1,
      "tags": ["software-engineer", "general"],
      "description": "General software engineering jobs"
    }
  ],
  "settings": {
    "max_feeds_to_process": 10,
    "respect_priority": true,
    "skip_disabled": true
  }
}
```

### Feed Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Human-readable name for the feed |
| `url` | string | Yes | RSS feed URL |
| `enabled` | boolean | No | Whether to process this feed (default: true) |
| `priority` | integer | No | Processing priority, lower = higher priority (default: 1) |
| `tags` | array | No | Tags for categorization (default: []) |
| `description` | string | No | Description of the feed (default: "") |

### Settings

| Setting | Type | Description |
|---------|------|-------------|
| `max_feeds_to_process` | integer | Maximum number of feeds to process |
| `respect_priority` | boolean | Whether to sort feeds by priority |
| `skip_disabled` | boolean | Whether to skip disabled feeds |

## Method 2: Environment Variable (Simple)

For simple setups with just a few feeds, you can use the `RSS_FEEDS` environment variable:

```env
RSS_FEEDS=https://feed1.xml,https://feed2.xml,https://feed3.xml
```

This is a comma-separated list of RSS feed URLs.

## Switching Between Methods

Set the `USE_JSON_FEEDS` environment variable in your `.env` file:

```env
# Use JSON configuration (recommended)
USE_JSON_FEEDS=true

# Use environment variable
USE_JSON_FEEDS=false
```

## Managing Feeds with the CLI Tool

The `manage_feeds.py` script provides a convenient way to manage your RSS feeds.

### List All Feeds

```bash
python manage_feeds.py list
```

Output:
```
================================================================================
                          RSS FEEDS CONFIGURATION
================================================================================

1. Google Alerts - Software Engineer
   Status: ✅ ENABLED
   URL: https://www.google.com/alerts/feeds/...
   Priority: 1
   Tags: software-engineer, general
   Description: General software engineering jobs

Total feeds: 3
Active feeds: 2
```

### Add a New Feed

```bash
python manage_feeds.py add
```

Follow the interactive prompts to add a new feed.

### Enable/Disable a Feed

```bash
python manage_feeds.py toggle
```

Select a feed number to toggle its enabled status.

### Test Feed Connectivity

```bash
python manage_feeds.py test
```

Tests all active feeds and shows how many entries are available.

## Getting RSS Feed URLs

### Google Alerts (Recommended)

1. Go to [Google Alerts](https://www.google.com/alerts)
2. Create an alert for your job search (e.g., "Software Engineer jobs San Francisco")
3. Click "Show options"
4. Set "Deliver to" as "RSS feed"
5. Click "Create Alert"
6. Click the RSS icon to get the feed URL
7. Copy the URL and add it to your configuration

### Other RSS Sources

Many job boards provide RSS feeds:

- **Indeed**: `https://www.indeed.com/rss?q=job+title&l=location`
- **Stack Overflow Jobs**: Check their RSS feed options
- **GitHub Jobs**: (if available) Check their API documentation
- **Company Career Pages**: Many companies provide RSS feeds for their job postings

## Example Configurations

### Example 1: Multiple Google Alerts

```json
{
  "feeds": [
    {
      "name": "Google Alerts - Python Developer Remote",
      "url": "https://www.google.com/alerts/feeds/USER_ID/ALERT_ID_1",
      "enabled": true,
      "priority": 1,
      "tags": ["python", "remote"],
      "description": "Remote Python developer positions"
    },
    {
      "name": "Google Alerts - Full Stack Engineer",
      "url": "https://www.google.com/alerts/feeds/USER_ID/ALERT_ID_2",
      "enabled": true,
      "priority": 2,
      "tags": ["full-stack", "general"],
      "description": "Full stack engineering roles"
    }
  ]
}
```

### Example 2: Mixed Sources

```json
{
  "feeds": [
    {
      "name": "Google Alerts - Senior Engineer",
      "url": "https://www.google.com/alerts/feeds/USER_ID/ALERT_ID",
      "enabled": true,
      "priority": 1,
      "tags": ["google-alerts", "senior"]
    },
    {
      "name": "Indeed - Software Engineer",
      "url": "https://www.indeed.com/rss?q=software+engineer&l=remote",
      "enabled": true,
      "priority": 2,
      "tags": ["indeed", "aggregator"]
    }
  ]
}
```

## Best Practices

1. **Use Descriptive Names**: Make it easy to identify feeds at a glance
2. **Set Priorities**: Higher priority feeds (lower numbers) are processed first
3. **Use Tags**: Organize feeds by technology, location, or job type
4. **Disable Instead of Delete**: Keep feeds for future reference
5. **Test Regularly**: Use `python manage_feeds.py test` to verify feeds are working
6. **Version Control**: Commit `rss_feeds.json` to track changes over time

## Troubleshooting

### No feeds found

- Check that `rss_feeds.json` exists and is valid JSON
- Verify at least one feed is enabled
- Check the `USE_JSON_FEEDS` setting in `.env`

### Feed not working

- Test the feed URL in a browser
- Use `python manage_feeds.py test` to diagnose issues
- Check for typos in the URL
- Verify the feed is still active

### Feeds not being processed

- Check that feeds are enabled (`"enabled": true`)
- Verify the feed URLs are correct
- Check the logs in `job_automation.log` for errors

