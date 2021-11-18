# DONE: 
    Jeden obiekt: Root (a w nim Index i items)
    Jeden plik bazy: <nazwa bazy>.db
    Struktura obiektów to drzewo obiektów z normalnymi atrybutami i odnośnikami do obiektówy klasy Persistent
    Pobieranie obiektów to rekurencyjna akcja
    Nowa klasa Item: (id), obiekt, ilość użyć
    Itemy znajdują się w jednym dużym dictionary w Index gdzie klucz to ID obiektu a item to obiekt klasy Item
    Root tak jak było
    porównanie last_changed przy aktualizacji
    odpowiednie in/dekrementowanie uses
# TODO: 
    stworzenie języka zapytań -> atrybuty, wartości (done) liczba elementów (TODO)
    obsługiwanie warstwy sieciowej (gniazdka itd)