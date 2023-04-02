
**Artists**
- GENRES - array<string>
- ID - string
- NAME - string

**Sessions** 
- EVENT_TYPE - string
- SESSION_ID - bigint
- TIMESTAMP - string
- TRACK_ID - string
- USER_ID - bigint

**Track Storage**
- DAILY_COST - double
- STORAGE_CLASS - string
- TRACK_ID - string

**Tracks**
- ACOUSTICNESS - double
- DANCEABILITY - double
- DURATION_MS - bigint
- ENERGY - double
- EXPLICIT - bigint
- ID - string
- ID_ARTIST - string
- INSTRUMENTALNESS - double
- KEY - bigint
- LIVENESS - double
- LOUDNESS - double
- NAME - string
- POPULARITY - bigint
- RELEASE_DATE - string
- SPEECHINESS - double
- TEMPO - double
- VALENCE - double

**Users**
- CITY - string
- FAVOURITE_GENRES - array<string>
- NAME - string
- PREMIUM_USER - boolean
- STREET - string
- USER_ID - bigint

```mermaid
erDiagram
    ARTIST {
        string id
        string name
        array-string genres
    }

    SESSION {
        int session_id
        int user_id
        string track_id
        string event_type
        timestamp timestamp
    }


    TRACK {
        string id
        string id_artist
        
        string name
        bigint duration_ms
        
        string release_date

        bigint explicit
        bigint key
        bigint popularity
        
        double acousticness
        double danceability
        double energy
        double instrumentalness
        double liveness
        double loudness
        double speechiness
        double tempo
        double valence
    }

    ARTIST ||--o{ TRACK: creates
    TRACK ||--|| TRACK_STORAGE : stores
    SESSION }o--o| TRACK: plays


    TRACK_STORAGE {
        string track_id
        string storage_class
        double daily_cost
    }

    USER {
        int user_id
        boolean premium_user
        string name
        string city
        array-string favourite_genres
    }

    USER ||--o{ SESSION : listens_to
```