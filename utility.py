from typing import Any, Dict, Optional, Union

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
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

TARGET_AND_FEATURES = TARGETS + FEATURES

DUMMY = 'dummy'
LOGISTIC_REG = 'logistic_regression'
XGB = 'xgb_classifier'
XGB_BEST_ESTIMATOR = 'xgb_classifier_best_estimator'

MODEL_TYPES = [DUMMY, LOGISTIC_REG, XGB, XGB_BEST_ESTIMATOR]

ArrayLike = Any

Model = Union[
    DummyClassifier,
    LogisticRegression,
    XGBClassifier
]


def plot_matrix(matrix: DataFrame) -> None:
    plt.figure(figsize=(16, 16))

    sns.heatmap(
        matrix,
        xticklabels=matrix.columns,  # type: ignore
        yticklabels=matrix.columns,  # type: ignore
        annot=True,
        annot_kws={"fontsize": 7},
        fmt=".0%",
        vmin=-1,
        vmax=1,
    )

    plt.show()


def construct_dummy(X_train: DataFrame,
                    y_train: DataFrame,
                    params: Optional[Dict[str, Any]] = None) -> DummyClassifier:
    return DummyClassifier().fit(X_train, y_train)


def construct_logistic_reggression(X_train: DataFrame,
                                   y_train: DataFrame,
                                   params: Optional[Dict[str, Any]] = None) -> LogisticRegression:
    return LogisticRegression().fit(X_train, y_train)


def plot_confusion_matrix(models: Dict[str, Model], X_test: DataFrame, Y_test: DataFrame) -> None:
    _, axs = plt.subplots(1, 2, figsize=(24, 10))  # type: ignore
    for i, target in enumerate(TARGETS):
        model = models[target]
        y_predicted = model.predict(X_test)
        y_true = Y_test[target]
        roc_auc_score_value = roc_auc_score(y_true, y_predicted)
        print(f"ROC AUC score for {target}: {roc_auc_score_value}")
        matrix = confusion_matrix(y_true, y_predicted)
        sns.heatmap(
            matrix,
            annot=True,
            annot_kws={"fontsize": 30},
            fmt='g',
            xticklabels=["0", "1"],  # type: ignore
            yticklabels=["0", "1"],  # type: ignore
            ax=axs[i]  # type: ignore
        )
    plt.show()


def retrieve_weights(model: Model) -> np.ndarray[np.float64]:
    if isinstance(model, LogisticRegression):
        return model.coef_[0]
    if isinstance(model, XGBClassifier):
        return model.feature_importances_
    return np.zeros(len(FEATURES))


def plot_feature_importances(models: Dict[str, Model]) -> None:
    _, axs = plt.subplots(1, len(TARGETS), figsize=(
        30, 10), constrained_layout=True)
    for i, target in enumerate(TARGETS):
        model = models[target]
        columns = FEATURES
        weights = retrieve_weights(model)
        axs[i].barh(y=columns, width=weights, edgecolor="black")
        axs[i].set_title(
            f"Model: {type} - feature importances for target {target}")
    plt.show()
