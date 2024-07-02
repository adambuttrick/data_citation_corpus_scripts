import csv
import re
import argparse
import sys
import os
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Validate subjID in CSV file based on repository and regex pattern.')
    parser.add_argument('-i', '--input_file',
                        required=True, help='Input CSV file')
    parser.add_argument('-r', '--repository', required=True,
                        help='Repository name to filter')
    parser.add_argument('-p', '--pattern', required=True,
                        help='Regex pattern for subjID validation')
    return parser.parse_args()


def is_valid_subjid(subjid, pattern):
    return re.match(pattern, subjid) is not None


def normalize_repository_name(repository):
    base_name = os.path.splitext(os.path.basename(repository))[0]
    return re.sub(r'[^a-zA-Z0-9]', '', base_name)


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")


def process_csv(input_file, repository, pattern):
    normalized_prefix = normalize_repository_name(repository)
    valid_output = f"{normalized_prefix}_valid.csv"
    invalid_output = f"{normalized_prefix}_invalid.csv"
    try:
        with open(input_file, 'r') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            unique_pairs = {}
            for row in reader:
                if row['repository'] == repository:
                    key = (row['objId'], row['subjId'])
                    current_date = parse_date(row['updated'])
                    if key not in unique_pairs or current_date > parse_date(unique_pairs[key]['updated']):
                        unique_pairs[key] = row
        with open(valid_output, 'w') as valid_file, open(invalid_output, 'w') as invalid_file:
            valid_writer = csv.DictWriter(valid_file, fieldnames=fieldnames)
            invalid_writer = csv.DictWriter(
                invalid_file, fieldnames=fieldnames)
            valid_writer.writeheader()
            invalid_writer.writeheader()
            for (objId, subjId), row in unique_pairs.items():
                if is_valid_subjid(subjId, pattern):
                    valid_writer.writerow(row)
                else:
                    invalid_writer.writerow(row)
        print(f"Processing complete. Valid rows written to {valid_output}, invalid rows written to {invalid_output}")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_arguments()
    process_csv(args.input_file, args.repository, args.pattern)


if __name__ == "__main__":
    main()
