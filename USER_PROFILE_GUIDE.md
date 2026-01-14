# User Profile Configuration Guide

## Overview

The job automation system now supports **JSON-based user profile configuration** for better organization and more features. This guide explains how to configure your profile using `user_profile.json`.

## Quick Start

### 1. Edit `user_profile.json`

```json
{
  "profile": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "skills": ["Python", "JavaScript", "React"],
    "experience_years": 3,
    "preferred_locations": ["Remote", "San Francisco"],
    "job_titles": ["Software Engineer", "Full Stack Developer"]
  }
}
```

### 2. Enable JSON Profile in `.env`

```env
USE_JSON_PROFILE=true
```

### 3. Run the System

```bash
python main.py
```

## Configuration Structure

### Profile Section

Basic information about you and your job preferences:

```json
{
  "profile": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "skills": [
      "Python",
      "JavaScript",
      "React",
      "Node.js",
      "AWS",
      "Docker"
    ],
    "experience_years": 3,
    "preferred_locations": [
      "Remote",
      "San Francisco",
      "New York"
    ],
    "job_titles": [
      "Software Engineer",
      "Full Stack Developer",
      "Backend Developer"
    ],
    "job_types": [
      "Full-time",
      "Contract"
    ],
    "salary_expectations": {
      "min": 80000,
      "max": 150000,
      "currency": "USD"
    },
    "work_preferences": {
      "remote_only": false,
      "willing_to_relocate": true,
      "visa_sponsorship_required": false
    }
  }
}
```

### Preferences Section

Advanced filtering and matching preferences:

```json
{
  "preferences": {
    "company_size": [
      "Startup",
      "Mid-size",
      "Enterprise"
    ],
    "industries": [
      "Technology",
      "FinTech",
      "HealthTech"
    ],
    "avoid_keywords": [
      "unpaid",
      "commission only",
      "MLM"
    ],
    "required_keywords": [],
    "nice_to_have": [
      "equity",
      "health insurance",
      "401k"
    ]
  }
}
```

### Settings Section

System behavior settings:

```json
{
  "settings": {
    "min_match_score": 60,
    "max_jobs_to_analyze": 20,
    "days_back": 1,
    "send_email_if_no_matches": true
  }
}
```

## Field Descriptions

### Profile Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Your full name | "John Doe" |
| `email` | string | Your email address | "john@example.com" |
| `skills` | array | List of your technical skills | ["Python", "AWS"] |
| `experience_years` | number | Years of professional experience | 3 |
| `preferred_locations` | array | Locations you're interested in | ["Remote", "NYC"] |
| `job_titles` | array | Job titles you're looking for | ["Software Engineer"] |
| `job_types` | array | Employment types | ["Full-time", "Contract"] |

### Salary Expectations

| Field | Type | Description |
|-------|------|-------------|
| `min` | number | Minimum acceptable salary |
| `max` | number | Maximum expected salary |
| `currency` | string | Currency code (USD, EUR, etc.) |

### Work Preferences

| Field | Type | Description |
|-------|------|-------------|
| `remote_only` | boolean | Only consider remote positions |
| `willing_to_relocate` | boolean | Open to relocation |
| `visa_sponsorship_required` | boolean | Need visa sponsorship |

### Settings

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `min_match_score` | number | Minimum score to consider a job suitable | 60 |
| `max_jobs_to_analyze` | number | Maximum jobs to analyze per run | 20 |
| `days_back` | number | How many days back to search | 1 |
| `send_email_if_no_matches` | boolean | Send email even with no matches | true |

## Migration from Environment Variables

If you're currently using environment variables, here's how to migrate:

### Old Way (.env)
```env
YOUR_SKILLS=Python,JavaScript,React
YOUR_EXPERIENCE_YEARS=3
YOUR_PREFERRED_LOCATIONS=Remote,San Francisco
YOUR_JOB_TITLES=Software Engineer,Full Stack Developer
```

### New Way (user_profile.json)
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

## Benefits of JSON Configuration

✅ **More Features**: Salary expectations, work preferences, company preferences  
✅ **Better Organization**: Structured data instead of comma-separated strings  
✅ **Easier to Edit**: Clear structure with proper formatting  
✅ **Version Control Friendly**: Easy to track changes  
✅ **Advanced Filtering**: Keywords to avoid, required keywords, nice-to-have features  

## Fallback to Environment Variables

The system still supports environment variables as a fallback. Set `USE_JSON_PROFILE=false` in `.env` to use the old method.

## Examples

See the included `user_profile.json` file for a complete example with all available options.

