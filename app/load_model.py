import mlflow

from app.constants import MODEL_NAME, MODEL_STAGE

MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"

model = None

def load_model():
    global model
    if model is None:
        model = mlflow.pyfunc.load_model(MODEL_URI)
    return model