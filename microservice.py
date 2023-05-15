from flask import Flask, request, jsonify
from sklearn.pipeline import Pipeline
from sklearn.base import ClassifierMixin
from pandas.io.json import json_normalize
import pandas as pd
import pickle
from typing import Dict

app = Flask(__name__)

TARGETS = [
    "premium_user_numerical",
    "will_buy_premium_next_month_numerical"
]


class IUMModel:
    pipeline: Pipeline
    predictors: Dict[str, ClassifierMixin]
    thresholds: Dict[str, float]

    def __init__(self, pipeline: Pipeline, predictors: Dict[str, ClassifierMixin], thresholds: Dict[str, float]):
        self.pipeline = pipeline
        self.predictors = predictors
        self.thresholds = thresholds


@app.route("/predict/", methods=['POST'], defaults={'predicting_model': 'xgbclassifier'})
@app.route("/predict/<predicting_model>", methods=['POST'])
def main(predicting_model: str):
    with open(f"models/{predicting_model}.pkl", "rb") as f:
        model: IUMModel = pickle.load(f)

        data = json_normalize(request.json)  # type: ignore
        normalized_data = model.pipeline.transform(data)

        data_frame = pd.DataFrame(normalized_data, columns=data.columns)

        prediction = {}
        for target in enumerate(TARGETS):
            predictor = model.predictors[target]
            probability: float = predictor.predict_proba(  # type: ignore
                data_frame
            )[0][1]
            prediction[target] = bool(probability > model.thresholds[target])

        return jsonify(prediction)


if __name__ == "__main__":
    app.run(debug=True)
