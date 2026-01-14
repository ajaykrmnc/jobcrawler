# Job Automation System

An intelligent job automation system that monitors RSS feeds from Google Site Alerts, analyzes job postings using Google's Gemini API, and sends daily email summaries of suitable positions.

## Features

- 📡 **RSS Feed Monitoring**: Automatically parses multiple RSS feeds from Google Site Alerts
- 🔍 **Content Extraction**: Uses readability-lxml to extract clean content from job posting pages
- 🤖 **AI-Powered Analysis**: Leverages Google Gemini API to match jobs against your profile
- 📧 **Email Notifications**: Sends beautiful HTML email reports with suitable job matches
- ⏰ **Daily Automation**: Runs automatically every day via GitHub Actions
- 📊 **Smart Scoring**: Jobs are scored 0-100 based on your skills and preferences
- ⚙️ **JSON Configuration**: Easy-to-manage configuration files for RSS feeds and user profiles

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
cd job-automation
pip install -r requirements.txt
```

### 2. Configure Your Profile

**Recommended: Use JSON Configuration**

Edit `user_profile.json` with your information:

```json
{
  "profile": {
    "skills": ["Python", "JavaScript", "React", "AWS"],
    "experience_years": 3,
    "preferred_locations": ["Remote", "San Francisco"],
    "job_titles": ["Software Engineer", "Full Stack Developer"]
  }
}
```

See [USER_PROFILE_GUIDE.md](USER_PROFILE_GUIDE.md) for complete configuration options.

**Alternative: Use Environment Variables**

Copy `.env.example` to `.env` and edit:

```bash
cp .env.example .env
```

```env
# Gemini API Key (get from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here

# SMTP Configuration (for Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
EMAIL_TO=your_email@gmail.com

# Use JSON configuration (recommended)
USE_JSON_FEEDS=true
USE_JSON_PROFILE=true
```

### 3. Configure RSS Feeds

**Recommended: Use JSON Configuration**

Edit `rss_feeds.json` with your RSS feed URLs:

```json
{
  "feeds": [
    {
      "name": "Google Alerts - Software Engineer",
      "url": "https://www.google.com/alerts/feeds/YOUR_USER_ID/YOUR_ALERT_ID",
      "enabled": true,
      "priority": 1,
      "tags": ["software-engineer"]
    }
  ]
}
```

See [RSS_FEEDS_GUIDE.md](RSS_FEEDS_GUIDE.md) for complete configuration options.

**Get Google Site Alerts RSS Feeds:**

1. Go to [Google Alerts](https://www.google.com/alerts)
2. Create alerts for job searches (e.g., "Software Engineer jobs", "Python developer remote")
3. Set "Deliver to" as "RSS feed"
4. Copy the RSS feed URLs and add them to `rss_feeds.json`

### 4. Test Configuration

Test your configuration files:

```bash
python manage_feeds.py test
python test_setup.py
```

### 5. Gmail App Password Setup

If using Gmail for SMTP:

1. Enable 2-Factor Authentication on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use this password in `SMTP_PASSWORD` (not your regular Gmail password)

### 6. Test Locally

Run the script locally to test:

```bash
python main.py
```

Check `job_automation.log` for detailed execution logs.

## GitHub Actions Setup

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Job automation system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/job-automation.git
git push -u origin main
```

### 2. Configure GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

- `GEMINI_API_KEY`
- `SMTP_SERVER` (e.g., smtp.gmail.com)
- `SMTP_PORT` (e.g., 587)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `EMAIL_TO`
- `RSS_FEEDS` (comma-separated URLs)
- `YOUR_SKILLS`
- `YOUR_EXPERIENCE_YEARS`
- `YOUR_PREFERRED_LOCATIONS`
- `YOUR_JOB_TITLES`

### 3. Enable GitHub Actions

The workflow will run automatically every day at 9:00 AM UTC. You can also trigger it manually:

1. Go to Actions tab
2. Select "Daily Job Automation"
3. Click "Run workflow"

## Project Structure

```
job-automation/
├── .github/
│   └── workflows/
│       └── daily-job-check.yml    # GitHub Actions workflow
├── rss_parser.py                   # RSS feed parser
├── content_extractor.py            # Web content extraction
├── job_analyzer.py                 # Gemini API job analysis
├── email_sender.py                 # SMTP email sender
├── main.py                         # Main orchestration script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## How It Works

1. **RSS Parsing**: Fetches job postings from configured RSS feeds
2. **Content Extraction**: Extracts clean text from job posting URLs using readability
3. **AI Analysis**: Sends job content to Gemini API with your profile for matching
4. **Scoring**: Each job receives a score (0-100) based on fit
5. **Email Report**: Sends HTML email with suitable jobs (score >= 60)

## Customization

### Adjust Schedule

Edit `.github/workflows/daily-job-check.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Change time (UTC)
```

### Change Suitability Threshold

Edit `job_analyzer.py`, line with `suitable: score >= 60`:

```python
'suitable': score >= 70  # Increase threshold
```

### Modify Email Template

Edit `email_sender.py` methods `_create_html_body()` and `_create_text_body()`

## Troubleshooting

### No jobs found
- Verify RSS feed URLs are correct
- Check if feeds have recent entries

### Email not sending
- Verify SMTP credentials
- For Gmail, ensure app password is used (not regular password)
- Check firewall/network settings

### Gemini API errors
- Verify API key is valid
- Check API quota limits
- Review error logs in `job_automation.log`

## License

MIT License - feel free to modify and use for your job search!

