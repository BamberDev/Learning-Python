print("Rejestr magazynu")

konto = 0
magazyn = {}
historia = []

print("""
Dostępne komendy:
- saldo
- sprzedaz
- zakup
- konto
- lista
- magazyn
- przeglad
- koniec
""")

while True:
    komenda = input("Wprowadz komende: ")

    if komenda == "saldo":
        kwota = int(input("Podaj kwote do dodania lub odjecia z konta: "))
        konto += kwota
        historia.append(f"saldo {kwota}")
        print(f"Aktualne saldo: {konto}")

    elif komenda == "sprzedaz":
        produkt = input("Podaj nazwe produktu: ")
        if produkt not in magazyn:
            print(f"Produkt {produkt} nie znajduje sie w magazynie.")
            continue
        cena = int(input("Podaj cene sprzedazy: "))
        liczba_sztuk = int(input("Podaj liczbe sztuk: "))
        if magazyn[produkt]["ilosc"] < liczba_sztuk:
            print(f"Nie masz wystarczajacej ilosci {produkt} w magazynie.")
            continue
        magazyn[produkt]["ilosc"] -= liczba_sztuk
        konto += cena * liczba_sztuk
        historia.append(f"sprzedaz {produkt} {cena} {liczba_sztuk}")
        print(f"Sprzedano {liczba_sztuk} sztuk {produkt}. Aktualne saldo: {konto}")

    elif komenda == "zakup":
        produkt = input("Podaj nazwe produktu: ")
        cena = int(input("Podaj cene zakupu: "))
        liczba_sztuk = int(input("Podaj liczbe sztuk: "))
        koszt = cena * liczba_sztuk

        if koszt > konto:
            print(f"Za malo srodkow na koncie! Aktualne saldo: {konto}")
            continue
        if cena < 0 or liczba_sztuk < 0:
            print("Cena i liczba sztuk musza byc dodatnie!")
            continue

        if produkt in magazyn:
            magazyn[produkt]["ilosc"] += liczba_sztuk
        else:
            magazyn[produkt] = {"cena": cena, "ilosc": liczba_sztuk}

        konto -= koszt
        historia.append(f"zakup {produkt} {cena} {liczba_sztuk}")
        print(f"Zakupiono {liczba_sztuk} sztuk {produkt}. Aktualne saldo: {konto}")

    elif komenda == "konto":
        print(f"Stan konta: {konto}")

    elif komenda == "lista":
        if len(magazyn) == 0:
            print("Magazyn jest pusty.")
        else:
            print("Stan magazynu:")
            for produkt, dane in magazyn.items():
                print(f"{produkt}: {dane["ilosc"]} sztuk, cena: {dane["cena"]}")

    elif komenda == "magazyn":
        produkt = input("Podaj nazwe produktu: ")
        if produkt in magazyn:
            print(f"{produkt}: {magazyn[produkt]["ilosc"]} sztuk, cena: {magazyn[produkt]["cena"]}")
        else:
            print(f"Produkt {produkt} nie znajduje sie w magazynie.")

    elif komenda == "przeglad":
        od = input("Podaj indeks poczatkowy (lub zostaw puste dla poczatku): ")
        do = input("Podaj indeks koncowy (lub zostaw puste dla konca): ")

        if od == "":
            od = 0
        else:
            od = int(od)

        if do == "":
            do = len(historia)
        else:
            do = int(do)

        if od < 0 or do > len(historia) or od > do:
            print(f"Nieprawidlowy zakres! Liczba operacji: {len(historia)}")
        else:
            print("Historia operacji:")
            for i in range(od, do):
                print(f"{i}: {historia[i]}")

    elif komenda == "koniec":
        print("Koniec programu.")
        break

    else:
        print("Nieznana komenda.")
    
    print("""
    Dostępne komendy:
    - saldo
    - sprzedaz
    - zakup
    - konto
    - lista
    - magazyn
    - przeglad
    - koniec
    """)
