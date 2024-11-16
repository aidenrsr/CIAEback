# Base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy the application code into the container
COPY . .

# Expose port (default for Flask)
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
