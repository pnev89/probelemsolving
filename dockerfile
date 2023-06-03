FROM python:3.8

ENV PATH="/poetry/bin:$PATH" \
    POETRY_VERSION="1.1.12" \
    SERVICE_HOME="/API"

WORKDIR ${SERVICE_HOME}

COPY ./poetry.lock ${SERVICE_HOME}/
COPY ./pyproject.toml ${SERVICE_HOME}/
COPY ./api ${SERVICE_HOME}/api

RUN apt-get update && apt-get install -y \
    curl python3.8-venv git

RUN curl -s https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py --output /install-poetry.py && \
    POETRY_HOME=/poetry python3 /install-poetry.py && \
    poetry config virtualenvs.in-project true


CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
