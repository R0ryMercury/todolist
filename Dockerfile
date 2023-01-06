FROM python:3.10-alpine
LABEL creator="R0ryMercury"

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY /todolist/docker-entrypoint.sh .
RUN sed -i 's/\r$//g' /code/docker-entrypoint.sh
RUN chmod +x /code/docker-entrypoint.sh

COPY todolist todolist/

ENTRYPOINT [ "/code/docker-entrypoint.sh" ]