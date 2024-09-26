# Pull base image
FROM python:3.12.6-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set work directory
WORKDIR /app

# Copy the dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev

COPY start.sh ./
RUN chmod +x ./start.sh

# Copy the application code
COPY ./code .

