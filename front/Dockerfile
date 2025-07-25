# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13.0
FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Устанавливаем зависимости (ещё под root)
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Копируем код (ещё под root)
COPY . .

RUN python manage.py collectstatic --noinput --clear --verbosity 3
# Даем appuser права на /app
RUN chown -R appuser:appuser /app

# Теперь переключаемся на appuser
USER appuser

EXPOSE 8000