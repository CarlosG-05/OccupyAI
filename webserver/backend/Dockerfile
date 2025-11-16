# Use official Python image
FROM python:3.13

WORKDIR /app

# Install dependencies
COPY webserver/backend/requirements.txt .
COPY webserver/backend/dist ./dist
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY webserver/backend/main.py .

# Expose port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
