# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to avoid unnecessary cache invalidation
COPY requirements.txt .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire Miaul application into the container
COPY . .

# Expose ports for HTTP and WebSocket servers
EXPOSE 8000
EXPOSE 8765

# Run the Miaul application
CMD ["python", "miaul.py"]
