FROM python:3.8-slim

ARG ENVIRON

ENV ENVIRON=${ENVIRON} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0 \
  WORKER_CLASS=uvicorn.workers.UvicornH11Worker

# Copy only requirements to cache them in docker layer:
WORKDIR /acebook
COPY requirements.txt /acebook/

# Project initialization:
RUN pip install -r requirements.txt

# Creating folders, and files for a project:
COPY . /acebook

# Setting start comand to python server.py:
ENTRYPOINT ["./docker-entrypoint.sh"]
