import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from constants import MODEL_NAME, MLFLOW_HOST

mlflow.set_tracking_uri(MLFLOW_HOST)
mlflow.set_experiment("iris_classification")

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

with mlflow.start_run():
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)

    mlflow.log_metric("accuracy", acc)

    signature = infer_signature(X_train, model.predict(X_train))
    input_example = X_train[:5]

    mlflow.sklearn.log_model(
        sk_model=model,
        name="model",
        signature=signature,
        input_example=input_example,
        registered_model_name=MODEL_NAME
    )
