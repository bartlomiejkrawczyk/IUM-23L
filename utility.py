from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from typing import Any, Union
from xgboost import XGBClassifier

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
    'average_daily_cost',
]

TARGETS = [
    "premium_user_numerical",
    "will_buy_premium_next_month_numerical"
]

BUCKETS_CNT = 10
T_ALPHA = 2.101

DUMMY = 'dummy'
LOGISTIC_REG = 'logistic_regression'
XGB = 'xgb_classifier'
XGB_BEST_ESTIMATOR = 'xgb_classifier_best_estimator'
RANDOM = 'randomized_search'

MODEL_TYPES = [DUMMY, LOGISTIC_REG, XGB, XGB_BEST_ESTIMATOR]

ArrayLike = Any

Model = Union[
    DummyClassifier,
    LogisticRegression,
    XGBClassifier
]
