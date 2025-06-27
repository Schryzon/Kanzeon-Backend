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

# Copy requirements
COPY requirements-nocuda.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-nocuda.txt

# Copy your project files
COPY . .

# Create tmp directory for uploads
RUN mkdir -p ./tmp

# Expose the port
EXPOSE 4706 8501

# Default to backend; override in compose for frontend
CMD ["python3", "backend.py"]

# If you want - I recommend using docker-compose
# RUN pip install honcho
# RUN printf "backend: python backend.py\nfrontend: streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0\n" > Procfile
# CMD ["honcho", "start", "-f", "Procfile"]