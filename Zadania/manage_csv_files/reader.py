import sys
import csv

def load_data(file_path):
    """
    Reads data from csv file
    """
    with open(file_path, "r", newline="") as file:
        reader = csv.reader(file)
        return [row for row in reader]
    
def modify_data(data, changes):
    """
    Modifies data
    """
    for change in changes:
        parts = change.split(',')
        if len(parts) != 3:
            print(f"Nieprawidlowy format zmiany: {change}")
            continue
        
        col, row, value = parts
        
        if not col.isdigit() or not row.isdigit():
            print(f"Kolumna lub wiersz nie sa liczbami w zmianie: {change}")
            continue

        col = int(col)
        row = int(row)
        
        if row >= len(data) or col >= len(data[row]):
            print(f"Zmiana {change} poza zakresem danych")
            continue
        
        data[row][col] = value
    
    
def save_data(file_path, data):
    """
    Writes data to csv file
    """
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def pretty_print(data):
    """
    Prints data in pretty format
    """
    max_lengths = [] 

    for col in range(len(data[0])):
        max_col_length = 0

        for row in data:
            max_col_length = max(max_col_length, len(row[col]))
        max_lengths.append(max_col_length)

    for row in data:
        text = ""

        for i, cell in enumerate(row):
            text += cell.ljust(max_lengths[i]) + "\t"
        print(text)


def main():
    if len(sys.argv) < 4:
        print("Przykladowe wywolanie: python reader.py data/in.csv data/out.csv <zmiana_1> <zmiana_2> ... <zmiana_n>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    changes = sys.argv[3:]

    data = load_data(input_file)

    print("\nTabela przed zmianami:")
    pretty_print(data)
    
    print("\n")

    modify_data(data, changes)

    print("Tabela po zmianach:")
    pretty_print(data)

    save_data(output_file, data)

if __name__ == "__main__":
    main()