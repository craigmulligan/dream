FROM python:3.8.5

USER user

EXPOSE 8080

WORKDIR /home/user/app

RUN pip install --quiet --progress-bar off poetry==1.1.7

# Install dependencies:
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .

CMD ["bash", "./start.sh"]
