# Use an official Python image as base
FROM python:3.10.6-buster

# Set the working directory
WORKDIR /app

# Copy the necessary files
COPY requirements.txt requirements.txt
COPY api/ api/
COPY qrbill/ qrbill/
COPY .env .env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 8080

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "2", "api.api:app"]
