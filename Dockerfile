FROM python:3.9-slim

# Update package lists
RUN apt-get -q -y update 

# Install GCC for compiling Python packages with native extensions
RUN apt-get install -y gcc

# define enviroment variables and working directory

# Set working directory
WORKDIR /backend

# Copy requirements file and install dependencies
# application code directory
COPY ciae-main ciae-main
COPY requirements.txt .
COPY service_entrypoint.sh .

RUN pip install --upgrade pip
# install packages
RUN pip install --no-cache-dir -r requirements.txt
# flask environment variable
ENV FLASK_APP=ciae-main
# make service entrypoint executable
RUN chmod +x service_entrypoint.sh

# Expose port (default for Flask)
EXPOSE 5000
RUN flask db init

ENTRYPOINT [ "./service_entrypoint.sh" ]
# # Set environment variables for Flask
# ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0
# Set environment variables for Flask
ENV FLASK_APP=backend/main.py
ENV FLASK_RUN_HOST=0.0.0.0

# # Run the Flask app
# CMD ["flask", "run"]
