import json
import csv
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter CSV based on JSON keys")
    parser.add_argument('-j', '--json', required=True,
                        help="Path to JSON file")
    parser.add_argument('-i', '--input_csv', required=True, help="Path to CSV file")
    return parser.parse_args()


def read_json(json_file):
    with open(json_file, 'r') as f:
        return set(json.load(f).keys())


def process_csv(csv_file, valid_keys):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        valid_rows = []
        invalid_rows = []

        for row in reader:
            if row['subjId'] in valid_keys:
                valid_rows.append(row)
            else:
                invalid_rows.append(row)

    return fieldnames, valid_rows, invalid_rows


def write_csv(filename, fieldnames, rows):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_output_filenames(csv_file):
    directory, filename = os.path.split(csv_file)
    base_name = os.path.splitext(filename)[0]
    valid_file = os.path.join(directory, f"{base_name}_valid.csv")
    invalid_file = os.path.join(directory, f"{base_name}_invalid.csv")
    return valid_file, invalid_file


def filter_csv(json_file, csv_file):
    valid_keys = read_json(json_file)
    fieldnames, valid_rows, invalid_rows = process_csv(csv_file, valid_keys)

    valid_file, invalid_file = get_output_filenames(csv_file)

    write_csv(valid_file, fieldnames, valid_rows)
    write_csv(invalid_file, fieldnames, invalid_rows)

    print(f"Processed {len(valid_rows) + len(invalid_rows)} rows.")
    print(f"Valid rows: {len(valid_rows)}")
    print(f"Invalid rows: {len(invalid_rows)}")
    print(f"Results written to {valid_file} and {invalid_file}")


def main():
    args = parse_arguments()
    filter_csv(args.json, args.input_csv)


if __name__ == "__main__":
    main()
