FROM python:3.13-slim

WORKDIR /app
COPY app/ app/
COPY pyproject.toml pyproject.toml

RUN pip install --no-cache-dir uv && uv sync

RUN uv run python app/train_model.py

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
