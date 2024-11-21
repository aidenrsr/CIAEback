# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application files to the working directory
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Set environment variables (optional)
ENV FLASK_ENV=production
ENV FLASK_APP=app/main.py
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
