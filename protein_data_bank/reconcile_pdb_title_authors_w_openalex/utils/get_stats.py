import csv
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process CSV and calculate statistics for specific fields")
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


def format_results(field_stats):
    results = "Field statistics:\n"
    for field, (count, percentage) in field_stats.items():
        results += f"{field}: {count} ({percentage:.2f}%)\n"
    return results


def write_results(results, output_file):
    with open(output_file, 'w') as f:
        f.write(results)


def main():
    args = parse_args()
    data = read_csv(args.input)
    fields = ['OpenAlex_ID', 'Author_Affiliations', 'ROR_IDs']
    field_counts, field_percentages = calculate_field_stats(data, fields)
    field_stats = {
        field: (field_counts[field], field_percentages[field]) for field in fields}
    results = format_results(field_stats)
    write_results(results, args.output)


if __name__ == "__main__":
    main()
