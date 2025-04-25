# Use official Python 3.12.4 slim image
FROM python:3.12.4-slim

# Set working directory inside container
WORKDIR /status-api

# Copy everything from the current directory into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
