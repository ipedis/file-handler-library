# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install the project dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the working directory
COPY . /app
COPY demo/.env /app/.env

ENV PYTHONPATH=/app

# Set the entry point for the container
ENTRYPOINT ["poetry", "run", "python", "demo/main.py"]