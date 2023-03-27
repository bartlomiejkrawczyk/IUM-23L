
## Pierwszy kontakt z klientem

Jakiś czas temu wprowadziliśmy konta premium, które uwalniają użytkowników od słuchania reklam.
Nie są one jednak jeszcze zbyt popularne - czy możemy się dowiedzieć, które osoby są bardziej skłonne do zakupu takiego konta?

## Nasze pytania w stronę klienta

1. Czy system oferuje jedynie jedną ofertę konta premium?
Czy istnieją jakieś różne dostępne oferty? Czy konta premium można dzielić?

1. Co chcieli by państwo uzyskać wykorzystując nasz system? Jakie mają Państwo oczekiwania co do systemu?

Czy mamy przewidywać czy dany użytkownik kupi konto premium? Czy może określić, cechy które sygnalizują, że użytkownik chce kupić takie konto?

1. Jakie są ograniczenia czasowe? Na kiedy chcą uzyskać Państwo gotowy projekt?

1. Chcielibyśmy dostać wszystkie dostępne dane. My wybierzemy z nich co nas interesuje.

1. Czy docelowy system ma wskazywać na to z czego wynika zakup konta premium na podstawie danych? Czy raczej API powinno przewidywać czy dany użytkownik jest skłonny do zakupu takiego konta?

1. Czy mają już Państwo istniejący system, który stara się przewidzieć kto jest skłonny do zakupu konta premium? Czy możemy uzyskać dostęp do takiego rozwiązania?

Czy mają Państwo pewne wymagania biznesowe co do predykcji naszego modelu?

Jeśli nie mają państwo żadnego istniejącego modelu do porówniania, to my postaramy się porównać model do pewnego przygotowanego przez nas naiwnego modelu predykcyjnego.


1. Czy możemy założyć, że Pan będzie naszym ekspertem domenowym? Czy raczej mamy, założyć, że to my jesteśmy ekspertami?

1. Jak duży jest państwa system? Ilu użytkowników korzysta z niego?

1. Czy dane udostępnione nam to kompletne dane?

2. Jakiej postaci dane mają Państwo dostępne? Czy trzymacie je w bazie NoSQL - w formacie JSON, czy raczej typowo w tabelach SQL? W jakich tabelach / formacie trzymacie wszystkie dane użytkowników? Czy możemy mieć dostęp do wszystkich tabel? Czy dostęp możemy otrzymać jedynie do wybranej części? Dlaczego do reszty danych nie mamy dostępu (pewnie hasła itp. xD)?

- lista dostępnych artystów i utworów muzycznych, (czy są określone gatunki)
- baza użytkowników, (czy wszystkie dane są pełne, płeć, wiek, zawód, , ...)
- historia sesji użytkowników, (przeglądarka, czas, piosenka, ...) (zakup, data zakupu, opłata, ...) (reklama, kiedy, czas trwania, ...)
- techniczne informacje dot. poziomu cache dla poszczególnych utworów.


- jesteśmy przekonani, że wszystkie dane się przydadzą i to my ustalimy czego potrzebujemy, a czego nie

2. Czy dostępna jest jakaś historia puszczanych reklam? - może to natrętne reklamy skłoniły do zakupu xD

2. Jak często puszczane są reklamy użytkownikom kont nie premium? Czy macie dostępną listę dostępnych reklam?


2. Czy możemy dostać schemat utrzymywanych danych? Jakaś klasa? Schemat z bazy? UML? - żebyśmy mogli ustalić jakie dane nam przesłał, a jakich nie dodał xD

3. Czy udostępnią nam Państwo dane już zagregowane do postaci jednej tabeli? Czy udostępnią je Państwo w formacie np. JSON? Albo czy udostępnią je jako kilka plików CSV, które my już zagregujemy?

4. W jaki sposób Państwo chcą wykorzystać przygotowane przez nas API? Czy my mamy ustalić format danych przyjmowanych / odsyłanych przez nasze api?

5. Czy powinniśmy coś wiedzieć na temat procesu zbierania przez Państwa danych? Jak Państwa system działa w przypadku błędu w czasie transakcji? Czy całe zapytanie do systemu jest wykonywane w ramach jednej transakcji? Czy może się zdarzyć, że jedynie częściowo zostanie zapisane? Czy programy działające na różnych systemach / przeglądarkach działają identycznie i w identyczny sposób zbierają dane? Czy jednak są pewne różnice w sposobie zbierania?

6. Czy mają Państwo jakieś wymagania niefunkcjonalne co do API? Czy mamy zapewnić bezpieczeństwo (HTTPS)? Czas odpowiedzi? Maksymalna przepustowość? Ograniczenia na zużycie zasobów? Czy mamy jakąś narzuconą technologię? Pyton? Java?

7. Jak bardzo mamy się skupiać na wyjaśnieniu predykcji naszego modelu? Czy mamy jedynie określić przynależność danego użytkownika? Czy raczej ustalić dlaczego wybraliśmy tak, a nie inaczej?

8. W jaki sposób system będzie wykorzystywany? W jaki sposób będzie testowany?

Rozumiemy, że w naszym rozwiązaniu mamy się skupić na **transparentność/zdolność wyjaśniania predykcji/ruch XAI (eXplainable AI),**

Z czego wynikają nie pełne dane? Czy to błąd wynikający z braku w bazie? Czy może błąd w czasie wyciągania danych z bazy?























