VERSION = 'v2'


VIEWS = {
    'artists': f"../data/{VERSION}/artists.jsonl",
    'sessions': f"../data/{VERSION}/sessions.jsonl",
    'track_storage': f"../data/{VERSION}/track_storage.jsonl",
    'tracks': f"../data/{VERSION}/tracks.jsonl",
    'users': f"../data/{VERSION}/users.jsonl",
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
