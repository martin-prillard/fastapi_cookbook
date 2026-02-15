import numpy as np
from app.celery_app import celery
from app.load_model import load_model


@celery.task(name="predict_batch_task")
def predict_batch_task(batch):
    model = load_model()

    features = [
        [
            item["sepal_length"],
            item["sepal_width"],
            item["petal_length"],
            item["petal_width"],
        ]
        for item in batch
    ]

    preds = model.predict(np.array(features))
    return [int(p) for p in preds]
