# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.8-slim-buster
# FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

COPY data.xlsx /app/storage-engine/data.xlsx

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y python3-tk

RUN pip install openpyxl

# Expose port 5015 for the Flask app to listen on
EXPOSE 5006

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "run.py","--port", "5006"]
