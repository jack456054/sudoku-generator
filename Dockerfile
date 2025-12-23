FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Configure poetry to not create virtual env (install globally in container)
RUN poetry config virtualenvs.create false

WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies (no dev dependencies)
RUN poetry install --without dev --no-interaction --no-ansi --no-root

# Copy application code
COPY src ./src
COPY README.md ./

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PORT=8080

# Expose port (Cloud Run sets environment variable PORT, typically 8080)
EXPOSE 8080

# Run the application using Gunicorn
# Adjust worker count and timeout as needed
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 sudoku.app:app
