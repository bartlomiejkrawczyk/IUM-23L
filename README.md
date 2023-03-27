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

## Zadanie

Jakiś czas temu wprowadziliśmy konta premium, które uwalniają użytkowników od słuchania reklam.
Nie są one jednak jeszcze zbyt popularne - czy możemy się dowiedzieć, które osoby są bardziej skłonne do zakupu takiego konta?

# Definicja Problemu Biznesowego

### Zrozumienie zagadnienia
<!-- Musimy zrozumieć, co tak naprawdę jest do zrobienia i ustalić, jak to osiągnąć. -->

1. Określenie celu biznesowego
    - Opis kontekstu.
    - Zdefiniowanie celów biznesowych.
    - Biznesowe kryterium sukcesu.
2. Ocena aktualnej sytuacji.
    - Spis dostępnych zasobów.
    - Lista wymagań, założeń i ograniczeń.
    - Zidentyfikowanie zagrożeń dla projektu.
    - Słowniczek terminologii (biznesowej i analitycznej).
    - Analiza kosztów i zysków z projektu.
3. Określenie celów modelowania.
    - Opis zadań modelowania.
    - Definicja kryteriów sukcesu z perspektywy analitycznej.
4. Przygotowanie planu projektu.
    - Plan etapów projektu.
    - Wstępne propozycje narzędzi i metod.


# Analiza Danych z Perspektywy Realizacji Zadań

### Zrozumienie danych
<!-- Wstępne zebranie i przeanalizowanie danych. -->

1. Zebranie wstępnego zbioru danych do modelowania 
    - raport podsumowujący zebrane dane.
2. Techniczny opis danych 
    - raport opisujący format danych, ich ilość, atrybuty, itp.
3. Eksploracja danych 
    - raport z eksploracji, wstępne hipotezy.
4. Weryfikacja jakości danych 
    - raport podsumowujący znalezione problemy i sugestie ich rozwiązań.


### Przygotowanie danych

<!-- Przygotowanie finalnego zbioru danych do modelowania, w tym oczyszczanie danych, selekcja atrybutów, feature engineering itd. -->

1. Selekcja danych (zarówno atrybuty jak i rekordy)
    - uzasadnienie dlaczego taki, a nie inny wybór.
2. Czyszczenie danych
    - raport z podjętych kroków.
3. Generowanie atrybutów/rekordów.
    - Opis utworzonych atrybutów.
    - Opis wygenerowanych rekordów (np. sztucznych rekordów dla klientów, którzy w danym roku nie dokonali zakupu).
4. Integracja danych
    - zintegrowane dane z wielu źródeł.
5. Zmiana formatu danych
    - przeformatowane dane.

### Modelowanie

<!-- Wybór algorytmów, architektury modeli, strojenie hiperparametrów, trening. -->

1. Wybór metody modelowania.
    - Opis wybranej metody.
    - Przyjęte założenia modelowania.
2. Opracowanie przebiegu eksperymentu
    - opis tego, jak będzie wykonywane trenowanie i ocena modelu.
3. Konstrukcja modelu.
    - Opis hiperparametrów.
    - Wytrenowane modele.
    - Opis modeli, ich interpretacja.
4. Ewaluacja modelu.
    - Podsumowanie uzyskanych wyników, miar błędu, itp.
    - Krytyczne wnioski odnośnie ustawień hiperparametrów (przydatne do następnej iteracji).

### Ewaluacja

<!-- Ocena przygotowanych modeli i procedury ich generowania z perspektywy zagadnienia biznesowego. -->

1. Ocena rezultatów z perspektywy biznesowej.
    - Ocena wyników pod kątem kryteriów sukcesu.
    - Lista zaakceptowanych modeli.
2. Retrospektywna analiza całego procesu
    - podsumowanie podkreślające brakujące elementy, niedopatrzenia.
3. Ustalenie sposobu dalszego postępowania (czy kontynuujemy prace).
    - Lista możliwych dalszych kroków.
    - Uzasadnione decyzje odnośnie dalszego postępowania.

### Wdrożenie

<!-- Wdrożenie przygotowanego modelu do użycia. -->

1. Zaplanowanie wdrożenia
    - plan.
2. Zaplanowanie kwestii związanych z monitorowaniem i utrzymaniem
    - plan.
3. Przygotowanie finalnego raportu
    - raport + prezentacja.
4. Rewizja projektu
    - podsumowanie doświadczeń/wiedzy zdobytej podczas realizacji projektu.















