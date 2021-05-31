FROM python:3.8.5

EXPOSE 8000

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTEST_ADDOPTS="--color=yes"
# Creds for aws 
ENV AWS_CONFIG_FILE=/root/.aws/config
# This is so we wipe the file on every container run.
ENV TESTMON_DATAFILE=/root/.testmondata

WORKDIR app

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["chalice", "local", "--host", "0.0.0.0"]
