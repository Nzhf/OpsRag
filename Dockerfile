FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better layer caching on rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code, ingestion scripts, frontend, and the data files
# the agent tools read at runtime (inventory / defect-log JSON).
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY static/ ./static/
COPY data/ ./data/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
