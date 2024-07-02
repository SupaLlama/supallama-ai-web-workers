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
COPY ./compose/local/fastapi/entrypoint.sh /entrypoint.sh
# Convert Windows line endings to Unix line endings via sed
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy shell script
COPY ./compose/local/fastapi/start.sh /start.sh
# Convert Windows line endings to Unix line endings via sed
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

# Copy shell script
COPY ./compose/local/fastapi/celery/worker/start.sh /start-celeryworker.sh
# Remove all carriage returns from the file via sed
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

# Copy shell script
COPY ./compose/local/fastapi/celery/beat/start.sh /start-celerybeat.sh
# Remove all carriage returns from the file via sed
RUN sed -i 's/\r$//g' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

# Copy shell script
COPY ./compose/local/fastapi/celery/flower/start.sh /start-flower.sh
# Remove all carriage returns from the file via sed
RUN sed -i 's/\r$//g' /start-flower.sh
RUN chmod +x /start-flower.sh

# Location in the container where we copied the source code
WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
