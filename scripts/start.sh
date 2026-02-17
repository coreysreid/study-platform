#!/bin/bash
# Start script for Study Platform development server
# Checks for git updates, runs migrations, and starts the server

set -e  # Exit on error

echo "🚀 Starting Study Platform development server..."
echo ""

# Check for git updates
echo "🔍 Checking for updates..."
git fetch --quiet 2>/dev/null || true

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

# Check if behind remote
BEHIND=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "0")
if [ "$BEHIND" -gt 0 ]; then
    echo "⚠️  Your branch is $BEHIND commit(s) behind origin/$CURRENT_BRANCH."
    echo "   Run 'git pull' to update."
    echo ""
fi

# Run migrations (in case there are new ones)
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

echo ""
echo "✅ Starting server on http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""

# Start the development server
python manage.py runserver 0.0.0.0:8000
