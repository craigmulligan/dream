# Fetch the LiteFS binary using a multi-stage build.
FROM flyio/litefs:0.2 AS litefs

# Final python app
FROM python:3.10-alpine

COPY --from=litefs /usr/local/bin/litefs /usr/local/bin/litefs

RUN apk add build-base

RUN apk add bash curl fuse sqlite

EXPOSE 8080

WORKDIR /home/user/app

RUN pip install --quiet --progress-bar off poetry==1.1.7

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

COPY etc/litefs-worker.yml /etc/
COPY etc/litefs-web.yml /etc/

RUN mkdir -p /data /mnt/data
