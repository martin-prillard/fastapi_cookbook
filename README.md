# FastAPI ML API with Monitoring

A complete example of serving a machine learning model with FastAPI, featuring MLflow model management, async batch processing with Celery, monitoring with Prometheus/Grafana, and load testing with Locust.

## Architecture

```
┌──────────┐     ┌─────────────┐     ┌─────────┐
│  FastAPI │────▶│ Prometheus  │────▶│ Grafana │
│  :8000   │     │   :9090     │     │  :3000  │
└──────────┘     └─────────────┘     └─────────┘
     │
     │ /metrics
     │
     ▼
┌──────────┐     ┌──────────┐
│  Celery  │────▶│  Redis   │
│  Worker  │     │  :6379   │
└──────────┘     └──────────┘
     │
     │
     ▼
┌──────────┐
│  MLflow  │
│  Server  │
└──────────┘
```

**Components:**
- **FastAPI** - REST API serving Iris classification model
- **MLflow** - Model registry and tracking (external server)
- **Celery + Redis** - Async batch processing
- **Prometheus** - Metrics collection
- **Grafana** - Metrics visualization
- **Locust** - Load testing

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ with `uv` package manager
- MLflow tracking server (configure `MLFLOW_TRACKING_URI`)

### Running the Stack

```bash
docker compose up --build
```

**Services:**
- FastAPI API: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- Locust: http://localhost:8089

### Running the Tutorial Notebook

The `enonce.ipynb` notebook provides a step-by-step tutorial covering:

1. **Model Training** - Train an Iris classifier with MLflow
2. **FastAPI Setup** - Create REST API with Pydantic models
3. **Async Processing** - Add Celery tasks for batch predictions
4. **Load Testing** - Use Locust for performance testing
5. **Deployment** - Canary and A/B testing strategies

**To launch:**
```bash
# Install dependencies
uv sync

# Start Jupyter
uv run jupyter notebook enonce.ipynb

# Or use JupyterLab
uv run jupyter lab enonce.ipynb
```

**Note:** Ensure MLflow tracking server is running and accessible at the URI configured in the notebook.

## API Endpoints

### `POST /predict`
Single prediction using the Iris classifier model from MLflow.

**Request:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "prediction": 0
}
```

### `POST /predict_batch`
Async batch prediction. Returns a task ID.

**Request:** Array of `IrisInput` objects

**Response:**
```json
{
  "task_id": "abc123..."
}
```

### `GET /predict_batch/{task_id}`
Get batch prediction results.

**Response:**
```json
{
  "status": "done",
  "predictions": [0, 1, 2]
}
```

### `GET /metrics`
Prometheus metrics endpoint (scraped by Prometheus).

### `GET /`
Health check endpoint.

## Development

### Local Setup

1. Install dependencies:
```bash
uv sync
```

2. Configure environment:
   - Set `MLFLOW_TRACKING_URI` in `.env` or environment
   - Ensure Redis is running for Celery: `docker run -p 6379:6379 redis`

3. Run FastAPI:
```bash
uv run uvicorn main:app --reload
```

4. Run Celery worker (for async tasks):
```bash
uv run celery -A app.celery_app.celery worker --pool=solo --loglevel=info
```

### Load Testing

Access Locust UI at http://localhost:8089:
- Configure users and spawn rate
- Monitor real-time statistics and charts
- View failures and exceptions
