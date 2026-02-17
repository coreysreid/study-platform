# Development container for Study Platform
FROM mcr.microsoft.com/devcontainers/python:3.12

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create media directory
RUN mkdir -p media

# Expose Django dev server port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBUG=True \
    DJANGO_SETTINGS_MODULE=study_platform.settings

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
