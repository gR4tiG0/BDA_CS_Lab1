FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir requests

# Expose a port if needed (not strictly required for just fetching)
EXPOSE 8080

# Run main.py when the container launches
CMD ["python", "main.py"]