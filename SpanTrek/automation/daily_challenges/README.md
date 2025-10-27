# Daily Challenges Automation

This directory contains automation scripts and configuration for creating daily challenges for all SpanTrek users at specified time.

## Scripts

-   `run_daily_challenges.bat` - Windows batch script to run the Django management command
-   `run_daily_challenges.ps1` - PowerShell script with better error handling and logging

## Setup Instructions

-   `django_crontab_setup.txt` - Instructions for using django-crontab (Linux/Mac)
-   `celery_setup.txt` - Instructions for using Celery Beat (production environments)

## Logs

-   `daily_challenges.log` - Log file created by the scripts (auto-generated)

## Current Setup

✅ **Windows Task Scheduler** is configured to run `run_daily_challenges.bat` every day at 7:00 AM.

### Management Commands

The Django management command is located at:
`SpanTrek/base/management/commands/create_daily_challenges.py`

### Manual Execution

To run manually:

```bash
# From SpanTrek directory
python manage.py create_daily_challenges
```

### Scheduled Task Management

```powershell
# View the scheduled task
schtasks /query /tn "SpanTrek Daily Challenges"

# Run manually for testing
schtasks /run /tn "SpanTrek Daily Challenges"

# Delete the task
schtasks /delete /tn "SpanTrek Daily Challenges" /f

# Recreate the task
schtasks /create /tn "SpanTrek Daily Challenges" /tr "d:\Wojtek\SpanTrek\SpanTrek\automation\daily_challenges\run_daily_challenges.bat" /sc daily /st 07:00 /f
```

## How It Works

1. **Windows Task Scheduler** runs the batch script daily at 7:00 AM
2. **Batch script** navigates to the Django project directory and runs the management command
3. **Management command** calls `create_daily_challenges()` method for all users in the database
4. **User model method** randomly selects 3 daily challenges from the DailyChallenge model
5. **Results** are logged to `daily_challenges.log`
