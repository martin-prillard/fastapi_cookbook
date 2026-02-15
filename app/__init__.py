import mlflow
from app.constants import MLFLOW_HOST

mlflow.set_tracking_uri(MLFLOW_HOST)
