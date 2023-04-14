# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.8-slim-buster
# FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y python3-tk

# Expose port 5015 for the Flask app to listen on
EXPOSE 5010

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "server.py"]
