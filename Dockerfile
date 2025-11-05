# Use Python 3.13 slim image for smaller size
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies via UV
RUN uv sync

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port for MCP server (if running in server mode)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD uv run python -c "from main import mcp; print('healthy')" || exit 1

# Default command - run the MCP server
CMD ["uv", "run", "python", "main.py"]

# Labels for metadata
LABEL maintainer="Darbot Labs <labs@darbot.io>"
LABEL description="Darbot-Windows-MCP - Lightweight MCP Server for Windows Desktop Automation"
LABEL version="0.1.0"
LABEL org.opencontainers.image.source="https://github.com/darbotlabs/Darbot-Windows-MCP"