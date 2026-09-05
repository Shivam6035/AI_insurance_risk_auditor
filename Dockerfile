

FROM python:3.11-slim

WORKDIR /app

# Install dependencies first
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY app /app/app

# Copy frontend
COPY frontend /app/frontend

# Fail the Docker build immediately if required frontend files are missing
RUN test -f /app/frontend/index.html
RUN test -f /app/frontend/compare.html

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]