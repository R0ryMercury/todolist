FROM python:3.10-alpine
LABEL creator="R0ryMercury"

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY todolist todolist/
