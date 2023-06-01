# Inżynieria Uczenia Maszynowego

Studenci:
```
Bartłomiej Krawczyk - 310774
Mateusz Brzozowski - 3106
```

## Temat

W ramach projektu wcielamy się w rolę analityka pracującego dla portalu „Pozytywka” -
serwisu muzycznego, który swoim użytkownikom pozwala na odtwarzanie ulubionych utworów
online. Praca na tym stanowisku nie jest łatwa - zadanie dostajemy w formie enigmatycznego opisu
i to do nas należy doprecyzowanie szczegółów tak, aby dało się je zrealizować. To oczywiście
wymaga zrozumienia problemu, przeanalizowania danych, czasami negocjacji z szefostwem.
Same modele musimy skonstruować tak, aby gotowe były do wdrożenia produkcyjnego -
pamiętając, że w przyszłości będą pojawiać się kolejne ich wersje, z którymi będziemy
eksperymentować.

Jak każda szanująca się firma internetowa, Pozytywka zbiera dane dotyczące swojej działalności - są to:
- lista dostępnych artystów i utworów muzycznych,
- baza użytkowników,
- historia sesji użytkowników,
- techniczne informacje dot. poziomu cache dla poszczególnych utworów.

(analitycy mogą wnioskować o dostęp do tych informacji na potrzeby realizacji zadania)


# Serwis

## Wymagania

W celu odpalenia aplikacji wymagana jest instalacja zależności. Warto to zrobić z wykorzystaniem venv:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Sposób uruchomienia

Bezpośrednie wywołanie skryptu `microservice.py`:
```shell
python ./microservice.py
```

Wywołanie skryptu `microservice.py` za pomocą Flask:
```shell
flask --app microservice run
```

Wywołanie skryptu `microservice.py`:
```shell
./microservice.py
```

## Endpoint-y

- `/predict/<predicting_model>`

Endpoint jest odpowiedzialny za zwracanie predykcji z wybranego modelu. Pozwala użytkownikom przesłać dane do modelu i otrzymać wynik predykcji w odpowiedzi.

Dostępne modele predykcyjne:
- `dummy`
- `logistic_regression`
- `xgb_classifier`
- `xgb_classifier_best_estimator`


- `/ab/`

Służy do przeprowadzenia eksperymentu typu A/B na aplikacji. Pozwala na przetestowanie różnych wariantów, takich jak interfejsy użytkownika, algorytmy lub funkcje, w celu określenia, który z nich zapewnia lepsze rezultaty lub doświadczenie dla użytkowników.

Sposób działania:
1. Dane wejściowe: Podczas przesyłania żądania do endpointu /ab/, przesyłane są dane związane z eksperymentem A/B. Ważnym elementem jest identyfikator rekordu, który umożliwia przypisanie danego użytkownika do odpowiedniego modelu.

2. Wybór modelu: Na podstawie przesłanego identyfikatora rekordu, serwer wybiera odpowiedni model, który zostanie użyty do przeprowadzenia predykcji.

3. Predykcja i zapis danych: Serwer korzysta z wybranego modelu, aby dokonać predykcji na podstawie przesłanych danych. Wynik predykcji jest odsyłany i następnie zapisywany w bazie danych (plik CSV).

- `/init/`

Endpoint pomocniczy służący do wyczyszczenia bazy danych i wczytania jej na nowo może być użyteczny w przypadku konieczności zresetowania lub zaktualizowania danych w systemie.

Sposób działania:
1. Wyczyszczenie bazy danych: Pierwszym krokiem w procesie ponownego wczytania bazy danych jest usunięcie wszystkich istniejących rekordów i danych z bazy danych.

2. Wczytanie nowych danych: Po wyczyszczeniu bazy danych, endpoint może wczytać nowe dane.


### Przykładowe wywołanie:

```
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
```