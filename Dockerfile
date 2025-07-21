FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY . .

RUN chmod +x ./app/scripts/prestart.sh

CMD ["sh", "-c", "uv run ./app/scripts/prestart.sh && uv run fastapi run app/main.py --host 0.0.0.0 --port 8000"]
