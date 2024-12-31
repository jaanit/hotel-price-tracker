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
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV JUPYTER_RUNTIME_DIR=/tmp/jupyter_runtime
ENV JUPYTER_DATA_DIR=/app/.jupyter
ENV PYTHONPATH=/app
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create virtual environment
RUN python -m venv /app/venv

# Create directories
RUN mkdir -p /app/data /app/src /app/notebooks /app/.jupyter

# Install Python packages in virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up virtual display
RUN Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &

# Make sure directories have correct permissions
RUN chmod -R 777 /app/data /app/.jupyter /tmp

EXPOSE 8888