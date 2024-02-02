# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    geos-dev \
    libc-dev

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Define the command to run your FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
