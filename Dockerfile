FROM python:3.9-slim

<<<<<<< HEAD:backend/Dockerfile
# Update package lists
RUN apt-get -q -y update 

# Install GCC for compiling Python packages with native extensions
RUN apt-get install -y gcc

# define enviroment variables and working directory
# USERNAME 바꿔도 됨
ENV USERNAME= ciae

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
# application code directory
COPY ciae-main ciae-main
COPY requirements.txt .
COPY service_entrypoint.sh .

'''
create the container user
(with the username we defined before)
and gives it the needed permissions
'''

# create a new user and group
RUN groupadd ${USERNAME} && useradd -g ${USERNAME} ${USERNAME}
# change ownership of the working directory
RUN chown -R ${USERNAME}:${USERNAME} /app
# set permissions for the working directory
RUN chmod -R u=rwx,g=rwx /app
# switch to user
USER ${USERNAME}
# update path for pip installations
ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

'''
install python packages
'''

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
