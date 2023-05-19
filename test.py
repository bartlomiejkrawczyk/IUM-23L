import itertools
import numpy as np
import pandas as pd
import pickle
import requests
import seaborn as sns

from IPython.display import display
from matplotlib import pyplot as plt
from math import sqrt
from scipy.stats import uniform
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import (
    confusion_matrix,
    roc_auc_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from statistics import stdev, mean
from typing import Any, Dict, Optional
from xgboost import XGBClassifier

from microservice import IUMModel
from utility import Model

FEATURE_VERSION = 'v1'
FEATURE_PATH = f'features/{FEATURE_VERSION}/feature.csv'

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
    'premium_user_numerical',
    'will_buy_premium_next_month_numerical'
]

TARGET_AND_FEATURES = TARGETS + FEATURES

data_frame = pd.read_csv(FEATURE_PATH)

pipeline = Pipeline([
    ("simple_imputer", SimpleImputer()),
    ("standard_scaler", StandardScaler())
])

TRAINING_UP_TO = 2023
TRAIN_DATA: pd.DataFrame = data_frame.loc[data_frame.year < TRAINING_UP_TO, :]
TEST_DATA: pd.DataFrame = data_frame.loc[data_frame.year >= TRAINING_UP_TO, :]
TEST_SIZE = 0.33

X_train_temp, X_test_temp, Y_train, Y_test = train_test_split(
    TRAIN_DATA[FEATURES],
    TRAIN_DATA[TARGETS],
    test_size=TEST_SIZE
)
X_train_temp: pd.DataFrame
X_test_temp: pd.DataFrame
Y_train: pd.DataFrame
Y_test: pd.DataFrame

train_data = pipeline.fit_transform(X_train_temp)
test_data = pipeline.transform(X_test_temp)
X_train = pd.DataFrame(train_data, columns=FEATURES)
X_test = pd.DataFrame(test_data, columns=FEATURES)

params = {
    'objective': 'binary:logistic',
    'gamma': 0.23,
    'max_depth': 3,
    'n_estimators': 52,
    'scale_pos_weight': 1.6311744635573293 * 1.6311744635573293,
    'eta': 0.01
}

model = XGBClassifier(**params).fit(X_train, Y_train[TARGETS[0]])


_, axs = plt.subplots(1, 2, figsize=(24, 10))  # type: ignore
for i, target in enumerate(TARGETS):
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
