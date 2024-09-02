# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy the script
COPY . /app

# Create a folder to store downloaded files
RUN mkdir -p /app/downloads
RUN mkdir -p /app/box

# Install ffmpeg for pydub
RUN apt-get update && apt-get install -y ffmpeg

# Install any needed packages
RUN pip install --no-cache-dir fastapi uvicorn nltk requests pydub
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab

# Make port 8000 available to the world outside this container
EXPOSE 8006

# Command to run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006"]
