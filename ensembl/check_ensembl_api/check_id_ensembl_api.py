import re
import csv
import requests
import argparse
from itertools import islice
from urllib.parse import quote, urlparse
from multiprocessing import Pool, cpu_count


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Validate subject IDs from CSV using BioStudies API')
    parser.add_argument('-i', '--input_file', help='Input CSV file path')
    parser.add_argument('-o', '--output_file', help='Output CSV file path')
    return parser.parse_args()


def extract_id(value):
    match = re.search(r'(ENS[A-Z]*\d+)(?:\.\d+)?', value)
    if match:
        value = match.group(1)
        value = re.sub("_", "", value)
    return value


def query_api(subj_id):
    url = f"https://rest.ensembl.org/archive/id/{quote(subj_id)}?content-type=application/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_response = response.json()
        if 'errorMessage' in json_response:
            return 'error', json_response['errorMessage']
        return 'valid', ''
    except requests.exceptions.RequestException as e:
        return 'failed', str(e)


def process_row(row):
    subj_id = extract_id(row['accession_number'])
    status, message = query_api(subj_id)
    row['api_status'] = status
    row['error_message'] = message
    return row


def process_chunk(chunk):
    with Pool(processes=min(5, cpu_count())) as pool:
        return pool.map(process_row, chunk)


def process_csv(input_file, output_file, chunk_size=100):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['api_status', 'error_message']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            chunk = list(islice(reader, chunk_size))
            if not chunk:
                break
            processed_chunk = process_chunk(chunk)
            writer.writerows(processed_chunk)


def main():
    args = parse_arguments()
    process_csv(args.input_file, args.output_file)
    print(f"Processing complete. Output written to {args.output_file}")


if __name__ == "__main__":
    main()
