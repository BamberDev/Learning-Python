from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///magazyn.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
alembic = Alembic()
alembic.init_app(app)


class Konto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Integer, nullable=False, default=0)


class Magazyn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produkt = db.Column(db.String(80), nullable=False)
    cena = db.Column(db.Integer, nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)


class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_action = db.Column(db.String(200), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    konto = Konto.query.first() or Konto(saldo=0)
    magazyn = Magazyn.query.all()

    if request.method == "POST":
        operation = request.form.get("operation")

        if operation == "saldo":
            try:
                kwota = int(request.form["kwota"])
                konto.saldo += kwota

                db.session.add(konto)
                db.session.add(
                    Historia(
                        log_action=f"Wprowadzono: {kwota} | Aktualne saldo: {konto.saldo}"
                    )
                )
                db.session.commit()
            except ValueError:
                return render_template(
                    "index.html",
                    page_title="Zarzadzanie magazynem",
                    konto=konto,
                    magazyn=magazyn,
                    error_message="Bledna kwota.",
                )

        elif operation == "zakup":
            try:
                produkt = request.form["produkt-zakup"]
                cena = int(request.form["cena-zakup"])
                liczba_sztuk = int(request.form["liczba-zakup"])
                koszt = cena * liczba_sztuk

                if koszt > konto.saldo:
                    return render_template(
                        "index.html",
                        page_title="Zarzadzanie magazynem",
                        konto=konto,
                        magazyn=magazyn,
                        error_message=f"Za malo srodkow na koncie! Aktualne saldo: {konto.saldo}",
                    )

                produkt_w_magazynie = Magazyn.query.filter_by(produkt=produkt).first()
                if produkt_w_magazynie:
                    produkt_w_magazynie.ilosc += liczba_sztuk
                else:
                    nowy_produkt = Magazyn(
                        produkt=produkt, cena=cena, ilosc=liczba_sztuk
                    )
                    db.session.add(nowy_produkt)

                konto.saldo -= koszt

                db.session.add(konto)
                db.session.add(
                    Historia(
                        log_action=f"Zakupiono {liczba_sztuk} sztuk {produkt}. Aktualne saldo: {konto.saldo}"
                    )
                )
                db.session.commit()
                magazyn = Magazyn.query.all()
            except ValueError:
                return render_template(
                    "index.html",
                    page_title="Zarzadzanie magazynem",
                    konto=konto,
                    magazyn=magazyn,
                    error_message="Bledne dane zakupu.",
                )

        elif operation == "sprzedaz":
            try:
                produkt = request.form["produkt-sprzedaz"]
                cena = int(request.form["cena-sprzedaz"])
                liczba_sztuk = int(request.form["liczba-sprzedaz"])

                produkt_w_magazynie = Magazyn.query.filter_by(produkt=produkt).first()
                if not produkt_w_magazynie or produkt_w_magazynie.ilosc < liczba_sztuk:
                    return render_template(
                        "index.html",
                        page_title="Zarzadzanie magazynem",
                        konto=konto,
                        magazyn=magazyn,
                        error_message=f"Brak wystarczajacej ilosci {produkt} w magazynie.",
                    )

                produkt_w_magazynie.ilosc -= liczba_sztuk
                if produkt_w_magazynie.ilosc == 0:
                    db.session.delete(produkt_w_magazynie)

                konto.saldo += cena * liczba_sztuk

                db.session.add(konto)
                db.session.add(
                    Historia(
                        log_action=f"Sprzedano {liczba_sztuk} sztuk {produkt}. Aktualne saldo: {konto.saldo}"
                    )
                )
                db.session.commit()
                magazyn = Magazyn.query.all()
            except ValueError:
                return render_template(
                    "index.html",
                    page_title="Zarzadzanie magazynem",
                    konto=konto,
                    magazyn=magazyn,
                    error_message="Bledne dane sprzedazy.",
                )

    return render_template(
        "index.html",
        page_title="Zarzadzanie magazynem",
        konto=konto,
        magazyn=magazyn,
    )


@app.route("/historia", methods=["GET"])
def historia():
    start = request.args.get("start")
    end = request.args.get("end")
    historia = Historia.query.all()

    if start is not None and end is not None:
        try:
            start = int(start)
            end = int(end)

            if start < 0 or end > len(historia) or start >= end:
                error_message = (
                    f"Nieprawidlowy zakres! Mozliwy zakres: od 0 do {len(historia)}."
                )
                return render_template(
                    "historia.html",
                    page_title="Historia operacji",
                    subtitle="Blad: Nieprawidlowy zakres",
                    historia=None,
                    error_message=error_message,
                )

            zakres = historia[start:end]
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
        historia=historia,
    )


if __name__ == "__main__":
    app.run(debug=True)
