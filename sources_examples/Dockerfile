FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY sources_examples/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./sources_examples /app

# Expose the port FastAPI is running on
EXPOSE 8043

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8043"]
