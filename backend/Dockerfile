# Base image with Python
FROM python:3.11-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for GeoPandas + Shapely
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    proj-bin \
    libproj-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy and install Python deps
COPY requirements.txt .

# Install Rust toolchain for maturin (needed for some packages)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Upgrade pip and install packages with pre-compiled wheels
RUN pip install --upgrade pip \
    && pip install --only-binary=all -r requirements.txt

# Copy rest of app
COPY . .

# Expose port for Render
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
