#!/bin/bash
# Check for git updates and notify if branch is behind remote

git fetch --quiet 2>/dev/null || true

BEHIND=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "0")
if [ "$BEHIND" -gt 0 ]; then
    echo "⚠️  Your branch is $BEHIND commit(s) behind origin. Run 'git pull' to update."
fi
