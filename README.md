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

Możliwe jest bezpośrednie wywołanie skryptu `microservice.py`:
```shell
python ./microservice.py
```

Za pomocą flask:
```shell
flask --app microservice run
```

Wywołanie skryptu `microservice.py`:
```shell
./microservice.py
```

## Endpoint-y

## Eksperymenty A/B