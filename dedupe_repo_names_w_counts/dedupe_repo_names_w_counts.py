import csv
import argparse
from collections import Counter


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Deduplicate repository list from CSV file and count instances')
    parser.add_argument('-i', '--input_file',
                        help='Path to the input CSV file')
    parser.add_argument('-o', '--output_file',
                        default='dedupe_repo_names_w_counts.csv', help='Path to the output CSV file')
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def extract_and_count_repositories(data):
    repositories = [row['repository'].strip()
                    for row in data if 'repository' in row]
    repo_counter = Counter(repositories)
    return [{'repository': repo, 'count': count} for repo, count in repo_counter.items()]


def write_csv(file_path, data):
    if data:
        fieldnames = ['repository', 'count']
        with open(file_path, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
    try:
        data = read_csv(input_file)
        repo_data = extract_and_count_repositories(data)
        write_csv(output_file, repo_data)
        print(f"Deduplicated repository list with counts written to: {output_file}")
    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
    except IOError:
        print(f"An error occurred while reading or writing the file.")
    except KeyError:
        print(f"The 'repository' column was not found in the CSV file.")


if __name__ == '__main__':
    main()
