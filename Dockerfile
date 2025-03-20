# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /Major

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .