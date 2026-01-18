# Job Automation System

> **An intelligent job automation system that monitors RSS feeds, analyzes job postings using AI, and sends 
> daily email summaries of suitable positions.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone <your-repo-url>
cd job-automation
./setup.sh

# 2. Configure
cp .env.example .env
# Edit .env with your API keys
# Edit user_profile.json with your job preferences
# Edit rss_feeds.json with your RSS feeds

# 3. Test
python3 test_config.py

# 4. Run
python3 main.py
```

📖 **[Read the Complete Guide →](GUIDE.md)**

## ✨ Features

- 📡 **RSS Feed Monitoring** - Parse multiple RSS feeds with priority support
- 🤖 **AI-Powered Matching** - Uses Google Gemini to analyze job fit
- 📊 **Smart Scoring** - Jobs scored 0-100 based on your profile
- 📧 **Email Reports** - Beautiful HTML emails with job summaries
- ⏰ **Daily Automation** - Runs automatically via GitHub Actions
- ⚙️ **JSON Configuration** - Easy-to-manage config files
- 🎯 **Advanced Filtering** - Salary, location, keywords, company preferences

## 📋 Requirements

- Python 3.8+
- Gmail account (for sending emails)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Google Alerts RSS feeds ([Create alerts](https://www.google.com/alerts))

## ⚙️ Configuration

### 1. Environment Variables (`.env`)

```env
GEMINI_API_KEY=your_gemini_api_key_here
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
EMAIL_TO=your_email@gmail.com
USE_JSON_PROFILE=true
USE_JSON_FEEDS=true
```

### 2. User Profile (`user_profile.json`)

```json
{
"profile": {
"skills": ["Python", "JavaScript", "React"],
"experience_years": 3,
"preferred_locations": ["Remote", "San Francisco"],
"job_titles": ["Software Engineer"]
},
"settings": {
"min_match_score": 60,
"max_jobs_to_analyze": 20,
"days_back": 1
}
}
```

### 3. RSS Feeds (`rss_feeds.json`)

```json
{
"feeds": [
{
"name": "Google Alerts - Software Engineer",
"url": "https://www.google.com/alerts/feeds/.../...",
"enabled": true,
"priority": 1
}
]
}
```

📖 **[Complete Configuration Guide →](GUIDE.md#configuration)**

## 🔧 Usage

### Local Execution

```bash
python3 main.py
```

### GitHub Actions (Automated)

1. Push to GitHub
2. Add secrets in Settings → Secrets and variables → Actions
3. Workflow runs daily at 9:00 AM UTC

📖 **[GitHub Actions Setup Guide →](GUIDE.md#github-actions-deployment)**

## 📁 Project Structure

```
job-automation/
├── main.py                  # Main orchestration script
├── rss_parser.py            # RSS feed parser
├── content_extractor.py     # Web content extraction
├── job_analyzer.py          # Gemini API job analysis
├── email_sender.py          # SMTP email sender
├── feed_config.py           # RSS feed config manager
├── user_config.py           # User profile config manager
├── manage_feeds.py          # CLI tool for managing feeds
├── test_config.py           # Configuration tests
├── user_profile.json        # Your job preferences
├── rss_feeds.json           # RSS feed sources
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── README.md                # This file
└── GUIDE.md                 # Complete documentation
```

## 🎯 How It Works

```
RSS Feeds → Content Extraction → AI Analysis → Email Report
```

1. **Parse RSS feeds** from Google Alerts and other sources
2. **Extract content** from job posting URLs
3. **Analyze with Gemini AI** to match your profile
4. **Score jobs** from 0-100 based on fit
5. **Send email** with suitable jobs (score ≥ 60)

## 🛠️ CLI Tools

```bash
# Manage RSS feeds
python3 manage_feeds.py add
python3 manage_feeds.py list
python3 manage_feeds.py test

# Test configuration
python3 test_config.py
python3 test_setup.py
```

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| No jobs found | Verify RSS feed URLs, check feed has recent entries |
| Email not sending | Use Gmail app password, verify SMTP credentials |
| Gemini API errors | Check API key, verify quota limits |
| Configuration errors | Run `python3 test_config.py` |

📖 **[Complete Troubleshooting Guide →](GUIDE.md#troubleshooting)**

## 📚 Documentation

- **[GUIDE.md](GUIDE.md)** - Complete comprehensive guide (setup, configuration, deployment, examples, API 
reference)
- **[README.md](README.md)** - This quick start guide

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - Feel free to modify and use for your job search!

---

**Happy job hunting! 🎯**

For detailed documentation, see **[GUIDE.md](GUIDE.md)**

