FROM --platform=$BUILDPLATFORM python:3.12-alpine

# Working directory in the container
WORKDIR /app

# Copy the required files into the container
COPY ./src /app

# Installing Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Execute Python script when container is launched
CMD ["python", "geocode.py"]