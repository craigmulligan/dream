FROM python:3.8.5

ARG UID=1000
ENV USER=app_user
RUN useradd -u $UID -ms /bin/bash $USER

EXPOSE 8000

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTEST_ADDOPTS="--color=yes"
ENV AWS_CONFIG_FILE=/root/.aws/config
ENV AWS_ENDPOINT_URL="http://127.0.0.1:9228"
USER app_user 

WORKDIR app

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["chalice", "local", "--host", "0.0.0.0"]
