# Use official Python image
FROM python:3.13

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
COPY dist ./dist
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY main.py ./

# Expose port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
