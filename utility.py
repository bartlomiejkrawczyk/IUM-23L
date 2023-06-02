from typing import Any, Dict, Optional, Union, Callable

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import DataFrame, concat, read_csv
from statistics import stdev, mean
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from xgboost import XGBClassifier

USER_ID = 'user_id'

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

DUMMY = 'dummy'
LOGISTIC_REG = 'logistic_regression'
XGB = 'xgb_classifier'
XGB_BEST_ESTIMATOR = 'xgb_classifier_best_estimator'

MODEL_TYPES = [DUMMY, LOGISTIC_REG, XGB, XGB_BEST_ESTIMATOR]

AB_RESULT = ['guess', 'ground_truth', 'model', 'year', 'month', 'user_id']

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
        annot_kws={'fontsize': 7},
        fmt='.0%',
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
        print(f'ROC AUC score for {target}: {roc_auc_score_value}')
        subplot_confusion_matrix(axs[i], y_true, y_predicted)
    plt.show()


def plot_confusion_matrix_ab_experiment(result: Dict[str, DataFrame]):
    _, axs = plt.subplots(1, 2, figsize=(24, 10))  # type: ignore
    for i, target in enumerate(TARGETS):
        roc_auc_score_value = roc_auc_score(
            result[target].ground_truth, result[target].guess
        )
        print(f'ROC AUC score for {target}: {roc_auc_score_value}')
        subplot_confusion_matrix(
            axs[i],
            result[target].ground_truth,
            result[target].guess
        )
    plt.plot()


def subplot_confusion_matrix(ax: Any, y_true: ArrayLike, y_predicted: ArrayLike) -> None:
    matrix = confusion_matrix(y_true, y_predicted)
    sns.heatmap(
        matrix,
        annot=True,
        annot_kws={'fontsize': 30},
        fmt='g',
        xticklabels=['0', '1'],  # type: ignore
        yticklabels=['0', '1'],  # type: ignore
        ax=ax  # type: ignore
    )


def get_params(model: Model) -> Optional[Dict[str, Any]]:
    if isinstance(model, XGBClassifier):
        return model.get_params()
    return None


def retrieve_weights(model: Model) -> np.ndarray[np.float64]:
    if isinstance(model, LogisticRegression):
        return model.coef_[0]
    if isinstance(model, XGBClassifier):
        return model.feature_importances_
    return np.zeros(len(FEATURES))


def plot_feature_importances(models: Dict[str, Model]) -> None:
    _, axs = plt.subplots(
        1,
        len(TARGETS),
        figsize=(30, 10),
        constrained_layout=True
    )
    for i, target in enumerate(TARGETS):
        model = models[target]
        columns = FEATURES
        weights = retrieve_weights(model)
        axs[i].barh(y=columns, width=weights, edgecolor='black')
        axs[i].set_title(
            f'Model: {type} - feature importances for target {target}')
    plt.show()


def compare_models(
        result: DataFrame,
        type_A: str,
        type_B: str,
        buckets: int,
        t_alpha: float,
        s_p: Callable[[float, float], float],
        t: Callable[[float, float, float], float]) -> None:
    for target in TARGETS:
        print(target)
        reality_A: DataFrame = result[type_A][target]
        reality_B: DataFrame = result[type_B][target]

        data = concat([reality_A, reality_B])
        random_ordered_ids = np.random.permutation(
            data['user_id'].unique()  # type: ignore
        )
        size = len(random_ordered_ids) // buckets

        reality_A_score = []
        reality_B_score = []

        for bucket in range(buckets):
            ids = random_ordered_ids[bucket * size:(bucket + 1) * size]
            mask = data['user_id'].isin(ids)
            bucket_data = data.loc[mask]
            reality_A_data = bucket_data.loc[bucket_data['model'] == type_A]
            reality_B_data = bucket_data.loc[bucket_data['model'] == type_B]

            reality_A_score.append(
                roc_auc_score(
                    reality_A_data['ground_truth'],
                    reality_A_data['guess'],
                )
            )
            reality_B_score.append(
                roc_auc_score(
                    reality_B_data['ground_truth'],
                    reality_B_data['guess']
                )
            )

        s_p_value = s_p(stdev(reality_A_score), stdev(reality_B_score))
        if s_p_value != 0:
            t_value = t(
                mean(reality_A_score),
                mean(reality_B_score),
                s_p_value
            )
        else:
            t_value = 0

        print('t_value = ', t_value)
        if t_value > t_alpha:
            print(f'{type_A} is better than {type_B}')
        else:
            print(f'We can\'t say that {type_A} is better than {type_B}')
        print()


SERVICE_PREDICTION_MODEL_INIT = {
    type: {
        target: DataFrame({
            'guess': [],
            'model': [],
            'year': [],
            'month': [],
            'user_id': [],
        })
        for target in TARGETS
    }
    for type in MODEL_TYPES
}


def store_result(result: Dict[str, Dict[str, DataFrame]]) -> None:
    for type in MODEL_TYPES:
        for target in TARGETS:
            result[type][target].to_csv(f'ab_result/{type}-{target}.csv')


def restore_result() -> Dict[str, Dict[str, DataFrame]]:
    result = {}
    for type in MODEL_TYPES:
        result[type] = {}
        for target in TARGETS:
            result[type][target] = read_csv(
                f'ab_result/{type}-{target}.csv'
            )
    return result
