# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 8050 for the Dash app to listen on
EXPOSE 8050

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
