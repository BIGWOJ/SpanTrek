@echo off
REM Script to run daily challenges creation

cd /d "d:\Wojtek\SpanTrek\SpanTrek"
python manage.py create_daily_challenges

REM Log the execution with timestamp
echo %date% %time% - Daily challenges created >> "d:\Wojtek\SpanTrek\SpanTrek\automation\daily_challenges\daily_challenges.log"