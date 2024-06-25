FROM python:3.9-alpine3.13
LABEL maintainer="victorvld"

ENV PYTHONUNBUFFERED 1

COPY requeriments.txt /tmp/requeriments.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && /py/bin/pip install --upgrade pip && /py/bin/pip install -r /tmp/requeriments.txt && rm -rf /tmp && adduser --disabled-password --no-create-home django-user

# Update the PATH variable in our OS so that we don't need to call the full path to execute python commands
ENV PATH="/py/bin:$PATH"

# Change the user
USER django-user