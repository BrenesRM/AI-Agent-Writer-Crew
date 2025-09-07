# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional NLP dependencies and download NLTK data
RUN pip install --no-cache-dir pydantic-settings nltk textblob mammoth && \
    python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p logs outputs/final_novel outputs/character_guide outputs/story_library outputs/video_prompts \
    rag/documents rag/processed rag/vectorstore data/sessions

# Set environment variables for proper encoding and Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Expose port for Streamlit
EXPOSE 8501

# Default command - can be overridden
CMD ["python", "-c", "print('AI Agent Writer Crew ready! Use docker-compose to run specific services.')"]