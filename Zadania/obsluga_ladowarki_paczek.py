# Program do obslugi ladowarki paczek.

print("Ile paczek chcesz wyslac?")
ilosc_paczek = int(input("Podaj ilosc paczek: "))

obecna_waga = 0
waga_koncowa = 0
ilosc_wyslanych_paczek = 0
ilosc_pustych_kg = 0
max_puste_kg = 0
max_puste_kg_index = 0

for i in range(ilosc_paczek):
    waga = float(input(f"Podaj wage paczki {i+1}: "))
        
    if waga < 1 or waga > 10:
        print("\nWaga poza dozwolonym zakresem (1-10 kg), konczenie pakowania.")
        break
        
    if obecna_waga + waga > 20:
        puste_kg = 20 - obecna_waga
        ilosc_pustych_kg += puste_kg
        ilosc_wyslanych_paczek += 1
            
        if puste_kg > max_puste_kg:
            max_puste_kg = puste_kg
            max_puste_kg_index = ilosc_wyslanych_paczek
            
        obecna_waga = 0
        
    obecna_waga += waga
    waga_koncowa += waga

if obecna_waga > 0:
    puste_kg = 20 - obecna_waga
    ilosc_pustych_kg += puste_kg
    ilosc_wyslanych_paczek += 1
        
    if puste_kg > max_puste_kg:
        max_puste_kg = puste_kg
        max_puste_kg_index = ilosc_wyslanych_paczek

print("\nPodsumowanie:")

if ilosc_wyslanych_paczek == 0:
    print(f"Wyslano {ilosc_wyslanych_paczek} paczek.")
elif ilosc_wyslanych_paczek == 1:
    print(f"Wyslano {ilosc_wyslanych_paczek} paczke.")
else:
    print(f"Wyslano {ilosc_wyslanych_paczek} paczki.")

print(f"Wyslano {waga_koncowa} kg.")
print(f"Suma pustych kilogramow: {ilosc_pustych_kg} kg.")
print(f"Najwiecej pustych kilogramow ma paczka {max_puste_kg_index} ({max_puste_kg} kg).")