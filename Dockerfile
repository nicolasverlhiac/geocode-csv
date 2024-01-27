ARG PYTHON_VERSION=3.12
FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION}-alpine

# Working directory in the container
WORKDIR /app

# Copy the required files into the container
COPY ./src /app

# Installing Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    # adduser --system --group --no-create-home geocode
    adduser -D geocode sudo

# Set non-root user for better security
USER geocode

# Execute Python script when container is launched
CMD ["python", "-m", "geocode"]