from flask import Flask, request, jsonify
from sklearn.pipeline import Pipeline
from sklearn.base import ClassifierMixin
from io import StringIO
import pandas as pd
import pickle

app = Flask(__name__)

TARGETS = [
    "premium_user_numerical",
    "will_buy_premium_next_month_numerical"
]

class IUMModel:
    pipeline: Pipeline
    model: ClassifierMixin
    threshold: float

    def __init__(self, pipeline, model, threshold):
        self.pipeline = pipeline
        self.model = model
        self.threshold = threshold


@app.route("/predict", methods=['POST'])
def main():
    with open("models/xgbclassifier.pkl", "rb") as f:
        model: IUMModel = pickle.load(f)

        data = pd.io.json.json_normalize(request.json)
        normalized_data = model.pipeline.transform(data)

        data_frame = pd.DataFrame(normalized_data, columns=data.columns)

        prediction = {}
        for i, target in enumerate(TARGETS):
            prediction[target] = bool(model.model.predict_proba(data_frame)[:, i][0] > model.threshold)

        return jsonify(prediction)


if __name__ == "__main__":
    app.run(debug = True)