from utils import (
    wyswietl_konto,
    wyswietl_magazyn,
    aktualizuj_magazyn,
    aktualizuj_konto,
    wyswietl_historie,
    zapisz_historie,
    Manager,
)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_KONTO = "data/konto.txt"
DATA_MAGAZYN = "data/magazyn.txt"
DATA_HISTORIA = "data/historia.txt"

manager = Manager()
manager.konto = wyswietl_konto(DATA_KONTO)
manager.magazyn = wyswietl_magazyn(DATA_MAGAZYN)
manager.historia = wyswietl_historie(DATA_HISTORIA)


@app.route("/", methods=["GET", "POST"])
def index():
    global manager

    if request.method == "POST":
        operation = request.form.get("operation")

        if operation == "saldo":
            try:
                kwota = int(request.form["kwota"])
                manager.konto += kwota
                aktualizuj_konto(manager.konto, DATA_KONTO)
                log_action = f"Wprowadzono: {kwota} | Aktualne saldo: {manager.konto}"
                manager.historia.append(log_action)
                zapisz_historie(manager.historia, DATA_HISTORIA)

            except (ValueError, KeyError):
                return render_template(
                    "index.html",
                    page_title="Zarzadzanie magazynem",
                    konto=manager.konto,
                    magazyn=manager.magazyn,
                    saldo_error_message="Bledna kwota.",
                )

        elif operation == "zakup":
            try:
                produkt = request.form["produkt-zakup"]
                cena = int(request.form["cena-zakup"])
                liczba_sztuk = int(request.form["liczba-zakup"])
                koszt = cena * liczba_sztuk

                if koszt > manager.konto:
                    return render_template(
                        "index.html",
                        page_title="Zarzadzanie magazynem",
                        konto=manager.konto,
                        magazyn=manager.magazyn,
                        error_message=f"Za malo srodkow na koncie! Aktualne saldo: {manager.konto}",
                    )

                if produkt in manager.magazyn:
                    manager.magazyn[produkt]["ilosc"] += liczba_sztuk
                else:
                    manager.magazyn[produkt] = {"cena": cena, "ilosc": liczba_sztuk}

                manager.konto -= koszt
                aktualizuj_konto(manager.konto, DATA_KONTO)
                aktualizuj_magazyn(manager.magazyn, DATA_MAGAZYN)
                log_action = (
                    f"Zakupiono {liczba_sztuk} sztuk {produkt}. Saldo: {manager.konto}"
                )
                print(log_action)
                manager.historia.append(log_action)
                zapisz_historie(manager.historia, DATA_HISTORIA)
            except (ValueError, KeyError):
                return render_template(
                    "index.html",
                    page_title="Zarzadzanie magazynem",
                    konto=manager.konto,
                    magazyn=manager.magazyn,
                    error_message="Bledne dane zakupu.",
                )

        elif operation == "sprzedaz":
            try:
                produkt = request.form["produkt-sprzedaz"]
                cena = int(request.form["cena-sprzedaz"])
                liczba_sztuk = int(request.form["liczba-sprzedaz"])

                if (
                    produkt not in manager.magazyn
                    or manager.magazyn[produkt]["ilosc"] < liczba_sztuk
                ):
                    return render_template(
                        "index.html",
                        page_title="Zarzadzanie magazynem",
                        konto=manager.konto,
                        magazyn=manager.magazyn,
                        error_message=f"Brak wystarczajacej ilosci {produkt} w magazynie.",
                    )

                manager.magazyn[produkt]["ilosc"] -= liczba_sztuk
                if manager.magazyn[produkt]["ilosc"] == 0:
                    del manager.magazyn[produkt]

                manager.konto += cena * liczba_sztuk
                aktualizuj_konto(manager.konto, DATA_KONTO)
                aktualizuj_magazyn(manager.magazyn, DATA_MAGAZYN)
                log_action = (
                    f"Sprzedano {liczba_sztuk} sztuk {produkt}. Saldo: {manager.konto}"
                )
                print(log_action)
                manager.historia.append(log_action)
                zapisz_historie(manager.historia, DATA_HISTORIA)
            except (ValueError, KeyError):
                return render_template(
                    "index.html",
                    page_title="Zarzadzanie magazynem",
                    konto=manager.konto,
                    magazyn=manager.magazyn,
                    error_message="Bledne dane sprzedazy.",
                )

        else:
            return render_template(
                "index.html",
                page_title="Zarzadzanie magazynem",
                konto=manager.konto,
                magazyn=manager.magazyn,
                error_message="Nieznana operacja!",
            )

    return render_template(
        "index.html",
        page_title="Zarzadzanie magazynem",
        konto=manager.konto,
        magazyn=manager.magazyn,
    )


@app.route("/historia", methods=["GET"])
def historia():
    start = request.args.get("start")
    end = request.args.get("end")

    if start is not None and end is not None:
        try:
            start = int(start)
            end = int(end)

            if start < 0 or end > len(manager.historia) or start >= end:
                error_message = f"Nieprawidlowy zakres! Mozliwy zakres: od 0 do {len(manager.historia)}."
                return render_template(
                    "historia.html",
                    page_title="Historia operacji",
                    subtitle="Blad: Nieprawidlowy zakres",
                    historia=None,
                    error_message=error_message,
                )

            zakres = manager.historia[start:end]
            return render_template(
                "historia.html",
                page_title="Historia operacji",
                subtitle=f"Historia operacji od {start} do {end}",
                historia=zakres,
            )
        except ValueError:
            error_message = "Zakres musi byc liczba calkowita!"
            return render_template(
                "historia.html",
                page_title="Historia operacji",
                subtitle="Blad: Nieprawidlowe dane",
                historia=None,
                error_message=error_message,
            )

    return render_template(
        "historia.html",
        page_title="Historia operacji",
        subtitle="Pelna historia operacji",
        historia=manager.historia,
    )


app.run(debug=True)
