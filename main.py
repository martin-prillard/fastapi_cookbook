from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import joblib
import time

app = FastAPI(title="Iris ML API", version="1.0")

model = joblib.load("model.joblib")

REQUEST_COUNT = Counter("api_requests_total", "Total API requests")
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency (seconds)")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "FastAPI ML API is running"}

@app.post("/predict", status_code=status.HTTP_200_OK)
def predict(data: IrisInput):
    REQUEST_COUNT.inc()
    start = time.time()
    try:
        features = [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]]
        pred = int(model.predict(features)[0])
        return {"prediction": pred}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        REQUEST_LATENCY.observe(time.time() - start)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
