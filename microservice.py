#!.venv/bin/python3
import os
import pickle
from typing import Dict

import pandas as pd
from flask import Flask, abort, jsonify, request
from sklearn.pipeline import Pipeline

from utility import FEATURES, MODEL_TYPES, TARGETS, USER_ID, Model

app = Flask(__name__)


class IUMModel:
    pipeline: Pipeline
    target_estimators: Dict[str, Model]

    def __init__(self, pipeline: Pipeline, target_estimators: Dict[str, Model]):
        self.pipeline = pipeline
        self.target_estimators = target_estimators


def load_model(type: str) -> IUMModel:
    with open(f'models/{type}.pkl', 'rb') as f:
        return pickle.load(f)


models_db = {}


def predict(model_type: str, features: pd.DataFrame) -> Dict[str, bool]:
    model = models_db[model_type]
    normalized_data = model.pipeline.transform(features)

    data_frame = pd.DataFrame(
        normalized_data,  # type: ignore
        columns=features.columns
    )

    prediction: Dict[str, bool] = {}
    for target in TARGETS:
        predictor = model.target_estimators[target]
        prediction[target] = bool(
            predictor.predict(data_frame)[0] == 1  # type: ignore
        )

    return prediction


def get_model_type(user_id: int) -> str:
    size = len(MODEL_TYPES)
    reality = hash(str(user_id)) % size
    return MODEL_TYPES[reality]


@app.route('/init/', methods=['POST'])
def initialize():
    initialize_models()
    clear()
    return {'message': 'Success'}


def initialize_models() -> None:
    global models_db
    models_db = {
        type: load_model(type)
        for type in MODEL_TYPES
    }


def clear() -> None:
    for type in MODEL_TYPES:
        for target in TARGETS:
            name = f'ab_experiment/{type}-{target}.csv'
            if os.path.exists(name):
                os.remove(name)
            pd.DataFrame({
                'guess': [],
                'model': [],
                'year': [],
                'month': [],
                'user_id': [],
            }).to_csv(name, index=False)


@app.route('/ab/', methods=['POST'])
def ab_experiment_endpoint():
    data = pd.json_normalize(request.json)  # type: ignore
    row = data.iloc[0]
    id: int = row[USER_ID]  # type: ignore
    model_type = get_model_type(id)
    features = data[FEATURES]
    prediction = predict(model_type, features)
    print(model_type, id)
    for target in TARGETS:
        pd.DataFrame({
            "guess": [1 if prediction[target] else 0],
            "model": [model_type],
            "year": [int(row['year'])],  # type: ignore
            "month": [int(row['month'])],  # type: ignore
            "user_id": [int(id)],
        }).to_csv(
            f'ab_experiment/{model_type}-{target}.csv',
            mode='a',
            index=False,
            header=False
        )
    return jsonify(prediction)


@app.route('/predict/<predicting_model>', methods=['POST'])
def predict_endpoint(predicting_model: str):
    if predicting_model not in models_db.keys():
        abort(404)
    data = pd.json_normalize(request.json)[FEATURES]  # type: ignore
    prediction = predict(predicting_model, data)
    return jsonify(prediction)


if __name__ == '__main__':
    initialize_models()
    app.run(debug=True)
