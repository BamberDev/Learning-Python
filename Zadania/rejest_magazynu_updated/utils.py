# funkcje pomocnicze
import ast
import datetime as dt

data_konto = "data/konto.txt"
data_magazyn = "data/magazyn.txt"
data_historia = "data/historia.txt"

def lista_komend():
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

def wyswietl_konto(data = data_konto):
    konto = 0
    with open(data, "r") as file:
        konto = int(file.read())
    return konto

def aktualizuj_konto(konto):
    with open(data_konto, "w") as file:
        file.write(str(konto))
    
def wyswietl_magazyn(data = data_magazyn):
    magazyn = {}
    with open(data, "r") as file:
        for line in file:
            produkt, details = line.strip().split(",", 1)
            details_dict = ast.literal_eval(details)
            magazyn[produkt] = {"cena": details_dict['cena'], "ilosc": details_dict['ilosc']}
    return magazyn

def aktualizuj_magazyn(magazyn):
    with open(data_magazyn, "w") as file:
        for produkt, dane in magazyn.items():
            file.write(f"{produkt},{{'cena': {dane['cena']}, 'ilosc': {dane['ilosc']}}}\n")

def wyswietl_historie(historia):
    with open(data_historia, "r") as file:
        for line in file:
            print(line.strip())
    return historia

def zapisz_historie(historia):
    if historia:
        historia.append(f"Dodano: {str(dt.datetime.now())}")
        with open(data_historia, "a") as file:
            for line in historia:
                file.write(f"{line}\n")
        print("Historia zostala zapisana")
