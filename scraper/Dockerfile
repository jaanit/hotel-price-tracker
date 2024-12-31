# ./scraper/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    curl \
    unzip \
    xvfb \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV JUPYTER_RUNTIME_DIR=/tmp/jupyter_runtime
ENV JUPYTER_DATA_DIR=/app/.jupyter

# Create directories
RUN mkdir -p /app/data /app/src /app/notebooks /app/.jupyter

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set up virtual display
RUN Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &

# Make sure directories have correct permissions
RUN chmod -R 777 /app/data /app/.jupyter /tmp

EXPOSE 8888

# Default command moved to docker-compose.yml