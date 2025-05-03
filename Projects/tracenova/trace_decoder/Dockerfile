# Use official Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /tracenova

# Install OS-level dependencies required for pyshark (tshark backend)
RUN apt-get update && \
    apt-get install -y tshark gcc libpcap-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the full monorepo context (make sure you run docker build from the monorepo root)
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r trace_decoder/requirements.txt

# Set PYTHONPATH so that common modules (like common.logger) work
ENV PYTHONPATH=/tracenova

# Expose FastAPI's default port
EXPOSE 8000

# Start the FastAPI app
CMD ["python", "-m", "uvicorn", "trace_decoder.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
