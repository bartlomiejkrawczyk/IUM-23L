
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

## Ocena danych v1 oraz odpowiedź klienta

> 1. System obsługuje ok. 50 tyś. użytkowników, czy jesteśmy w ostanie otrzymać dane dotyczące wszystkich 50 tyś. Użytkowników oraz ich sesji, ponieważ otrzymaliśmy dane jedyne 50 użytkowników.

Myślę, że jestem w stanie dać Państwu dostęp do danych ok. 20k użytkowników, czy taka ilość danych byłaby ok?

> 2. W kolumanch znajduje się dużo identyfikatorów o "id": -1. Czym to jest spowodowane? Czy to jest problem w czasie wykonywania "dump-a" bazy danych? Czy może ten problem wynika z jakiegoś błędu w czasie zapisu do bazy i jest nie do uniknięcia?
> 
> 3. Podobnie w pliku sessions.jsonl jak mamy interpretować null w kolumnie "user_id". Czy to wynika z niekompletnych danych w bazie, czy może podobnie jak w pytaniu wyżej z trefnego "dump-a" bazy danych?
> 
> 4. Favourite_genres zawiera rekordy null, co to oznacza? Czy to oznacza, że użytkownik nie zdefiniował jeszcze ulubionych gatunków? Z czego to wynika? Może jest to stare konto? Albo błąd w czasie zapisu/odczytu?
> 
> 5. "premium_user" zawiera rekordy null. W tej kolumnie nie widzimy wartości false, a za to występują nulle. Chcielibyśmy uzyskać także dane użytkowników nie premium, aby mieć porównanie.
> 
> 6. 5 użytkowników ma pole o nazwie "id". Czy to pole o czymś świadczy? Czy może pozostało z jakiejś starej wersji systemu?
> 
> 7. W sessions, user_id oraz track_id są nullami, szczególnie gdy event_type jest ustawione na ADVERTISEMENT lub BUY_PREMIUM, co to oznacza?
> 
> 9. event_type zawiera rekordy null, co to oznacza?
> 
> 12. Czemu tylko 4 rekordy dla przypadku "FAST". Czy popsuł się wam szybki cache?
> 
> 13. W tracks, acousticness, danceability, speechiness, tempo, valence, energy są zerami, co to oznacza oraz dlaczego zerowe przypadki korelują ze sobą? Jeśli w jednej kolumnie jest 0.0 to w innych często też jest.
> 14. W tracks kolumny id, id_artists zaeirają nulle, co to oznacza?

Te błędy wkradły się w dane przy okazji łączenia danych z różnych systemów, mogę podesłać nową, poprawioną paczkę.

> 8. W sessions jest mało danych oraz dodatkowo chcielibyśmy uzyskać więcej danych na temat ADVERTISEMENT i BUY_PREMIUM.

Co to dokładnie znaczy "więcej danych"?

> 10. timestamp jest krótki, czy możemy uzyskać dane z dłuższym zakresem?

O jakim zakresie mówimy?

> 11. Gdzie przechowujecie reklamy? Czy macie jakąś wydzieloną bazę danych?

Reklamy są przechowywane w chmurze. Obawiam się, że nie możemy podzielić się ich treścią.

> 15. Co oznacza kolumna key w tracks oraz instrumentalness, która jest 0 w bardzo dużej ilości przypadków?

key: liczby w https://en.wikipedia.org/wiki/Pitch_class

instrumentalness: przewidywanie czy utwór posiada wokal, im bliżej 1.0 tym wyższe prawdopodobieństwo, że utwór jest instrumentalny. Wartości powyżej 0.5 można traktować jak utwory instrumentalne

> 16. Co oznacza loudness na minusie? Czy to jest wartość w decybelach?

średnia głośność w decybelach, typowo od -60 do 0dB

> 17. Czy mamy przewidywać czy dany użytkownik kupi konto premium? Czy może określić, cechy które sygnalizują, że użytkownik chce kupić takie konto?
> 
> 18. Czy docelowy system ma wskazywać na to z czego wynika zakup konta premium na podstawie danych? Czy raczej API powinno przewidywać czy dany użytkownik jest skłonny do zakupu takiego konta?

Chodzi tu raczej o przewidzenie czy dany użytownik jest skłonny do zakupu takiego konta

> 19. W jaki sposób Państwo chcą wykorzystać przygotowane przez nas API? Czy my mamy ustalić format danych przyjmowanych / odsyłanych przez nasze api? Czy jest jakiś narzucony z góry?

Możecie Państwo sami ustalić format danych przyjmowanych/odsyłanych

> 20. Czy mają Państwo jakieś wymagania niefunkcjonalne co do API? Czy mamy zapewnić bezpieczeństwo (HTTPS)? Czas odpowiedzi? Maksymalna przepustowość? Ograniczenia na zużycie zasobów? Czy mamy jakąś narzuconą technologię? Pyton? Java?

