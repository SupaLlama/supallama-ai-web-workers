FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy 'start-fastapi' shell script
COPY ./scripts/start-fastapi.sh /start-fastapi.sh
# Convert Windows line endings to Unix line endings via sed
RUN sed -i 's/\r$//g' /start-fastapi.sh
RUN chmod +x /start-fastapi.sh

# Set container directory with the copied source code
WORKDIR /app