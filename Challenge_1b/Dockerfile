FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy everything into /app
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "analyze_pdfs.py"]
