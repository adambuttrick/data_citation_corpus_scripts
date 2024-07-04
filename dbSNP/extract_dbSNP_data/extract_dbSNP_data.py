import os
import csv
import json
import argparse
import requests
from time import sleep
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Query dbSNP API and process results')
    parser.add_argument('-i', '--input_file',
                        required=True, help='Input CSV file')
    parser.add_argument('-o', '--output_file', help='Output CSV file')
    return parser.parse_args()


def query_api(subj_id):
    url = f"https://api.ncbi.nlm.nih.gov/variation/v0/refsnp/{subj_id.lstrip('rs')}"
    response = requests.get(url)
    return url, response.ok, response.status_code, response.json() if response.ok else None


def extract_citation_ids(data):
    return ';'.join(map(str, data.get('citations', [])))


def extract_submitter_handles(data):
    handles = set()
    for support in data.get('primary_snapshot_data', {}).get('support', []):
        handle = support.get('submitter_handle')
        if handle:
            handles.add(handle)
    return ';'.join(sorted(handles))


def process_and_write(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + \
            ['API_URL', 'Valid_Response', 'Response_Code',
                'Citation_IDs', 'Submitter_Handles']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            subj_id = row['subjId']
            url, valid_response, response_code, data = query_api(subj_id)
            row.update({
                'API_URL': url,
                'Valid_Response': valid_response,
                'Response_Code': response_code,
                'Citation_IDs': extract_citation_ids(data) if data else '',
                'Submitter_Handles': extract_submitter_handles(data) if data else ''
            })
            writer.writerow(row)
            sleep(1)


def main():
    args = parse_arguments()
    if args.output_file:
        output_file = args.output_file
    else:
        input_file_base = os.path.splitext(args.input_file)[0]
        output_file = f"{input_file_base}_w_dbSNP_data.csv"
    process_and_write(args.input_file, output_file)
    print(f"Processing complete. Results written to {output_file}")


if __name__ == "__main__":
    main()
