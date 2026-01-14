# Quick Start Guide

Get your job automation system running in 5 minutes!

## Step 1: Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

## Step 2: Set Up Gmail App Password

1. Go to your [Google Account](https://myaccount.google.com/)
2. Enable 2-Factor Authentication if not already enabled
3. Visit [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and generate a password
5. Copy the 16-character password

## Step 3: Get RSS Feeds from Google Alerts

1. Go to [Google Alerts](https://www.google.com/alerts)
2. Create alerts for your job searches:
   - Example: "Software Engineer Python remote"
   - Example: "Full Stack Developer San Francisco"
   - Example: "Backend Engineer startup"
3. For each alert:
   - Click "Show options"
   - Set "Deliver to" → "RSS feed"
   - Click "Create Alert"
   - Copy the RSS feed URL (looks like: `https://www.google.com/alerts/feeds/...`)
4. Combine all RSS URLs with commas

## Step 4: Run Setup

```bash
cd job-automation
./setup.sh
```

## Step 5: Configure Your Profile

Edit the `.env` file:

```bash
nano .env  # or use your favorite editor
```

Fill in:

```env
GEMINI_API_KEY=your_key_from_step_1
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_from_step_2
EMAIL_TO=your_email@gmail.com
RSS_FEEDS=feed1_url,feed2_url,feed3_url

YOUR_SKILLS=Python,JavaScript,Docker,AWS,React
YOUR_EXPERIENCE_YEARS=3
YOUR_PREFERRED_LOCATIONS=Remote,San Francisco
YOUR_JOB_TITLES=Software Engineer,Full Stack Developer
```

## Step 6: Test Locally

```bash
source venv/bin/activate
python main.py
```

Check your email for the job report!

## Step 7: Deploy to GitHub Actions

### Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/job-automation.git
git push -u origin main
```

### Add GitHub Secrets

Go to: Repository → Settings → Secrets and variables → Actions

Add these secrets (copy from your `.env` file):

| Secret Name | Value |
|-------------|-------|
| `GEMINI_API_KEY` | Your Gemini API key |
| `SMTP_SERVER` | smtp.gmail.com |
| `SMTP_PORT` | 587 |
| `SMTP_USERNAME` | your_email@gmail.com |
| `SMTP_PASSWORD` | Your Gmail app password |
| `EMAIL_TO` | your_email@gmail.com |
| `RSS_FEEDS` | Your comma-separated RSS URLs |
| `YOUR_SKILLS` | Your skills (comma-separated) |
| `YOUR_EXPERIENCE_YEARS` | Number of years |
| `YOUR_PREFERRED_LOCATIONS` | Locations (comma-separated) |
| `YOUR_JOB_TITLES` | Job titles (comma-separated) |

### Test GitHub Action

1. Go to "Actions" tab in your repository
2. Click "Daily Job Automation"
3. Click "Run workflow" → "Run workflow"
4. Wait for completion and check your email!

## Customization Tips

### Change Schedule

Edit `.github/workflows/daily-job-check.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # 9 AM UTC daily
  # Change to '0 14 * * *' for 2 PM UTC
  # Or '0 1 * * 1' for 1 AM UTC every Monday
```

### Adjust Job Matching Threshold

Jobs with score >= 60 are considered "suitable". To change this:

Edit `job_analyzer.py`, find:
```python
'suitable': score >= 60
```

Change to:
```python
'suitable': score >= 70  # More selective
```

### Process More Jobs

By default, the system processes up to 20 jobs per run. To change:

Edit `main.py`, find:
```python
for job in jobs[:20]:
```

Change to:
```python
for job in jobs[:50]:  # Process 50 jobs
```

## Troubleshooting

### "No jobs found"
- Check your RSS feed URLs are correct
- Visit the URLs in a browser to verify they work
- Make sure feeds have recent entries

### "Email not sending"
- Verify you're using Gmail app password, not regular password
- Check SMTP settings are correct
- Try sending a test email manually

### "Gemini API error"
- Verify API key is correct
- Check you haven't exceeded free tier limits
- Visit [Google AI Studio](https://makersuite.google.com/) to check quota

### "GitHub Action failing"
- Check all secrets are added correctly
- View the action logs for specific errors
- Ensure requirements.txt is committed

## Support

Check `job_automation.log` for detailed execution logs.

For issues, review the main README.md for more detailed documentation.

Happy job hunting! 🎯

