print("Wygeneruj spersonalizowana kartke urodzinowa\n")

imie_odbiorcy = str(input("Podaj imie odbiorcy: "))

obecny_rok = int(2024)

rok_urodzenia = int(input("Podaj rok urodzenia odbiorcy: "))

wiek = int(obecny_rok-rok_urodzenia)

spersonalizowana_wiadomosc = str(input("Twoje zyczenia: "))

imie_nadawcy = str(input("Podaj imie nadawcy: "))

print("\n")

print(f"Hej {imie_odbiorcy}! Wszystkiego najlepszego z okazji {wiek} urodzin!\n\n{spersonalizowana_wiadomosc}\n\nZyczy Ci: {imie_nadawcy}")
