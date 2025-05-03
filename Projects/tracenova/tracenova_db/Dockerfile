FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    python3-dev \
    cython3 \
    # libpq-dev \                  # PostgreSQL client libraries (commented for MySQL)
    default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy app source code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
