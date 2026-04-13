FROM dhi.io/python:3.13-dev AS builder

WORKDIR /app

ENV PATH="/app/venv/bin:$PATH"

RUN python -m venv /app/venv

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    /app/venv/bin/pip install -r requirements.txt

RUN useradd -u 10001 -m appuser


FROM dhi.io/python:3.13

WORKDIR /app

ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY --from=builder --chown=10001:10001 /app/venv /app/venv
COPY --chown=10001:10001 app/ ./app/

USER 10001

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]