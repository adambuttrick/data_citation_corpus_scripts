import csv
import argparse
from collections import Counter


def parse_args():
    p = argparse.ArgumentParser(
        description="Process CSV and calculate statistics")
    p.add_argument("-i", "--input", required=True, help="Input CSV file path")
    p.add_argument("-o", "--output", default="stats.txt", help="Output file path for results")
    return p.parse_args()


def read_csv(f):
    data = []
    with open(f, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def calculate_stats(d):
    total = len(d)
    valid = sum(1 for row in d if row['subjId_valid'].lower() == 'true')
    valid_extracted = sum(1 for row in d if row['subjId_valid'].lower(
    ) == 'true' and row['extracted_orgs'])
    valid_matched = sum(
        1 for row in d if row['subjId_valid'].lower() == 'true' and row['matched_ids'])

    return {
        'total': total,
        'valid': valid,
        'valid_extracted': valid_extracted,
        'valid_matched': valid_matched
    }


def format_results(s):
    total, valid = s['total'], s['valid']
    percent_valid = (valid / total) * 100 if total > 0 else 0
    percent_extracted = (s['valid_extracted'] / valid) * \
        100 if valid > 0 else 0
    percent_matched = (s['valid_matched'] / valid) * 100 if valid > 0 else 0

    return (
        f"Total entries: {total}\n"
        f"Valid entries (subjId_valid = True): {valid} ({percent_valid:.2f}%)\n"
        f"Valid entries with extracted_orgs: {s['valid_extracted']} ({percent_extracted:.2f}%)\n"
        f"Valid entries with matched_ids: {s['valid_matched']} ({percent_matched:.2f}%)"
    )


def write_results(r, o):
    if o:
        with open(o, 'w') as f:
            f.write(r)
    else:
        print(r)


def main():
    args = parse_args()
    data = read_csv(args.input)
    stats = calculate_stats(data)
    results = format_results(stats)
    write_results(results, args.output)


if __name__ == "__main__":
    main()
