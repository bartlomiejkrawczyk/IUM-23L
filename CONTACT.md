
## Pierwszy kontakt z klientem

Jakiś czas temu wprowadziliśmy konta premium, które uwalniają użytkowników od słuchania reklam.
Nie są one jednak jeszcze zbyt popularne - czy możemy się dowiedzieć, które osoby są bardziej skłonne do zakupu takiego konta?

## Nasze pierwsze pytania w stronę klienta

> Czy system oferuje jedynie jedną ofertę konta premium, czy może istnieją jakieś różne dostępne oferty?

System oferuje tylko jedną ofertę konta premium

> Czy konto premium można dzielić?

Nie 

> Co chcieli by państwo uzyskać wykorzystując nasz system i jakie mają Państwo oczekiwania co do systemu?

 

> Jak duży jest państwa system? Ilu użytkowników korzysta z niego?

System obsługuje obecnie ok. 50 tys. użytkowników

> Czy dostępna jest jakaś historia puszczanych reklam?

Co Państwo rozumiecie przez historię puszczanych reklam?

> Jak często puszczane są reklamy użytkownikom, którzy nie posiadają konta premium? Czy macie dostępną listę dostępnych reklam?

Reklamy zmieniają się w zależności od konkretnych umów z innymi podmiotami. Za dobór częstotliwości reklam odpowiada nasz autorski algorytm.

> Jakiej postaci dane mają Państwo dostępne? Czy moglibyśmy uzyskać wszystkie dostępne dane, a my wybierzemy z nich co nas interesuje?

Dane dostępne są w formacie plików JSON, podsyłam je w załączeniu

> Czy udostępnią nam Państwo dane już zagregowane do postaci jednej tabeli, czy też udostępnią je Państwo w formacie np. JSON, albo czy udostępnią je jako kilka plików CSV, które my już zagregujemy?

j.w.

> Czy możemy dostać schemat utrzymywanych danych, może jakaś klasa, schemat z bazy, UML?

Niestety nie posiadamy takich schematów

> Czy powinniśmy wiedzieć coś więcej na temat procesu zbierania przez Państwa danych? Jak Państwa system działa w przypadku błędu w czasie transakcji? Czy całe zapytanie do systemu jest wykonywane w ramach jednej transakcji? Czy może się zdarzyć, że jedynie częściowo zostanie zapisane? Czy programy działające na różnych systemach / przeglądarkach działają identycznie i w identyczny sposób zbierają dane? Czy jednak są pewne różnice w sposobie zbierania?

Możecie Państwo założyć, że dane, które od nas otrzymujecie są uwspólnione, a ew. różnice wynikające ze sposobu ich zbierania zostały usunięte.

> Czy mają już Państwo istniejący system, który stara się przewidzieć kto jest skłonny do zakupu konta premium, jeżeli tak, to czy możemy uzyskać dostęp do takiego rozwiązania?

Nie posiadamy takiego systemu

> Czy możemy założyć, że Pan będzie naszym ekspertem domenowym? Czy raczej mamy, założyć, że to my jesteśmy ekspertami?

Tak, możemy się tak umówić


## Ocena danych


>> Jak duży jest państwa system? Ilu użytkowników korzysta z niego?

> System obsługuje obecnie ok. 50 tys. użytkowników

W takim wypadku, czy jesteśmy wstanie otrzymać dane dotyczące wszystkich 50 tyś. użytkowników oraz ich sesji. W danych które otrzymaliśmy znajduje się jedynie 50 użytkowników.


W którym roku została założona "Pozytywka"?

Na pierwszy rzut oka widzimy w danych bardzo dużo identyfikatorów o "id": -1. Czym to jest spowodowane? Czy to jest problem w czasie wykonywania "dump-a" bazy danych? Czy może ten problem wynika z jakiegoś błędu w czasie zapisu do bazy i jest nie do uniknięcia?

Podobnie w pliku `sessions.jsonl` jak mamy interpretować null w kolumnie "user_id". Czy to wynika z niekompletnych danych w bazie, czy może podobnie jak w pytaniu wyżej z trefnego "dump-a" bazy danych?


### Users

+------+
|length|
+------+
|    50|
+------+

Mało użytkowników.

> "favourite_genres": null

Favourite_genres powinno być listą. Co to oznacza? Czy to oznacza, że użytkownik nie zdefiniował jeszcze ulubionych gatunków? 

Z czego to wynika? Może jest to stare konto? Albo błąd w czasie zapisu/odczytu?

> "premium_user": null

