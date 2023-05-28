#!/bin/bash

curl --location 'http://127.0.0.1:5000/predict/xgb_classifier_best_estimator' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": 0,
    "month": 1,
    "year": 2023,
    "number_of_advertisements": 0,
    "number_of_tracks": 0,
    "number_of_skips": 0,
    "number_of_likes": 0,
    "number_of_liked_tracks_listened": 0,
    "number_of_tracks_in_favourite_genre": 0,
    "total_number_of_favourite_genres_listened": 0,
    "average_popularity_in_favourite_genres": 0,
    "total_tracks_duration_ms": 0,
    "number_of_different_artists": 0,
    "average_release_date": 0,
    "average_duration_ms": 0,
    "explicit_tracks_ratio": 0,
    "average_popularity": 0,
    "average_acousticness": 0,
    "average_danceability": 0,
    "average_energy": 0,
    "average_instrumentalness": 0,
    "average_liveness": 0,
    "average_loudness": 0,
    "average_speechiness": 0,
    "average_tempo": 0,
    "average_valence": 0,
    "average_track_name_length": 0,
    "average_daily_cost": 0
}'