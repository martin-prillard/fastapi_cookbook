"""
FastAPI ML API for Iris Flower Classification.

This module provides a RESTful API for predicting Iris flower species
using a pre-trained machine learning model. The API includes Prometheus
metrics for monitoring request counts and latency.

Endpoints:
    GET /status: Health check endpoint
    POST /predict: Predict Iris flower species from input features
    GET /metrics: Prometheus metrics endpoint
"""
import time
from typing import Dict, List

from celery.result import AsyncResult
from fastapi import HTTPException
import numpy as np
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.celery_app import celery
from app.constants import MODEL_STAGE
from app.data_models import IrisInput
from app.load_model import load_model
from app.monitor import REQUEST_COUNT, REQUEST_LATENCY
from app.tasks import predict_batch_task

app = FastAPI(title="Iris ML API", version="1.0")
model = load_model()

@app.get("/status")
def status() -> Dict[str, str]:
    """
    Status endpoint for health check.

    Returns a simple message indicating that the API is running.
    This endpoint can be used to verify that the service is up
    and responding to requests.

    Returns:
        Dict[str, str]: A dictionary containing a status message.

    Example:
        >>> response = {"status": "OK"}
    """
    return {"status": "OK"}


@app.post("/predict")
def predict(data: IrisInput) -> Dict[str, int]:
    """
    Predict Iris flower species from input features.

    This endpoint accepts the four Iris flower measurements (sepal and
    petal dimensions) and returns the predicted species class. The
    prediction is performed using a pre-trained machine learning model.

    The endpoint tracks metrics:
        - Total request count (incremented for each request)
        - Request latency (measured in seconds)

    Args:
        data: IrisInput model containing the four flower measurements.

    Returns:
        Dict[str, int]: A dictionary containing the predicted class.
            The prediction is an integer representing the species:
            - 0: Setosa
            - 1: Versicolor
            - 2: Virginica

    Raises:
        HTTPException: If the prediction fails or input validation fails.
            Status code 400 with error details.

    Example:
        >>> input_data = IrisInput(
        ...     sepal_length=5.1,
        ...     sepal_width=3.5,
        ...     petal_length=1.4,
        ...     petal_width=0.2
        ... )
        >>> response = predict(input_data)
        >>> # Returns: {"prediction": 0}
    """
    REQUEST_COUNT.inc()
    start = time.time()
    try:
        features = [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width,
        ]]
        pred = int(model.predict(np.array(features))[0])
        return {"prediction": pred, "model_stage": MODEL_STAGE}
    except Exception as e:
        raise e
    finally:
        REQUEST_LATENCY.observe(time.time() - start)


@app.post("/predict_batch")
async def predict_batch(data: List[IrisInput]):
    task = predict_batch_task.delay([item.model_dump() for item in data])
    return {"task_id": task.id}


@app.get("/predict_batch/{task_id}")
async def get_batch_result(task_id: str):
    task = AsyncResult(task_id, app=celery)

    if task.state == "PENDING":
        return {"status": "pending"}

    if task.state == "FAILURE":
        raise HTTPException(status_code=500, detail=str(task.result))

    if task.state == "SUCCESS":
        return {"status": "done", "predictions": task.result}
    return {"status": task.state}



@app.get("/metrics")
def metrics() -> Response:
    """
    Prometheus metrics endpoint.

    Returns metrics in Prometheus format that can be scraped by
    a Prometheus server. This endpoint exposes various metrics
    including request counts and latency histograms.

    Returns:
        Response: HTTP response containing Prometheus-formatted metrics
            with content type 'text/plain; version=0.0.4; charset=utf-8'.

    Example:
        The response will contain metrics like:
        # HELP api_requests_total Total number of API requests
        # TYPE api_requests_total counter
        api_requests_total 42.0
        # HELP api_request_latency_seconds Request latency in seconds
        # TYPE api_request_latency_seconds histogram
        ...
    """
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
