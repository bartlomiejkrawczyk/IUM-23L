
VIEWS = {
    'artists': "../data/v1/artists.jsonl",
    'sessions': "../data/v1/sessions.jsonl",
    'track_storage': "../data/v1/track_storage.jsonl",
    'tracks': "../data/v1/tracks.jsonl",
    'users': "../data/v1/users.jsonl",
}

NUMBER_COLUMNS = {
    'artists': [],
    'sessions': ['session_id',  'user_id'],  # timestamp
    'track_storage': ['daily_cost'],
    'tracks': [
        'acousticness',
        'danceability',
        'duration_ms',
        'energy',
        'explicit',
        'instrumentalness',
        'key',
        'liveness',
        'loudness',
        'popularity',
        'speechiness',
        'tempo',
        'valence'
    ],
    'users': ['user_id'],
}


LIST_COLUMNS = {
    'artists': ['genres'],
    'sessions': [],
    'track_storage': [],
    'tracks': [],
    'users': ['favourite_genres'],
}

DATE_FORMAT = "yyyy-MM-dd'T'HH:mm:ss[.SSSSSS]"
