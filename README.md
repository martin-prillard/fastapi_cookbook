# FastAPI ML API with Monitoring

A complete example of serving a machine learning model with FastAPI, monitored using Prometheus and Grafana.

## Overview

This project demonstrates how to:
- Serve a machine learning model using FastAPI
- Monitor API performance and metrics with Prometheus
- Visualize metrics with Grafana dashboards
- Set up a complete monitoring stack using Docker Compose

## Architecture

The project consists of three main services:

1. **FastAPI Application** - Serves the ML model and exposes metrics
2. **Prometheus** - Collects and stores time-series metrics
3. **Grafana** - Visualizes metrics through dashboards

```
┌──────────┐     ┌─────────────┐     ┌─────────┐
│  FastAPI │────▶│ Prometheus  │────▶│ Grafana │
│  :8000   │     │   :9090     │     │  :3000  │
└──────────┘     └─────────────┘     └─────────┘
     │
     │ /metrics
     │
     ▼
```

### What is Prometheus?

Prometheus is an open-source monitoring and alerting toolkit. It collects metrics from your applications and stores them as time-series data.

### What is Grafana?

Grafana is an open-source analytics and visualization platform. It connects to data sources (like Prometheus) and creates beautiful dashboards.

### What is Locust?

Locust is an open-source load testing tool that allows you to simulate user behavior and test how your API performs under different load conditions. It provides a web-based UI to start tests and monitor results in real-time.

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)

### Running the Stack

1. Clone this repository
2. Start all services:
```bash
docker compose up --build
```

This will:
- Build the FastAPI application with the trained model
- Start Prometheus to collect metrics
- Start Grafana with pre-configured dashboards

3. Access the services:
   - **FastAPI Swagger UI**: http://localhost:8000/docs
   - **Prometheus UI**: http://localhost:9090
   - **Grafana**: http://localhost:3000 (admin/admin)
   - **Locust Web UI**: http://localhost:8089

### Running Load Tests

1. **Access Locust Web UI**: Open http://localhost:8089 in your browser

2. **Configure and start a test**:
   - **Number of users**: Number of concurrent users to simulate (e.g., 10, 50, 100)
   - **Spawn rate**: How many users to add per second (e.g., 2 users/second)
   - Click **"Start swarming"** to begin the test

3. **Monitor the test**:
   - **Statistics tab**: See request statistics, response times, and failure rates
   - **Charts tab**: View real-time charts of requests per second and response times
   - **Failures tab**: See any failed requests
   - **Exceptions tab**: View any exceptions that occurred

4. **Stop the test**: Click **"Stop"** when you want to end the test


## API Endpoints

### `GET /`
Health check endpoint. Returns a status message.

### `POST /predict`
Makes a prediction using the trained Iris classifier.

**Request body:**
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

### `GET /metrics`
Exposes Prometheus metrics in the format Prometheus expects. This endpoint is scraped by Prometheus.

## Development

### Local Development (without Docker)

1. Install dependencies:
```bash
uv sync
```

2. Train the model:
```bash
uv run python train_model.py
```

3. Run the API:
```bash
uv run uvicorn app.main:app --reload
```
