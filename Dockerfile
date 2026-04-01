FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies with uv
RUN uv sync

# Set default duration to 10s if not provided
ENV DURATION=60s

# Run the application with the duration parameter
ENTRYPOINT ["sh", "-c", "uv run python -m container_app_job_playground --duration $DURATION"]
