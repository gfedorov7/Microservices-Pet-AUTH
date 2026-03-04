FROM python:3.13-slim

EXPOSE 8000

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY auth-api/pyproject.toml auth-api/poetry.lock ./

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.in-project true

RUN /root/.local/bin/poetry install --no-root

COPY . .

RUN chmod +x local_entrypoint.sh

CMD ["./local_entrypoint.sh"]