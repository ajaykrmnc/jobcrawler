# RSS Feeds - Quick Reference

## 🚀 Quick Start

### Using JSON Configuration (Recommended)

1. **Edit `rss_feeds.json`**:
   ```json
   {
     "feeds": [
       {
         "name": "My Job Feed",
         "url": "https://your-feed-url.xml",
         "enabled": true,
         "priority": 1,
         "tags": ["tag1", "tag2"],
         "description": "Description here"
       }
     ]
   }
   ```

2. **Set in `.env`**:
   ```env
   USE_JSON_FEEDS=true
   ```

3. **Test**:
   ```bash
   python3 manage_feeds.py test
   ```

### Using Environment Variable (Simple)

1. **Set in `.env`**:
   ```env
   USE_JSON_FEEDS=false
   RSS_FEEDS=https://feed1.xml,https://feed2.xml
   ```

## 📋 CLI Commands

| Command | Description |
|---------|-------------|
| `python3 manage_feeds.py list` | List all feeds |
| `python3 manage_feeds.py add` | Add a new feed |
| `python3 manage_feeds.py toggle` | Enable/disable a feed |
| `python3 manage_feeds.py test` | Test feed connectivity |

## 📝 Feed Properties

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `name` | string | ✅ Yes | - | Feed name |
| `url` | string | ✅ Yes | - | RSS feed URL |
| `enabled` | boolean | No | `true` | Enable/disable |
| `priority` | integer | No | `1` | Priority (lower = higher) |
| `tags` | array | No | `[]` | Tags for organization |
| `description` | string | No | `""` | Description/notes |

## 🔧 Configuration Options

### In `.env` file:

```env
# Use JSON configuration (recommended)
USE_JSON_FEEDS=true

# OR use environment variable (simple)
USE_JSON_FEEDS=false
RSS_FEEDS=https://feed1.xml,https://feed2.xml,https://feed3.xml
```

## 📚 Common Tasks

### Add a Google Alert Feed

1. Create alert at [Google Alerts](https://www.google.com/alerts)
2. Set "Deliver to" as "RSS feed"
3. Copy the RSS URL
4. Add to `rss_feeds.json`:
   ```json
   {
     "name": "Google Alerts - Python Jobs",
     "url": "YOUR_COPIED_URL",
     "enabled": true,
     "priority": 1,
     "tags": ["python", "google-alerts"]
   }
   ```

### Temporarily Disable a Feed

**Option 1: Using CLI**
```bash
python3 manage_feeds.py toggle
# Select the feed number
```

**Option 2: Edit JSON**
```json
{
  "name": "My Feed",
  "enabled": false,  // Changed from true
  ...
}
```

### Set Feed Priority

Lower number = higher priority (processed first)

```json
{
  "name": "High Priority Feed",
  "priority": 1,  // Processed first
  ...
},
{
  "name": "Low Priority Feed",
  "priority": 10,  // Processed last
  ...
}
```

### Organize Feeds with Tags

```json
{
  "feeds": [
    {
      "name": "Python Jobs",
      "tags": ["python", "backend", "high-priority"]
    },
    {
      "name": "Remote Jobs",
      "tags": ["remote", "flexible"]
    }
  ]
}
```

## 🧪 Testing

### Test All Feeds
```bash
python3 manage_feeds.py test
```

### Test Full System
```bash
python3 test_setup.py
```

### Run Job Automation
```bash
python3 main.py
```

## 📖 Documentation Files

| File | Description |
|------|-------------|
| `RSS_FEEDS_GUIDE.md` | Complete guide |
| `EXAMPLES.md` | Practical examples |
| `CHANGELOG_RSS_FEEDS.md` | What's new |
| `QUICK_REFERENCE.md` | This file |

## 🐛 Troubleshooting

### No feeds found
- Check `rss_feeds.json` exists
- Verify at least one feed has `"enabled": true`
- Check `USE_JSON_FEEDS` in `.env`

### Feed not working
- Test with: `python3 manage_feeds.py test`
- Verify URL in browser
- Check logs in `job_automation.log`

### System using wrong configuration
- Check `USE_JSON_FEEDS` in `.env`
- `true` = uses `rss_feeds.json`
- `false` = uses `RSS_FEEDS` env var

## 💡 Best Practices

1. ✅ Use descriptive feed names
2. ✅ Set priorities (1 = highest)
3. ✅ Add tags for organization
4. ✅ Disable instead of delete
5. ✅ Test before deploying
6. ✅ Document with descriptions

## 🔄 Migration from Old System

**Old way** (still works):
```env
RSS_FEEDS=https://feed1.xml,https://feed2.xml
```

**New way** (recommended):
1. Create `rss_feeds.json` with your feeds
2. Set `USE_JSON_FEEDS=true` in `.env`
3. Test with `python3 manage_feeds.py test`

## 📞 Getting Help

1. Read `RSS_FEEDS_GUIDE.md` for details
2. Check `EXAMPLES.md` for examples
3. Run `python3 manage_feeds.py` for CLI help
4. Check `job_automation.log` for errors

