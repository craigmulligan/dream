# syntax = docker/dockerfile:experimental
FROM python:3.8.5

ARG USER_ID
ARG GROUP_ID

# Avoid file permission issues for container user files that are written to host volume.
RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

EXPOSE 8080

RUN echo $USER_ID
RUN echo $GROUP_ID

RUN mkdir -p /home/user/.pytest/cache

ENV VIRTUAL_ENV=/home/user/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTEST_ADDOPTS="--color=yes"
# This is so we wipe the file on every container run.
ENV TESTMON_DATAFILE=/home/user/.testmondata

WORKDIR /home/user/app

RUN pip install --quiet --progress-bar off poetry==1.1.7

# Install dependencies:
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,mode=0755,target=/root/.cache poetry install

COPY . .

CMD ["gunicorn run:app"]
