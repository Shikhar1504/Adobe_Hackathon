# Use an AMD64-compatible lightweight Python base
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install required system packages for PyMuPDF (fitz)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your PDF processing script and data folder structure
COPY process_pdfs.py .
COPY sample_dataset/ sample_dataset/

# Run the script on container start
CMD ["python", "process_pdfs.py"]
