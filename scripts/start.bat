@echo off
REM Start script for Study Platform development server (Windows)
REM Checks for git updates, runs migrations, and starts the server

echo Starting Study Platform development server...
echo.

REM Check for git updates
echo Checking for updates...
git fetch --quiet 2>nul

REM Get current branch
for /f "tokens=*" %%a in ('git rev-parse --abbrev-ref HEAD 2^>nul') do set CURRENT_BRANCH=%%a
if "%CURRENT_BRANCH%"=="" set CURRENT_BRANCH=main

REM Check if behind remote
for /f "tokens=*" %%a in ('git rev-list --count HEAD..@{u} 2^>nul') do set BEHIND=%%a
if "%BEHIND%"=="" set BEHIND=0

if %BEHIND% GTR 0 (
    echo WARNING: Your branch is %BEHIND% commit(s) behind origin/%CURRENT_BRANCH%.
    echo          Run 'git pull' to update.
    echo.
)

REM Run migrations
echo Running database migrations...
python manage.py migrate --noinput

echo.
echo Server starting on http://localhost:8000
echo Press Ctrl+C to stop
echo.

REM Start the development server
python manage.py runserver 0.0.0.0:8000
