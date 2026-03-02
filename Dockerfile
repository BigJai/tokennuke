FROM python:3.12-slim

WORKDIR /app

# Install tokennuke from PyPI
RUN pip install --no-cache-dir tokennuke

# Create data directory for SQLite databases
RUN mkdir -p /root/.tokennuke

# Expose default HTTP port
EXPOSE 5002

ENTRYPOINT ["tokennuke"]
