# Use the official lightweight Python image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure stdout/stderr are logged immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create a non-root user and group for security
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (if needed by underlying libraries like PyTorch/parsers)
# RUN apt-get update && apt-get install -y --no-install-recommends \

#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the actual application code
COPY ./app ./app

# Transfer ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port the FastAPI server will run on
EXPOSE 8000

# Start the FastAPI server using Uvicorn

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]