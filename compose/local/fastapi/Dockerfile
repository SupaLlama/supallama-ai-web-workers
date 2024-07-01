FROM python:3.12-slim-bookworm

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

# Copy shell script
COPY ./compose/local/fastapi/entrypoint /entrypoint
# Convert Windows line endings to Unix line endings via sed
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# Copy shell script
COPY ./compose/local/fastapi/start /start
# Convert Windows line endings to Unix line endings via sed
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Copy shell script
COPY ./compose/local/fastapi/celery/worker/start /start-celeryworker
# Remove all carriage returns from the file via sed
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

# Copy shell script
COPY ./compose/local/fastapi/celery/beat/start /start-celerybeat
# Remove all carriage returns from the file via sed
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

# Copy shell script
COPY ./compose/local/fastapi/celery/flower/start /start-flower
# Remove all carriage returns from the file via sed
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# Location in the container where we copied the source code
WORKDIR /app

ENTRYPOINT ["/entrypoint"]