Nie, nie mamy takich wymagań

> 21. Jak bardzo mamy się skupiać na wyjaśnieniu predykcji naszego modelu? Czy mamy jedynie określić przynależność danego użytkownika? Czy raczej ustalić dlaczego wybraliśmy tak, a nie inaczej?

Na początek wystarczy jedynie określenie przynależności danego użytkownika

> 22. W jaki sposób system będzie wykorzystywany? W jaki sposób będzie testowany?

Zgodnie z oczekiwaniami, jeśli chodzi o testy to może Państwo coś zaproponujecie


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

Szczególnie gdy event_type jest ustawione na ADVERTISEMENT lub BUY_PREMIUM.

+-------+----------+--------+-------------+--------------------+                
|user_id|session_id|track_id|   event_type|           timestamp|
+-------+----------+--------+-------------+--------------------+
|    101|       124|        |ADVERTISEMENT|2022-04-19T10:19:...|
|    103|       153|        |ADVERTISEMENT|2022-04-04T20:39:...|
|    104|       165|        |ADVERTISEMENT|2022-05-22T22:47:...|
|    107|       206|    null|ADVERTISEMENT|2022-04-18T08:02:...|
|    108|       218|        |ADVERTISEMENT|2022-04-03T00:06:...|
|    112|       274|        |ADVERTISEMENT|2022-07-08T07:06:...|
|    117|       330|        |ADVERTISEMENT|2022-04-23T00:30:...|
|    119|       358|        |ADVERTISEMENT|2022-04-03T02:51:...|
|    119|       358|        |ADVERTISEMENT|2022-04-03T02:56:...|
|    120|       375|        |ADVERTISEMENT|2022-04-26T07:11:...|
|    122|       403|        |ADVERTISEMENT|2022-05-11T00:01:...|
|    123|       419|        |ADVERTISEMENT|2022-12-14T22:49:...|
|    125|       442|        |ADVERTISEMENT|2022-06-13T06:22:...|
|   null|       444|        |ADVERTISEMENT|2022-07-10T19:36:...|
|    126|       454|        |ADVERTISEMENT|2022-04-15T17:51:...|
|    127|       466|        |ADVERTISEMENT|2023-01-05T17:04:...|
|    129|       476|        |ADVERTISEMENT|2022-04-04T04:24:...|
|    132|       515|        |ADVERTISEMENT|2022-06-22T06:30:...|
|    133|       525|        |ADVERTISEMENT|2022-05-31T05:59:...|
|    134|       543|        |ADVERTISEMENT|2022-06-17T18:21:...|
+-------+----------+--------+-------------+--------------------+

I tak samo buy premium:

+-------+----------+--------+-----------+--------------------+                  
|user_id|session_id|track_id| event_type|           timestamp|
+-------+----------+--------+-----------+--------------------+
|   null|       124|        |BUY_PREMIUM|2022-04-19T10:19:...|
|    102|       143|        |BUY_PREMIUM|2022-04-19T19:30:...|
|    103|       153|        |BUY_PREMIUM|2022-04-04T20:39:...|
|    104|       165|        |BUY_PREMIUM|2022-05-22T22:47:...|
|    105|       172|    null|BUY_PREMIUM|2022-05-25T20:33:...|
|    106|       185|        |BUY_PREMIUM|2022-03-29T15:42:...|
|    107|       206|        |BUY_PREMIUM|2022-04-18T08:02:...|
|    108|       218|        |BUY_PREMIUM|2022-04-03T00:07:...|
|    109|       235|        |BUY_PREMIUM|2022-04-15T09:33:...|
|    110|       250|        |BUY_PREMIUM|2022-05-15T23:19:...|
|    111|       266|        |BUY_PREMIUM|2022-04-09T16:22:...|
|    112|       274|        |BUY_PREMIUM|2022-07-08T07:07:...|
|    113|       284|    null|BUY_PREMIUM|2022-08-18T12:55:...|
|    114|       295|        |BUY_PREMIUM|2022-04-05T13:00:...|
|    115|       312|        |BUY_PREMIUM|2022-06-27T13:49:...|
|    116|       322|        |BUY_PREMIUM|2022-04-01T03:33:...|
|    117|       330|        |BUY_PREMIUM|2022-04-23T00:31:...|
|    118|       343|        |BUY_PREMIUM|2022-05-12T22:34:...|
|    119|       358|        |BUY_PREMIUM|2022-04-03T02:56:...|
|    120|       375|        |BUY_PREMIUM|2022-04-26T07:12:...|
+-------+----------+--------+-----------+--------------------+


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

Gdzie przechowujecie reklamy? Czy macie jakąś wydzieloną bazę danych?

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