Premium_user powinno być booleanem. W kolumnie tej nie widzimy wartości false, a za to występują nulle. 

> "premium_user": false - 0 takich użytkowników

Chcielibyśmy uzyskać także dane użytkowników nie premium, aby mieć porównanie.

> "id": -1

5 użytkowników ma pole o nazwie "id". Czy to pole o czymś świadczy? Czy może pozostało z jakiejś starej wersji systemu?

### Sessions

> "user_id": null

> "track_id": null

Generalnie jest mało danych:

+-------------+------+
|   event_type|length|
+-------------+------+
|         null|   181|
|ADVERTISEMENT|    28|
|  BUY_PREMIUM|    49|
|         LIKE|   595|
|         PLAY|  2157|
|         SKIP|   795|
+-------------+------+

Ale dodatkowo chcielibyśmy uzyskać więcej danych na temat ADVERTISEMENT i BUY_PREMIUM.

## Artists

> "genres": null

W 1352 przypadkach występuje null.

> "id": -1

W 1371 przypadkach.

## Sessions

Tylko 3805.

> "event_type": null

Co oznacza? Wystąpił 181 razy.


> timestamp

- prosimy o dłuższy zakres

> "track_id": null

W 200 przypadkach.

> "track_id": ""

> "user_id": null

W 183 przypadkach.

## Track Storage

> storage_class

Czemu tylko 4 rekordy dla przypadku "FAST". Czy popsuł się wam szybki cache?

## Tracks

> "acousticness": 0.0

W 12 przypadkach?

> "danceability": 0.0

W 48 przypadkach

> "speechiness": 0.0

W 48 przypadkach

> "tempo": 0.0

W 48 przypadkach

> "valence": 0.0

W 51 przypadkach

> "energy": 0.0

W 9 przypadkach

Przypadki zerowe korelują ze sobą, jeśli w jednej kolumnie jest 0.0 to w innych często też jest.

> "id": null

W 6530 przypadkach

> "id_artist": null

W 6504 przypadkach

> "instrumentalness": 0.0

W 46190 przypadkach!

> "key" - co to oznacza

jest 12 klas tej grupy

> "liveness": 0.0

W 9 przypadkach

> "loudness" < 0

Co oznacza loudness na minusie? Czy to jest wartość w decybelach?


+------+-----+-----+------------------+
| count|  min|  max|           average|
+------+-----+-----+------------------+
|129648|-60.0|4.362|-9.734177465136398|
+------+-----+-----+------------------+

Czemu taka nierównowaga?

> "name": null

W 6547 przypadków

> "popularity": null

W 6469 przypadków

> "release_date"

czasami w tej kolumnie jest rok YYYY, a czasami data YYYY-MM-DD

> "duration_ms"

Wartość 4995083ms to w przybliżeniu 1.387523056h - trochę długo jak na utwór. No chyba, że jakaś składanka.


# Pytania na ten etap

>> Co chcieli by państwo uzyskać wykorzystując nasz system i jakie mają Państwo oczekiwania co do systemu?

Czy mamy przewidywać czy dany użytkownik kupi konto premium? Czy może określić, cechy które sygnalizują, że użytkownik chce kupić takie konto?

Czy docelowy system ma wskazywać na to z czego wynika zakup konta premium na podstawie danych? Czy raczej API powinno przewidywać czy dany użytkownik jest skłonny do zakupu takiego konta?

TODO: Czy mają Państwo pewne wymagania biznesowe co do predykcji naszego modelu?

W jaki sposób Państwo chcą wykorzystać przygotowane przez nas API? Czy my mamy ustalić format danych przyjmowanych / odsyłanych przez nasze api? Czy jest jakiś narzucony z góry?

Czy mają Państwo jakieś wymagania niefunkcjonalne co do API? Czy mamy zapewnić bezpieczeństwo (HTTPS)? Czas odpowiedzi? Maksymalna przepustowość? Ograniczenia na zużycie zasobów? Czy mamy jakąś narzuconą technologię? Pyton? Java?

Jak bardzo mamy się skupiać na wyjaśnieniu predykcji naszego modelu? Czy mamy jedynie określić przynależność danego użytkownika? Czy raczej ustalić dlaczego wybraliśmy tak, a nie inaczej?

W jaki sposób system będzie wykorzystywany? W jaki sposób będzie testowany?

Rozumiemy, że w naszym rozwiązaniu mamy się skupić na **transparentność/zdolność wyjaśniania predykcji/ruch XAI (eXplainable AI),**



