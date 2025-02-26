FROM python:3.12-slim-bookworm 

# Environment variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.8.4

# Create a non-root user
RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

# Install system dependencies
RUN apt-get update && apt-get install python3-dev gcc build-essential libpq-dev -y

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy application files
COPY pyproject.toml /home/user/app/
COPY *poetry.lock /home/user/app/

# Set working directory
WORKDIR /home/user/app/

# Set permissions for the application directory
RUN chmod -R ugo+w /home/user/app/

# Install Python dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Set working directory for the backend
WORKDIR /home/user/app/backend

# Copy backend code and scripts
COPY backend/ /home/user/app/backend

# Ensure scripts are executable
RUN chmod +x scripts/django-entrypoint.sh 
RUN chmod +x scripts/wait-script.sh
# Switch to non-root user
USER user

# Set ENTRYPOINT to the initialization script
ENTRYPOINT ["sh", "scripts/django-entrypoint.sh"]
# Set default command
CMD gunicorn core.wsgi --log-file - -b 0.0.0.0:8000 --reload --workers 2 --timeout 120 --max-requests 1000 --max-requests-jitter 50