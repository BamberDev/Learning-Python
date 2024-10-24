import sys
import csv
import json
import pickle


class FileHandler:
    """
    Base class for file handlers
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        raise NotImplementedError("Subclass must implement this method (load)")

    def save(self):
        raise NotImplementedError("Subclass must implement this method (save)")

    def modify(self, data, changes):
        """
        Modify the data by applying changes in the format (x, y, value).
        """
        for change in changes:
            x, y, value = change
            data[int(y)][int(x)] = value
        return data


class CSVHandler(FileHandler):
    """
    File handler for CSV files
    """

    def load(self):
        with open(self.file_path) as file:
            reader = csv.reader(file)
            return [row for row in reader]

    def save(self, data):
        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)


class JSONHandler(FileHandler):
    """
    File handler for JSON files
    """

    def load(self):
        with open(self.file_path) as file:
            return json.load(file)

    def save(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=2)


class TxtHandler(FileHandler):
    """
    File handler for TXT files
    """

    def load(self):
        with open(self.file_path) as file:
            return file.read()

    def save(self, data):
        if isinstance(data, list):
            data = "\n".join([",".join(row) for row in data])
        with open(self.file_path, "w") as file:
            file.write(data)


class PickleHandler(FileHandler):
    """
    File handler for pickle files
    """

    def load(self):
        with open(self.file_path, "rb") as file:
            return pickle.load(file)

    def save(self, data):
        with open(self.file_path, "wb") as file:
            pickle.dump(data, file)


def parse_changes(changes):
    parsed_changes = []
    for change in changes:
        x, y, value = change.split(",")
        parsed_changes.append((int(x), int(y), value))
    return parsed_changes


def get_handler(file_path):
    if file_path.endswith(".csv"):
        return CSVHandler(file_path)
    elif file_path.endswith(".json"):
        return JSONHandler(file_path)
    elif file_path.endswith(".txt"):
        return TxtHandler(file_path)
    elif file_path.endswith(".pickle"):
        return PickleHandler(file_path)
    else:
        raise ValueError(
            "Unsupported file format. Supported file formats: .csv, .json, .txt, .pickle"
        )


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
        print("Something went wrong!")
        print(
            "Example usage: python reader.py data/in.csv data/out.json <change_1> <change_2> ... <change_n>"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    changes = sys.argv[3:]

    try:
        input_handler = get_handler(input_file)
        output_handler = get_handler(output_file)
        data = input_handler.load()

        print("\nOriginal Data (Before Modification):")
        pretty_print(data)

        parsed_changes = parse_changes(changes)
        modified_data = input_handler.modify(data, parsed_changes)

        print("\nModified Data (After Modification):")
        pretty_print(modified_data)

        output_handler.save(modified_data)
        print(f"\nData saved to {output_file}.")

    except ValueError as err:
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
