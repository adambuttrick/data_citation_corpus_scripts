import csv
import argparse
from collections import Counter


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Count repositories from CSV file and calculate percentages')
    parser.add_argument('-i', '--input_file',
                        help='Path to the input CSV file')
    parser.add_argument('-o', '--output_file',
                        help='Path to the output CSV file')
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def process_repositories(data):
    repo_counter = Counter()
    for row in data:
        repo = row['repository'].strip()
        if repo:
            repo_counter[repo] += 1
    total_count = sum(repo_counter.values())
    repo_data = [
        {
            'repository': repo,
            'count': count,
            'percent_total': count / total_count if total_count > 0 else 0
        }
        for repo, count in repo_counter.items()
    ]
    repo_data.sort(key=lambda x: x['count'], reverse=True)

    return repo_data


def write_csv(file_path, data):
    if data:
        fieldnames = ['repository', 'count', 'percent_total']
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
        repo_data = process_repositories(data)
        write_csv(output_file, repo_data)
        print(f"Repository list with counts and correct percentages written to: {output_file}")
    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
    except IOError:
        print(f"An error occurred while reading or writing the file.")
    except KeyError:
        print(f"The 'repository' column was not found in the CSV file.")


if __name__ == '__main__':
    main()
