#!/bin/bash
# Setup script for Study Platform
# This script is idempotent - safe to run multiple times

set -e  # Exit on error

echo "🚀 Setting up Study Platform..."

# Install dependencies first (if not already installed)
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

# Check if .env exists, if not copy from .env.example
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    
    # Generate a random SECRET_KEY if not set or still using placeholder
    CURRENT_KEY=$(grep "^SECRET_KEY=" .env | cut -d'=' -f2)
    if [ "$CURRENT_KEY" = "your-secret-key-here" ]; then
        echo "🔑 Generating random SECRET_KEY..."
        SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
        # Use Python to update the file for cross-platform compatibility
        python -c "
import re
with open('.env', 'r') as f:
    content = f.read()
content = re.sub(r'^SECRET_KEY=.*', 'SECRET_KEY=${SECRET_KEY}', content, flags=re.MULTILINE)
with open('.env', 'w') as f:
    f.write(content)
" SECRET_KEY="$SECRET_KEY"
    fi
    
    # Set DEBUG=True for dev environment using Python for cross-platform compatibility
    python -c "
import re
with open('.env', 'r') as f:
    content = f.read()
content = re.sub(r'^DEBUG=.*', 'DEBUG=True', content, flags=re.MULTILINE)
with open('.env', 'w') as f:
    f.write(content)
"
    echo "✅ .env file created and configured for development"
else
    echo "✅ .env file already exists"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Check if we should create a superuser
if [ "$CREATE_SUPERUSER" = "true" ] || [ "$1" = "--create-superuser" ]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the development server, run:"
echo "  ./scripts/start.sh"
echo ""
echo "Or manually:"
echo "  python manage.py runserver"
echo ""
