FROM python:3.12-slim

WORKDIR /app

# Install codemunch-pro from PyPI
RUN pip install --no-cache-dir codemunch-pro

# Create data directory for SQLite databases
RUN mkdir -p /root/.codemunch-pro

# Expose default HTTP port
EXPOSE 5002

ENTRYPOINT ["codemunch-pro"]
