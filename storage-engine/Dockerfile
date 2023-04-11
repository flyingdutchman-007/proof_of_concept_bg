# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

COPY data.xlsx /app/storage-engine/data.xlsx

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN pip install openpyxl

# Expose port 5015 for the Flask app to listen on
EXPOSE 5006

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "run.py"]
