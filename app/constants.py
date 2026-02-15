import os

MODEL_NAME = os.getenv('MODEL_NAME', "iris_rf_model")
MODEL_STAGE = os.getenv('MODEL_STAGE', "latest")

REDIS_HOST = os.getenv('REDIS_HOST', "localhost")

