FROM python:3.8.5

EXPOSE 8000

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTEST_ADDOPTS="--color=yes"
ENV AWS_CONFIG_FILE=/root/.aws/config

WORKDIR app

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["chalice", "local", "--host", "0.0.0.0"]
