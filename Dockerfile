#Base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]