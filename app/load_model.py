import mlflow

model_name = "iris_rf_model"
stage = "latest"

MODEL_URI = f"models:/{model_name}/{stage}"

model = None

def load_model():
    global model
    if model is None:
        model = mlflow.pyfunc.load_model(MODEL_URI)
    return model