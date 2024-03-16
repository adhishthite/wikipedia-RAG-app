# Use an official Python runtime as a parent image
FROM python:3.12
LABEL authors="adhishthite"

# Install Nginx
RUN apt-get update &&  \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# First, copy only the requirements.txt file
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Setup Nginx to forward requests to Gunicorn
COPY nginx.conf /etc/nginx/sites-available/default

# Make port 8000 available to the world outside this container
EXPOSE 8000
EXPOSE 80

# Run app.py when the container launches
CMD service nginx start && gunicorn --workers 8 app.app:app --bind unix:/app/app.sock
