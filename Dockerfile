
FROM python:3.12-slim

# Set working directory
WORKDIR /FastAPI

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only the necessary files for installing dependencies
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

ENV PYTHONPATH="/FastAPI/src:$PYTHONPATH"

# Expose the port FastAPI will run on
EXPOSE 8000 

# Command to run the FastAPI application with Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--reload"]