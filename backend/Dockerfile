# Base image with Python
FROM python:3.11-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal system dependencies for Shapely
RUN apt-get update && apt-get install -y \
    libgeos-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy and install Python deps
COPY requirements.txt .

# Upgrade pip and install packages
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy rest of app
COPY . .

# Expose port for Render
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
