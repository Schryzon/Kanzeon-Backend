# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /kanzeon

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
    poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Optional: Install Indonesian language for Tesseract (if needed)
# RUN apt-get install -y tesseract-ocr-ind

# Copy requirements if you have it
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files
COPY . .

# Expose the port
EXPOSE 4706

# Run the app
CMD ["python", "api.py"]