# Use a base image with Python and system tools
FROM python:3.11-slim

# Install system dependencies (GDAL, PROJ, GEOS)
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    proj-bin \
    proj-data \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy code
COPY . .

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
