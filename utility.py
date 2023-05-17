import pandas as pd
import numpy as np
import os

from sklearn.dummy import DummyClassifier
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from typing import Dict, List, Tuple, Any, Union
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


def load_data() -> pd.DataFrame:
    xgb_results = pd.read_csv(os.path.join("results", "xgb.csv"))
    logreg_results = pd.read_csv(os.path.join("results", "logic.csv"))
    data = pd.concat([xgb_results, logreg_results], axis=0)
    return data.rename(
        columns={"guess": "pred", "ground_truth": "true", "model": "variant"}
    )


def get_buckets_indices(user_ids: np.ndarray) -> List[List[int]]:
    buckets_indices = [[] for _ in range(BUCKETS_CNT)]
    for user_id in user_ids:
        bucket = np.random.randint(0, BUCKETS_CNT)
        buckets_indices[bucket].append(user_id)
    return buckets_indices


def get_xgb_logreg_f1_scores(
    data: pd.DataFrame, buckets_indices: List[List[int]]
) -> Tuple[List[float], List[float]]:
    xgb_f1_scores, logreg_f1_scores = [], []
    for bucket in buckets_indices:
        tmp_data = data.loc[data.user_id.isin(bucket), :]
        xgb_data = tmp_data.loc[tmp_data.variant == "xgbclassifier", :]
        logreg_data = tmp_data.loc[tmp_data.variant ==
                                   "logistic_regression", :]
        xgb_f1_scores.append(f1_score(xgb_data.true, xgb_data.pred))
        logreg_f1_scores.append(f1_score(logreg_data.true, logreg_data.pred))
    return xgb_f1_scores, logreg_f1_scores


def get_s_p(xgb_f1_scores: List[float], logreg_f1_scores: List[float]) -> float:
    return np.sqrt(
        (
            (BUCKETS_CNT - 1) * np.std(xgb_f1_scores) ** 2
            + (BUCKETS_CNT - 1) * np.std(logreg_f1_scores) ** 2
        )
        / (BUCKETS_CNT * 2 - 2)
    )


def get_t(
    xgb_f1_scores: List[float], logreg_f1_scores: List[float], s_p: float
) -> float:
    return (np.mean(xgb_f1_scores) - np.mean(logreg_f1_scores)) / (
        s_p * np.sqrt(1 / BUCKETS_CNT + 1 / BUCKETS_CNT)
    )


def is_xgb_better(t: float) -> bool:
    return t > T_ALPHA


def main():
    data = load_data()
    buckets_indices = get_buckets_indices(data.user_id.values)
    xgb_f1_score, logreg_f1_score = get_xgb_logreg_f1_scores(
        data, buckets_indices)
    s_p = get_s_p(xgb_f1_score, logreg_f1_score)
    t = get_t(xgb_f1_score, logreg_f1_score, s_p)
    if is_xgb_better(t):
        print("XGBClassifier is better than LogisticRegression")
    else:
        print("We can't say that XGBClassifier is better than LogisticRegression")


if __name__ == "__main__":
    main()
