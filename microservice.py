#!.venv/bin/python3
from flask import Flask, request, jsonify, abort
from sklearn.pipeline import Pipeline
from utility import FEATURES, TARGETS, MODEL_TYPES, Model  # type: ignore
import pandas as pd
import pickle
from typing import Dict

app = Flask(__name__)


class IUMModel:
    pipeline: Pipeline
    target_estimators: Dict[str, Model]

    def __init__(self, pipeline: Pipeline, target_estimators: Dict[str, Model]):
        self.pipeline = pipeline
        self.target_estimators = target_estimators


def load_model(type: str) -> IUMModel:
    with open(f"models/{type}.pkl", "rb") as f:
        return pickle.load(f)


models = {}

# TODO: redirect by user id to specific model for prediction
# TODO: store prediction for future use
# TODO: add endpoint for retrieving results for given month


@app.route("/predict/<predicting_model>", methods=['POST'])
def predict(predicting_model: str):
    if predicting_model not in models.keys():
        abort(404)

    model = models[predicting_model]

    data = pd.json_normalize(request.json)[FEATURES]  # type: ignore
    normalized_data = model.pipeline.transform(data)

    data_frame = pd.DataFrame(normalized_data, columns=data.columns)

    prediction = {}
    for target in TARGETS:
        predictor = model.target_estimators[target]
        prediction[target] = bool(
            predictor.predict(data_frame)[
                0] == 1  # type: ignore
        )

    return jsonify(prediction)


if __name__ == "__main__":
    models = {
        type: load_model(type)
        for type in MODEL_TYPES
    }
    app.run(debug=True)
