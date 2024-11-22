import ast


class Manager:
    def __init__(self):
        self.methods = {}
        self.konto = 0
        self.magazyn = {}
        self.historia = []

    def assign(self, action_name):
        def decorator(func):
            self.methods[action_name] = func
            return func

        return decorator

    def execute(self, action_name):
        if action_name in self.methods:
            return self.methods[action_name](self)
        else:
            raise AttributeError(f"Komenda {action_name} nie istnieje")


def wyswietl_konto(data):
    with open(data, "r") as file:
        return int(file.read())


def aktualizuj_konto(konto, data):
    with open(data, "w") as file:
        file.write(str(konto))


def wyswietl_magazyn(data):
    magazyn = {}
    with open(data, "r") as file:
        for line in file:
            produkt, details = line.strip().split(",", 1)
            details_dict = ast.literal_eval(details)
            magazyn[produkt] = {
                "cena": details_dict["cena"],
                "ilosc": details_dict["ilosc"],
            }
    return magazyn


def aktualizuj_magazyn(magazyn, data):
    with open(data, "w") as file:
        for produkt, dane in magazyn.items():
            file.write(
                f"{produkt},{{'cena': {dane['cena']}, 'ilosc': {dane['ilosc']}}}\n"
            )


def wyswietl_historie(data):
    with open(data, "r") as file:
        return [line.strip() for line in file]


def zapisz_historie(historia, data):
    with open(data, "a") as file:
        file.write(f"{historia[-1]}\n")
    print("\nHistoria zostala zapisana")
