from flask import Flask, request, jsonify
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from xgboost import XGBClassifier
from utility import OptimalThresholdXGBClassifier
import pandas as pd
import pickle
from typing import Dict, Union

app = Flask(__name__)

DUMMY = 'dummy'
LOGISTIC_REG = 'logistic_regression'
XGB = 'xgb_classifier'
RANDOM = 'randomized_search'

MODEL_TYPES = [DUMMY, LOGISTIC_REG, XGB, RANDOM]

TARGETS = [
    "premium_user_numerical",
    "will_buy_premium_next_month_numerical"
]

FEATURES = [
    'number_of_advertisements',
    'number_of_tracks',
    'number_of_skips',
    'number_of_likes',
    'number_of_liked_tracks_listened',
    'number_of_tracks_in_favourite_genre',
    'total_number_of_favourite_genres_listened',
    'average_popularity_in_favourite_genres',
    'total_tracks_duration_ms',
    'number_of_different_artists',
    'average_release_date',
    'average_duration_ms',
    'explicit_tracks_ratio',
    'average_popularity',
    'average_acousticness',
    'average_danceability',
    'average_energy',
    'average_instrumentalness',
    'average_liveness',
    'average_loudness',
    'average_speechiness',
    'average_tempo',
    'average_valence',
    'average_track_name_length',
    'average_daily_cost'
]

Model = Union[
    DummyClassifier,
    LogisticRegression,
    XGBClassifier,
    OptimalThresholdXGBClassifier
]


class IUMModel:
    pipeline: Pipeline
    target_estimators: Dict[str, Model]

    def __init__(self, pipeline: Pipeline, target_estimators: Dict[str, Model]):
        self.pipeline = pipeline
        self.target_estimators = target_estimators


def load_model(type: str) -> IUMModel:
    with open(f"models/{type}.pkl", "rb") as f:
        return pickle.load(f)


MODELS = {
    type: load_model(type)
    for type in MODEL_TYPES
}


@app.route("/predict/<predicting_model>", methods=['POST'])
def main(predicting_model: str):
    model = MODELS[predicting_model]

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
    app.run(debug=True)
