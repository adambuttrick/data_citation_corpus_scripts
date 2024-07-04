import csv
import argparse
from collections import Counter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process CSV and calculate statistics")
    parser.add_argument("-i", "--input", required=True,
                        help="Input CSV file path")
    parser.add_argument("-o", "--output", default="stats.txt",
                        help="Output file path for results")
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def calculate_field_stats(data, fields):
    total = len(data)
    field_counts = {field: sum(
        1 for row in data if row[field]) for field in fields}
    field_percentages = {field: (count / total) *
                         100 for field, count in field_counts.items()}
    return field_counts, field_percentages


def calculate_doi_pmid_stats(data):
    total = len(data)
    doi_count = sum(1 for row in data if row['doi'] or row['JRNL_DOI'])
    pmid_count = sum(1 for row in data if row['JRNL_PMID'])
    both_count = sum(1 for row in data if (
        row['doi'] or row['JRNL_DOI']) and row['JRNL_PMID'])

    return {
        'doi': (doi_count, (doi_count / total) * 100),
        'pmid': (pmid_count, (pmid_count / total) * 100),
        'both': (both_count, (both_count / total) * 100)
    }


def format_results(field_stats, doi_pmid_stats):
    results = "Field completeness:\n"
    for field, (count, percentage) in field_stats.items():
        results += f"{field}: {count} ({percentage:.2f}%)\n"

    results += "\nDOI and PMID statistics:\n"
    results += f"Entries with DOIs: {doi_pmid_stats['doi'][0]} ({doi_pmid_stats['doi'][1]:.2f}%)\n"
    results += f"Entries with PMIDs: {doi_pmid_stats['pmid'][0]} ({doi_pmid_stats['pmid'][1]:.2f}%)\n"
    results += f"Entries with both DOIs and PMIDs: {doi_pmid_stats['both'][0]} ({doi_pmid_stats['both'][1]:.2f}%)\n"

    return results


def write_results(results, output_file):
    if output_file:
        with open(output_file, 'w') as f:
            f.write(results)
    else:
        print(results)


def main():
    args = parse_args()
    data = read_csv(args.input)

    fields = ['TITLE', 'KEYWDS', 'AUTHOR', 'JRNL_AUTH', 'JRNL_TITL',
              'JRNL_REF', 'JRNL_PMID', 'JRNL_DOI', 'COMMON_AUTHORS']

    field_counts, field_percentages = calculate_field_stats(data, fields)
    field_stats = {
        field: (field_counts[field], field_percentages[field]) for field in fields}

    doi_pmid_stats = calculate_doi_pmid_stats(data)

    results = format_results(field_stats, doi_pmid_stats)
    write_results(results, args.output)


if __name__ == "__main__":
    main()
