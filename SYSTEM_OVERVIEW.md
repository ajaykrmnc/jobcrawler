# Job Automation System - Complete Overview

## 🎯 What This System Does

This automated job hunting assistant:
1. **Monitors** RSS feeds from Google Site Alerts for new job postings
2. **Extracts** clean content from job posting websites using readability
3. **Analyzes** each job using Google's Gemini AI to match against your profile
4. **Scores** jobs from 0-100 based on fit with your skills and preferences
5. **Emails** you a beautiful daily report with the best matching jobs
6. **Runs automatically** every day via GitHub Actions

## 📁 Project Structure

```
job-automation/
├── .github/
│   └── workflows/
│       └── daily-job-check.yml    # GitHub Actions workflow (runs daily)
│
├── Core Modules:
│   ├── rss_parser.py              # Parses RSS feeds from Google Alerts
│   ├── content_extractor.py       # Extracts clean text using readability-lxml
│   ├── job_analyzer.py            # AI analysis using Gemini API
│   ├── email_sender.py            # Sends HTML emails via SMTP
│   └── main.py                    # Orchestrates the entire workflow
│
├── Configuration:
│   ├── .env.example               # Template for environment variables
│   ├── requirements.txt           # Python dependencies
│   └── .gitignore                 # Git ignore rules
│
├── Documentation:
│   ├── README.md                  # Comprehensive documentation
│   ├── QUICKSTART.md              # 5-minute setup guide
│   └── SYSTEM_OVERVIEW.md         # This file
│
└── Utilities:
    ├── setup.sh                   # Automated setup script
    └── test_setup.py              # Verify configuration
```

## 🔄 System Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY AUTOMATION                          │
│              (GitHub Actions - 9 AM UTC)                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: RSS Feed Parsing (rss_parser.py)                   │
│  • Fetches job postings from Google Alerts RSS feeds        │
│  • Filters jobs from last 24 hours                          │
│  • Extracts: title, link, published date, summary           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Content Extraction (content_extractor.py)          │
│  • Visits each job posting URL                              │
│  • Uses readability-lxml to extract clean content           │
│  • Removes ads, navigation, and clutter                     │
│  • Returns plain text job description                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: AI Analysis (job_analyzer.py)                      │
│  • Sends job content + your profile to Gemini API           │
│  • AI analyzes job requirements vs your skills              │
│  • Returns:                                                  │
│    - Suitability score (0-100)                              │
│    - Matching points                                         │
│    - Skill gaps                                              │
│    - Recommendation                                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Email Report (email_sender.py)                     │
│  • Creates beautiful HTML email                             │
│  • Highlights jobs with score >= 60                         │
│  • Shows matching points and gaps                           │
│  • Sends via SMTP (Gmail)                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    📧 You receive email!
```

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **RSS Parsing** | feedparser | Parse Google Alerts RSS feeds |
| **Content Extraction** | readability-lxml | Extract clean text from web pages |
| **Web Scraping** | requests, BeautifulSoup4 | Fetch and parse HTML |
| **AI Analysis** | Google Gemini API | Intelligent job matching |
| **Email** | smtplib, email.mime | Send HTML emails |
| **Configuration** | python-dotenv | Manage environment variables |
| **Automation** | GitHub Actions | Daily scheduled execution |

## 📊 Sample Email Report

Your daily email will look like this:

```
┌────────────────────────────────────────────────┐
│        Daily Job Report - Jan 14, 2026         │
└────────────────────────────────────────────────┘

Summary:
• Total jobs processed: 15
• Jobs analyzed: 12
• Suitable jobs found: 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUITABLE JOBS (Score >= 60):

1. Senior Python Developer - Remote
   Score: 92/100
   URL: https://example.com/job1
   
   Recommendation: Excellent match! Your Python and 
   AWS experience aligns perfectly with requirements.
   
   Matching Points:
   ✓ 3+ years Python experience required
   ✓ AWS and Docker skills mentioned
   ✓ Remote position matches preference
   
   Gaps:
   ⚠ Kubernetes experience preferred (not required)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🚀 Quick Start Commands

```bash
# Initial setup
cd job-automation
./setup.sh

# Configure your profile
nano .env

# Test configuration
python test_setup.py

# Run manually
python main.py

# Deploy to GitHub
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

## 🔐 Required Secrets (for GitHub Actions)

Add these in: Repository → Settings → Secrets and variables → Actions

- `GEMINI_API_KEY` - From Google AI Studio
- `SMTP_USERNAME` - Your Gmail address
- `SMTP_PASSWORD` - Gmail app password
- `EMAIL_TO` - Where to send reports
- `RSS_FEEDS` - Comma-separated RSS URLs
- `YOUR_SKILLS` - Your technical skills
- `YOUR_EXPERIENCE_YEARS` - Years of experience
- `YOUR_PREFERRED_LOCATIONS` - Desired locations
- `YOUR_JOB_TITLES` - Target job titles

## 📈 Customization Options

### Change Schedule
Edit `.github/workflows/daily-job-check.yml`:
```yaml
cron: '0 9 * * *'  # Daily at 9 AM UTC
```

### Adjust Matching Threshold
Edit `job_analyzer.py`:
```python
'suitable': score >= 60  # Change to 70 for stricter matching
```

### Process More Jobs
Edit `main.py`:
```python
for job in jobs[:20]:  # Change 20 to process more
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No jobs found | Verify RSS feed URLs in browser |
| Email not sending | Use Gmail app password, not regular password |
| Gemini API error | Check API key and quota limits |
| GitHub Action fails | Verify all secrets are set correctly |

## 📝 Logs

- **Local**: Check `job_automation.log`
- **GitHub Actions**: Actions tab → Workflow run → View logs

## 🎓 Learning Resources

- [Google Alerts](https://www.google.com/alerts) - Create job alerts
- [Google AI Studio](https://makersuite.google.com/) - Get Gemini API key
- [Gmail App Passwords](https://myaccount.google.com/apppasswords) - SMTP auth
- [GitHub Actions Docs](https://docs.github.com/en/actions) - Automation

## 💡 Pro Tips

1. **Multiple Alerts**: Create specific alerts for different job types
2. **Location Filters**: Add location keywords to Google Alerts
3. **Skill Updates**: Regularly update YOUR_SKILLS in .env
4. **Score Tuning**: Adjust threshold based on market conditions
5. **Timing**: Schedule for early morning to review over coffee ☕

## 🤝 Support

- Check logs for detailed error messages
- Review QUICKSTART.md for setup help
- Verify configuration with test_setup.py
- Ensure all dependencies are installed

---

**Happy Job Hunting! 🎯**

This system works 24/7 to find your perfect job match!

