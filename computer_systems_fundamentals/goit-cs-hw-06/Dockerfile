# ---------------------------------------------------------------------------
# Dockerfile for the Python web + socket application
# ---------------------------------------------------------------------------
# Base image: official Python 3.14 slim variant for a small footprint
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies first (layer is cached if requirements.txt
# does not change, making rebuilds faster)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and templates/static assets
COPY main.py .
COPY templates/ templates/
COPY static/ static/

# Expose ports:
#   3000 — HTTP web server
#   5000 — UDP socket server (declare for documentation purposes; UDP is
#           typically handled at the host/compose network level)
EXPOSE 3000
EXPOSE 5000/udp

# Run the application
CMD ["python", "main.py"]
