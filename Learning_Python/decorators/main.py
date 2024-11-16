from utils import (
    lista_komend,
    wyswietl_konto,
    wyswietl_magazyn,
    aktualizuj_magazyn,
    aktualizuj_konto,
    wyswietl_historie,
    zapisz_historie,
    Manager,
)

DATA_KONTO = "data/konto.txt"
DATA_MAGAZYN = "data/magazyn.txt"
DATA_HISTORIA = "data/historia.txt"

manager = Manager()
manager.konto = wyswietl_konto(DATA_KONTO)
manager.magazyn = wyswietl_magazyn(DATA_MAGAZYN)
manager.historia = wyswietl_historie(DATA_HISTORIA)


@manager.assign("saldo")
def saldo(manager):
    kwota = int(input("Podaj kwote do dodania lub odjecia z konta: "))
    manager.konto += kwota
    aktualizuj_konto(manager.konto, DATA_KONTO)
    log_action = f"Wprowadzono: {kwota} | Aktualne saldo: {manager.konto}"
    print(log_action)
    manager.historia.append(log_action)
    zapisz_historie(manager.historia, DATA_HISTORIA)


@manager.assign("sprzedaz")
def sprzedaz(manager):
    produkt = input("Podaj nazwe produktu: ")

    if produkt not in manager.magazyn:
        print(f"Produkt {produkt} nie znajduje się w magazynie.")
        return

    cena = int(input("Podaj cene sprzedazy: "))
    liczba_sztuk = int(input("Podaj liczbe sztuk: "))

    if manager.magazyn[produkt]["ilosc"] < liczba_sztuk:
        print(f"Brak wystarczajacej ilosci {produkt}.")
        return

    manager.magazyn[produkt]["ilosc"] -= liczba_sztuk
    if manager.magazyn[produkt]["ilosc"] == 0:
        del manager.magazyn[produkt]

    manager.konto += cena * liczba_sztuk
    aktualizuj_konto(manager.konto, DATA_KONTO)
    aktualizuj_magazyn(manager.magazyn, DATA_MAGAZYN)
    log_action = f"Sprzedano {liczba_sztuk} sztuk {produkt}. Saldo: {manager.konto}"
    print(log_action)
    manager.historia.append(log_action)
    zapisz_historie(manager.historia, DATA_HISTORIA)


@manager.assign("zakup")
def zakup(manager):
    produkt = input("Podaj nazwe produktu: ")
    cena = int(input("Podaj cenę zakupu: "))
    liczba_sztuk = int(input("Podaj liczbę sztuk: "))
    koszt = cena * liczba_sztuk

    if koszt > manager.konto:
        print(f"Za malo srodkow na koncie! Aktualne saldo: {manager.konto}")
        return

    if produkt in manager.magazyn:
        manager.magazyn[produkt]["ilosc"] += liczba_sztuk
    else:
        manager.magazyn[produkt] = {"cena": cena, "ilosc": liczba_sztuk}

    manager.konto -= koszt
    aktualizuj_konto(manager.konto, DATA_KONTO)
    aktualizuj_magazyn(manager.magazyn, DATA_MAGAZYN)
    log_action = f"Zakupiono {liczba_sztuk} sztuk {produkt}. Saldo: {manager.konto}"
    print(log_action)
    manager.historia.append(log_action)
    zapisz_historie(manager.historia, DATA_HISTORIA)


@manager.assign("konto")
def konto(manager):
    print(f"Stan konta: {manager.konto}")


@manager.assign("lista")
def lista(manager):
    if not manager.magazyn:
        print("Magazyn jest pusty.")
        return
    print("Stan magazynu:")
    for produkt, dane in manager.magazyn.items():
        print(f"{produkt}: {dane['ilosc']} sztuk, cena: {dane['cena']}")


@manager.assign("magazyn")
def magazyn_produkty(manager):
    produkt = input("Podaj nazwe produktu: ")
    if produkt in manager.magazyn:
        dane = manager.magazyn[produkt]
        print(f"{produkt}: {dane['ilosc']} sztuk, cena: {dane['cena']}")
    else:
        print(f"Produkt {produkt} nie znajduje sie w magazynie.")


@manager.assign("przeglad")
def przeglad(manager):
    od = input("Podaj indeks poczatkowy (lub zostaw puste dla poczatku): ")
    do = input("Podaj indeks koncowy (lub zostaw puste dla konca): ")

    od = int(od) if od else 0
    do = int(do) if do else len(manager.historia)

    if od < 0 or do > len(manager.historia) or od > do:
        print(f"Nieprawidlowy zakres! Liczba operacji: {len(manager.historia)}")
        return

    print("Historia operacji:")
    for i, line in enumerate(manager.historia[od:do], start=od):
        print(f"{i}: {line}")


def __main__():
    print("\nRejestr magazynu")
    lista_komend()

    while True:
        komenda = input("Wprowadz komende: ").strip().lower()
        if komenda == "koniec":
            print("Zakonczono dzialanie programu.")
            break
        try:
            manager.execute(komenda)
            lista_komend()
        except AttributeError as e:
            print(e)
            lista_komend()


if __name__ == "__main__":
    __main__()
