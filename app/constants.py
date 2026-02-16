import os

MLFLOW_HOST = "http://89.58.44.97:5000/"

MODEL_NAME = os.getenv('MODEL_NAME', "iris_rf_model")
MODEL_STAGE = os.getenv('MODEL_STAGE', "latest")

REDIS_HOST = os.getenv('REDIS_HOST', "localhost")

