# Job Automation System - Complete Guide

> **An intelligent job automation system that monitors RSS feeds, analyzes job postings using AI, and sends daily email summaries of suitable positions.**

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [RSS Feeds Setup](#rss-feeds-setup)
6. [User Profile Setup](#user-profile-setup)
7. [Running the System](#running-the-system)
8. [GitHub Actions Deployment](#github-actions-deployment)
9. [Customization](#customization)
10. [Troubleshooting](#troubleshooting)
11. [API Reference](#api-reference)
12. [Examples](#examples)

---

## Overview

This system automates your job search by:
1. **Monitoring RSS feeds** from Google Alerts and other sources
2. **Extracting job content** from posting URLs
3. **Analyzing jobs** using Google's Gemini AI to match your profile
4. **Scoring each job** from 0-100 based on fit
5. **Sending email reports** with the best matches

### How It Works

```
RSS Feeds → Content Extraction → AI Analysis → Email Report
   ↓              ↓                   ↓             ↓
Multiple      Clean text         Gemini API    HTML email
 sources      extraction         matching      with scores
```

### System Architecture

```
┌─────────────────┐
│  RSS Feeds      │ (Google Alerts, Indeed, etc.)
└────────┬────────┘
         ↓
┌─────────────────┐
│  RSS Parser     │ (rss_parser.py)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Content Extract │ (content_extractor.py)
└────────┬────────┘
         ↓
┌─────────────────┐
│  Job Analyzer   │ (job_analyzer.py + Gemini API)
└────────┬────────┘
         ↓
┌─────────────────┐
│  Email Sender   │ (email_sender.py)
└─────────────────┘
```

---

## Features

✅ **RSS Feed Monitoring** - Parse multiple RSS feeds with priority support
✅ **AI-Powered Matching** - Uses Google Gemini to analyze job fit
✅ **Smart Scoring** - Jobs scored 0-100 based on your profile
✅ **Email Reports** - Beautiful HTML emails with job summaries
✅ **Daily Automation** - Runs automatically via GitHub Actions
✅ **JSON Configuration** - Easy-to-manage config files
✅ **Advanced Filtering** - Salary, location, keywords, company preferences
✅ **Backward Compatible** - Supports environment variables too

---

## Quick Start

### Prerequisites

- Python 3.8+
- Gmail account (for sending emails)
- Google Gemini API key
- Google Alerts RSS feeds

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd job-automation

# Run setup script
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Get API Keys

#### 1. Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

#### 2. Gmail App Password

1. Enable 2-Factor Authentication on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Copy the 16-character password

### Basic Configuration

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   EMAIL_TO=your_email@gmail.com
   USE_JSON_FEEDS=true
   USE_JSON_PROFILE=true
   ```

3. **Edit `user_profile.json`:**
   ```json
   {
     "profile": {
       "skills": ["Python", "JavaScript", "React"],
       "experience_years": 3,
       "preferred_locations": ["Remote", "San Francisco"],
       "job_titles": ["Software Engineer", "Full Stack Developer"]
     }
   }
   ```

4. **Edit `rss_feeds.json`** (see RSS Feeds Setup section below)

### Method 2: Environment Variables (Simple)

**Files:**
- `.env` - All configuration in environment variables

**Set in `.env`:**
```env
USE_JSON_PROFILE=false
USE_JSON_FEEDS=false
YOUR_SKILLS=Python,JavaScript,React
YOUR_EXPERIENCE_YEARS=3
YOUR_PREFERRED_LOCATIONS=Remote,San Francisco
YOUR_JOB_TITLES=Software Engineer,Full Stack Developer
RSS_FEEDS=https://feed1.xml,https://feed2.xml
```

---

## RSS Feeds Setup

### Getting Google Alerts RSS Feeds

1. **Go to [Google Alerts](https://www.google.com/alerts)**

2. **Create job search alerts:**
   - "Software Engineer jobs"
   - "Python developer remote"
   - "Full Stack Developer [your city]"
   - "Backend Engineer hiring"

3. **Configure each alert:**
   - **How often:** As-it-happens or At most once a day
   - **Sources:** Automatic or News
   - **Language:** Your preferred language
   - **Region:** Your target region
   - **How many:** All results
   - **Deliver to:** RSS feed ⚠️ Important!

4. **Copy the RSS feed URL:**
   - Click "RSS" icon next to the alert
   - Copy the URL (looks like: `https://www.google.com/alerts/feeds/...`)

5. **Add to `rss_feeds.json`:**
   ```json
   {
     "feeds": [
       {
         "name": "Google Alerts - Software Engineer",
         "url": "https://www.google.com/alerts/feeds/12345678901234567890/1234567890123456789",
         "enabled": true,
         "priority": 1,
         "tags": ["software-engineer", "general"],
         "description": "General software engineering jobs"
       }
     ]
   }
   ```

### RSS Feed Configuration Reference

```json
{
  "feeds": [
    {
      "name": "Feed Name",              // Required: Display name
      "url": "https://feed-url.xml",    // Required: RSS feed URL
      "enabled": true,                  // Optional: Enable/disable (default: true)
      "priority": 1,                    // Optional: Processing priority 1-10 (default: 1)
      "tags": ["tag1", "tag2"],         // Optional: Organize feeds by tags
      "description": "Description"      // Optional: Feed description
    }
  ],
  "settings": {
    "max_feeds_to_process": 10,         // Optional: Max feeds per run
    "respect_priority": true,           // Optional: Process by priority
    "skip_disabled": true               // Optional: Skip disabled feeds
  }
}
```

### Managing RSS Feeds

**Using CLI tool:**
```bash
# Add a new feed interactively
python3 manage_feeds.py add

# List all feeds
python3 manage_feeds.py list

# Enable/disable a feed
python3 manage_feeds.py enable "Feed Name"
python3 manage_feeds.py disable "Feed Name"

# Remove a feed
python3 manage_feeds.py remove "Feed Name"

# Test feeds
python3 manage_feeds.py test
```

**Manually editing:**
Just edit `rss_feeds.json` directly with your favorite editor.

### Other RSS Feed Sources

**Indeed:**
```
https://www.indeed.com/rss?q=software+engineer&l=San+Francisco
```

**LinkedIn (via third-party):**
Use services like RSSHub or create custom scrapers.

**Company Career Pages:**
Some companies offer RSS feeds for their job postings.

---

## User Profile Setup

### Complete Configuration Reference

```json
{
  "profile": {
    // Basic Information
    "name": "Your Name",                          // Optional
    "email": "your.email@example.com",            // Optional

    // Required Fields
    "skills": [                                   // Required: Your technical skills
      "Python",
      "JavaScript",
      "React",
      "Node.js",
      "AWS",
      "Docker",
      "Kubernetes",
      "PostgreSQL"
    ],
    "experience_years": 3,                        // Required: Years of experience
    "preferred_locations": [                      // Required: Target locations
      "Remote",
      "San Francisco",
      "New York",
      "Austin"
    ],
    "job_titles": [                               // Required: Target job titles
      "Software Engineer",
      "Full Stack Developer",
      "Backend Developer",
      "Python Developer"
    ],

    // Optional Fields
    "job_types": [                                // Optional: Employment types
      "Full-time",
      "Contract",
      "Part-time"
    ],
    "salary_expectations": {                      // Optional: Salary range
      "min": 80000,
      "max": 150000,
      "currency": "USD"
    },
    "work_preferences": {                         // Optional: Work preferences
      "remote_only": false,                       // Only remote positions
      "willing_to_relocate": true,                // Open to relocation
      "visa_sponsorship_required": false          // Need visa sponsorship
    }
  },

  "preferences": {                                // Optional: Advanced filtering
    "company_size": [                             // Target company sizes
      "Startup",
      "Mid-size",
      "Enterprise"
    ],
    "industries": [                               // Target industries
      "Technology",
      "FinTech",
      "HealthTech",
      "E-commerce"
    ],
    "avoid_keywords": [                           // Keywords to avoid
      "unpaid",
      "commission only",
      "MLM",
      "pyramid"
    ],
    "required_keywords": [                        // Must-have keywords
      "health insurance",
      "401k"
    ],
    "nice_to_have": [                             // Nice-to-have features
      "equity",
      "stock options",
      "flexible hours",
      "remote work"
    ]
  },

  "settings": {                                   // Optional: System settings
    "min_match_score": 60,                        // Minimum score for "suitable" (0-100)
    "max_jobs_to_analyze": 20,                    // Max jobs to analyze per run
    "days_back": 1,                               // How many days back to search
    "send_email_if_no_matches": true              // Send email even with no matches
  }
}
```

### Field Descriptions

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `skills` | array | Your technical skills | Required |
| `experience_years` | number | Years of professional experience | Required |
| `preferred_locations` | array | Target locations (cities, "Remote") | Required |
| `job_titles` | array | Job titles you're looking for | Required |
| `job_types` | array | Employment types (Full-time, Contract, etc.) | [] |
| `salary_expectations.min` | number | Minimum acceptable salary | 0 |
| `salary_expectations.max` | number | Maximum expected salary | 0 |
| `salary_expectations.currency` | string | Currency code (USD, EUR, GBP, etc.) | "USD" |
| `work_preferences.remote_only` | boolean | Only consider remote positions | false |
| `work_preferences.willing_to_relocate` | boolean | Open to relocation | true |
| `work_preferences.visa_sponsorship_required` | boolean | Need visa sponsorship | false |
| `company_size` | array | Preferred company sizes | [] |
| `industries` | array | Target industries | [] |
| `avoid_keywords` | array | Keywords to avoid in job postings | [] |
| `required_keywords` | array | Must-have keywords | [] |
| `nice_to_have` | array | Nice-to-have features/benefits | [] |
| `min_match_score` | number | Minimum score to consider suitable (0-100) | 60 |
| `max_jobs_to_analyze` | number | Max jobs to analyze per run | 20 |
| `days_back` | number | How many days back to search | 1 |
| `send_email_if_no_matches` | boolean | Send email even with no matches | true |

---

## Running the System

### Local Execution

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the system
python3 main.py
```

### What Happens

1. **Loads configuration** from JSON files and `.env`
2. **Parses RSS feeds** to find job postings
3. **Extracts content** from job posting URLs
4. **Analyzes jobs** using Gemini API
5. **Scores each job** from 0-100
6. **Sends email report** with suitable jobs (score ≥ 60)

### Output

```
============================================================
Starting Job Automation System
============================================================
Loading configuration...
Configured 3 RSS feeds
  - Google Alerts - Software Engineer (Priority: 1, Tags: software-engineer, general)
  - Google Alerts - Python Developer (Priority: 1, Tags: python, backend)
  - Google Alerts - Remote Jobs (Priority: 2, Tags: remote, flexible)

User Profile:
  Skills: Python, JavaScript, React, Node.js, AWS...
  Experience: 3 years
  Locations: Remote, San Francisco, New York

Step 1: Parsing RSS feeds...
Found 15 job postings

Step 2: Extracting content from job postings...
Successfully extracted content from 12 job postings

Step 3: Analyzing jobs with Gemini API...
Analyzed 12 jobs
Found 5 suitable jobs

Step 4: Sending email report...
Email sent successfully to your_email@gmail.com
```

### Logs

Check `job_automation.log` for detailed execution logs:
```bash
tail -f job_automation.log
```

---

## GitHub Actions Deployment


### Setup GitHub Actions

1. **Create a GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/job-automation.git
   git push -u origin main
   ```

2. **Add GitHub Secrets:**
   - Go to your repository on GitHub
   - Click **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Add the following secrets:

   | Secret Name | Value |
   |-------------|-------|
   | `GEMINI_API_KEY` | Your Gemini API key |
   | `SMTP_SERVER` | smtp.gmail.com |
   | `SMTP_PORT` | 587 |
   | `SMTP_USERNAME` | your_email@gmail.com |
   | `SMTP_PASSWORD` | Your Gmail app password |
   | `EMAIL_TO` | your_email@gmail.com |

3. **Commit configuration files:**
   ```bash
   git add rss_feeds.json user_profile.json
   git commit -m "Add configuration files"
   git push
   ```

4. **Enable GitHub Actions:**
   - Go to **Actions** tab in your repository
   - Enable workflows if prompted

### Workflow Configuration

The workflow file `.github/workflows/daily-job-check.yml` is already configured:

```yaml
name: Daily Job Automation

on:
  schedule:
    - cron: '0 9 * * *'  # Runs daily at 9:00 AM UTC
  workflow_dispatch:      # Allows manual trigger

jobs:
  job-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run job automation
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          SMTP_SERVER: ${{ secrets.SMTP_SERVER }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USERNAME: ${{ secrets.SMTP_USERNAME }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
          USE_JSON_FEEDS: true
          USE_JSON_PROFILE: true
        run: python main.py
```

### Manual Trigger

To run the workflow manually:
1. Go to **Actions** tab
2. Select **Daily Job Automation**
3. Click **Run workflow**
4. Select branch and click **Run workflow**

### Change Schedule

Edit `.github/workflows/daily-job-check.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9:00 AM UTC
  - cron: '0 18 * * *' # Daily at 6:00 PM UTC (twice daily)
```

**Cron syntax:**
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

**Examples:**
- `0 9 * * *` - Daily at 9:00 AM UTC
- `0 9 * * 1-5` - Weekdays at 9:00 AM UTC
- `0 */6 * * *` - Every 6 hours
- `0 9,18 * * *` - Daily at 9:00 AM and 6:00 PM UTC

---

## Customization

### Adjust Match Threshold

**Option 1: Edit `user_profile.json`:**
```json
{
  "settings": {
    "min_match_score": 70  // Higher = more selective (default: 60)
  }
}
```

**Option 2: Edit `job_analyzer.py`:**
```python
# Line ~137
'suitable': score >= 70  # Change from 60 to 70
```

### Process More Jobs

Edit `user_profile.json`:
```json
{
  "settings": {
    "max_jobs_to_analyze": 50  // Default: 20
  }
}
```

### Search More Days Back

Edit `user_profile.json`:
```json
{
  "settings": {
    "days_back": 7  // Default: 1 (search last 7 days)
  }
}
```

### Customize Email Template

Edit `email_sender.py`:

**HTML template** (`_create_html_body` method):
```python
def _create_html_body(self, analyses: List[Dict], total_jobs: int) -> str:
    # Customize HTML email template here
    # Change colors, layout, add your logo, etc.
```

**Text template** (`_create_text_body` method):
```python
def _create_text_body(self, analyses: List[Dict], total_jobs: int) -> str:
    # Customize plain text email template here
```

### Add Custom Scoring Logic

Edit `job_analyzer.py` (`_create_analysis_prompt` method):
```python
def _create_analysis_prompt(self, job_content: Dict) -> str:
    prompt = f"""
    You are a job matching expert. Analyze the following job posting...

    # Add your custom instructions here
    # For example:
    # - Give extra weight to remote positions
    # - Prioritize companies with good work-life balance
    # - Consider commute time for on-site positions
    """
```

---

## Troubleshooting

### No Jobs Found

**Possible causes:**
- RSS feed URLs are incorrect
- Feeds have no recent entries
- Feeds are disabled in `rss_feeds.json`

**Solutions:**
```bash
# Test RSS feeds
python3 manage_feeds.py test

# Check feed URLs in browser
# Visit each URL to verify it returns XML

# Enable all feeds
# Edit rss_feeds.json and set "enabled": true
```

### Email Not Sending

**Possible causes:**
- Incorrect SMTP credentials
- Using regular Gmail password instead of app password
- Firewall blocking SMTP port 587

**Solutions:**
```bash
# Verify credentials in .env
cat .env | grep SMTP

# Test SMTP connection
python3 -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your_email@gmail.com', 'your_app_password')
print('✅ SMTP connection successful')
server.quit()
"

# Generate new Gmail app password
# https://myaccount.google.com/apppasswords
```

### Gemini API Errors

**Possible causes:**
- Invalid API key
- API quota exceeded
- Rate limiting

**Solutions:**
```bash
# Verify API key
python3 -c "
import google.generativeai as genai
genai.configure(api_key='your_api_key')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello')
print('✅ Gemini API working')
"

# Check quota at:
# https://makersuite.google.com/app/apikey

# Reduce max_jobs_to_analyze in user_profile.json
```

### Configuration Errors

**Possible causes:**
- Invalid JSON syntax
- Missing required fields
- Incorrect data types

**Solutions:**
```bash
# Validate configuration
python3 test_config.py

# Check JSON syntax
python3 -m json.tool user_profile.json
python3 -m json.tool rss_feeds.json

# View detailed error messages
python3 main.py 2>&1 | tee error.log
```

### GitHub Actions Failing

**Possible causes:**
- Missing secrets
- Configuration files not committed
- Dependency installation issues

**Solutions:**
```bash
# Verify all secrets are set
# Go to Settings → Secrets and variables → Actions

# Commit configuration files
git add rss_feeds.json user_profile.json
git commit -m "Update configuration"
git push

# Check workflow logs
# Go to Actions tab → Select failed run → View logs
```

---

## API Reference

### FeedConfigManager

```python
from feed_config import FeedConfigManager, RSSFeed

# Initialize
manager = FeedConfigManager('rss_feeds.json')

# Load feeds
manager.load_from_json()  # Load from JSON
manager.load_from_env()   # Load from environment variables
feeds = manager.load_feeds(prefer_json=True)  # Auto-load with preference

# Get feeds
active_feeds = manager.get_active_feeds(respect_priority=True)
python_feeds = manager.get_feeds_by_tag('python')
high_priority = manager.get_feeds_by_priority(1)

# Manage feeds
new_feed = RSSFeed(
    name="New Feed",
    url="https://example.com/feed.xml",
    enabled=True,
    priority=1,
    tags=["tag1"],
    description="Description"
)
manager.add_feed(new_feed)
manager.remove_feed("Feed Name")
manager.enable_feed("Feed Name")
manager.disable_feed("Feed Name")

# Save changes
manager.save_to_json()
```

### UserConfigManager

```python
from user_config import UserConfigManager

# Initialize
manager = UserConfigManager('user_profile.json')

# Load profile
manager.load_from_json()  # Load from JSON
manager.load_from_env()   # Load from environment variables

# Access profile
profile = manager.profile
print(profile.skills)
print(profile.experience_years)
print(profile.preferred_locations)

# Access preferences
preferences = manager.preferences
print(preferences.avoid_keywords)
print(preferences.industries)

# Access settings
settings = manager.settings
print(settings.get('min_match_score', 60))
print(settings.get('max_jobs_to_analyze', 20))

# Convert to dict (for backward compatibility)
profile_dict = profile.to_dict()
```

### RSSParser

```python
from rss_parser import RSSParser

# Initialize with feed URLs or RSSFeed objects
parser = RSSParser(feed_urls)

# Parse feeds
jobs = parser.parse_feeds(days_back=1)

# Each job is a dict:
# {
#   'title': 'Job Title',
#   'link': 'https://...',
#   'published': datetime,
#   'summary': 'Job description...'
# }
```

### ContentExtractor

```python
from content_extractor import ContentExtractor

# Initialize
extractor = ContentExtractor(timeout=15)

# Extract content from URL
content = extractor.extract_content(url)

# Returns dict:
# {
#   'title': 'Page Title',
#   'content': 'Extracted text content',
#   'url': 'https://...'
# }
```

### JobAnalyzer

```python
from job_analyzer import JobAnalyzer

# Initialize
analyzer = JobAnalyzer(api_key, user_profile)

# Analyze single job
analysis = analyzer.analyze_job(job_content)

# Analyze multiple jobs
analyses = analyzer.analyze_multiple_jobs(job_contents)

# Each analysis is a dict:
# {
#   'title': 'Job Title',
#   'url': 'https://...',
#   'score': 75,
#   'matching_points': ['Point 1', 'Point 2'],
#   'gaps': ['Gap 1', 'Gap 2'],
#   'recommendation': 'Recommendation text',
#   'suitable': True
# }
```

### EmailSender

```python
from email_sender import EmailSender

# Initialize
sender = EmailSender(smtp_server, smtp_port, username, password)

# Send job report
success = sender.send_job_report(to_email, analyses, total_jobs)
```

---

## Examples

### Example 1: Basic Setup

**user_profile.json:**
```json
{
  "profile": {
    "skills": ["Python", "Django", "PostgreSQL"],
    "experience_years": 2,
    "preferred_locations": ["Remote"],
    "job_titles": ["Backend Developer", "Python Developer"]
  }
}
```

**rss_feeds.json:**
```json
{
  "feeds": [
    {
      "name": "Google Alerts - Python Remote",
      "url": "https://www.google.com/alerts/feeds/.../...",
      "enabled": true,
      "priority": 1
    }
  ]
}
```

### Example 2: Advanced Configuration

**user_profile.json:**
```json
{
  "profile": {
    "skills": ["Python", "JavaScript", "React", "AWS", "Docker"],
    "experience_years": 5,
    "preferred_locations": ["Remote", "San Francisco", "New York"],
    "job_titles": ["Senior Software Engineer", "Tech Lead"],
    "salary_expectations": {
      "min": 120000,
      "max": 180000,
      "currency": "USD"
    },
    "work_preferences": {
      "remote_only": true,
      "willing_to_relocate": false,
      "visa_sponsorship_required": false
    }
  },
  "preferences": {
    "company_size": ["Startup", "Mid-size"],
    "industries": ["FinTech", "HealthTech"],
    "avoid_keywords": ["unpaid", "commission", "on-call 24/7"],
    "required_keywords": ["health insurance", "401k"],
    "nice_to_have": ["equity", "unlimited PTO", "remote-first"]
  },
  "settings": {
    "min_match_score": 70,
    "max_jobs_to_analyze": 30,
    "days_back": 2
  }
}
```

### Example 3: Multiple RSS Feeds with Priorities

**rss_feeds.json:**
```json
{
  "feeds": [
    {
      "name": "Google Alerts - Senior Python Remote",
      "url": "https://www.google.com/alerts/feeds/.../...",
      "enabled": true,
      "priority": 1,
      "tags": ["python", "senior", "remote"]
    },
    {
      "name": "Google Alerts - Tech Lead",
      "url": "https://www.google.com/alerts/feeds/.../...",
      "enabled": true,
      "priority": 1,
      "tags": ["leadership", "senior"]
    },
    {
      "name": "Indeed - Python Jobs",
      "url": "https://www.indeed.com/rss?q=python+developer&l=remote",
      "enabled": true,
      "priority": 2,
      "tags": ["indeed", "python"]
    },
    {
      "name": "Company X Career Page",
      "url": "https://company-x.com/careers/feed",
      "enabled": false,
      "priority": 3,
      "tags": ["company-specific"]
    }
  ],
  "settings": {
    "max_feeds_to_process": 10,
    "respect_priority": true,
    "skip_disabled": true
  }
}
```

### Example 4: Programmatic Usage

```python
#!/usr/bin/env python3
"""Custom job automation script"""

from feed_config import FeedConfigManager
from user_config import UserConfigManager
from rss_parser import RSSParser
from content_extractor import ContentExtractor
from job_analyzer import JobAnalyzer
from email_sender import EmailSender
import os

# Load configuration
feed_manager = FeedConfigManager('rss_feeds.json')
feed_manager.load_from_json()
active_feeds = feed_manager.get_active_feeds()

user_manager = UserConfigManager('user_profile.json')
user_manager.load_from_json()

# Parse RSS feeds
parser = RSSParser(active_feeds)
jobs = parser.parse_feeds(days_back=1)
print(f"Found {len(jobs)} jobs")

# Extract content
extractor = ContentExtractor(timeout=15)
job_contents = []
for job in jobs[:20]:
    content = extractor.extract_content(job['link'])
    if content:
        job_contents.append(content)

# Analyze jobs
analyzer = JobAnalyzer(
    os.getenv('GEMINI_API_KEY'),
    user_manager.profile.to_dict()
)
analyses = analyzer.analyze_multiple_jobs(job_contents)

# Filter suitable jobs
suitable = [a for a in analyses if a['suitable']]
print(f"Found {len(suitable)} suitable jobs")

# Send email
sender = EmailSender(
    os.getenv('SMTP_SERVER'),
    int(os.getenv('SMTP_PORT')),
    os.getenv('SMTP_USERNAME'),
    os.getenv('SMTP_PASSWORD')
)
sender.send_job_report(os.getenv('EMAIL_TO'), analyses, len(jobs))
```

---

## Project Structure

```
job-automation/
├── .github/
│   └── workflows/
│       └── daily-job-check.yml    # GitHub Actions workflow
├── venv/                           # Virtual environment (not in git)
├── rss_parser.py                   # RSS feed parser
├── content_extractor.py            # Web content extraction
├── job_analyzer.py                 # Gemini API job analysis
├── email_sender.py                 # SMTP email sender
├── feed_config.py                  # RSS feed configuration manager
├── user_config.py                  # User profile configuration manager
├── main.py                         # Main orchestration script
├── manage_feeds.py                 # CLI tool for managing feeds
├── test_config.py                  # Configuration validation tests
├── test_setup.py                   # Setup validation tests
├── rss_feeds.json                  # RSS feed configuration
├── user_profile.json               # User profile configuration
├── requirements.txt                # Python dependencies
├── setup.sh                        # Setup script
├── .env                            # Environment variables (not in git)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── README.md                       # Quick start guide
├── GUIDE.md                        # This comprehensive guide
└── job_automation.log              # Execution logs (not in git)
```

---

## License

MIT License - Feel free to modify and use for your job search!

---

## Support

For issues, questions, or contributions:
- Check the [Troubleshooting](#troubleshooting) section
- Review the [Examples](#examples)
- Check `job_automation.log` for detailed error messages

---

**Happy job hunting! 🎯**
       }
     ]
   }
   ```

5. **Test the configuration:**
   ```bash
   python3 test_config.py
   ```

6. **Run the system:**
   ```bash
   python3 main.py
   ```

---

## Configuration

The system supports two configuration methods:

### Method 1: JSON Configuration (Recommended)

**Advantages:**
- ✅ Structured data with validation
- ✅ Advanced features (salary, preferences, filtering)
- ✅ Easy to read and maintain
- ✅ Version control friendly

**Files:**
- `user_profile.json` - Your job preferences
- `rss_feeds.json` - RSS feed sources
- `.env` - API keys and secrets

### Method 2: Environment Variables (Simple)

**Advantages:**
- ✅ Simple setup
- ✅ Good for basic use cases

