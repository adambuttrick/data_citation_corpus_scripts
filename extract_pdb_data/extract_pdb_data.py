import io
import os
import re
import csv
import gzip
import argparse
import requests
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process PDB files and extract metadata")
    parser.add_argument('-i', '--input_file',
                        required=True, help='Input CSV file')
    parser.add_argument('-o', '--output_file', help='Output CSV file')
    return parser.parse_args()


def fetch_pdb_file(subj_id):
    url = f"https://files.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb{subj_id.lower()}.ent.gz"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.status_code)
        return response.content
    else:
        return None


def parse_pdb_content(gzipped_content):
    parsed_data = defaultdict(list)
    current_field = None
    jrnl_subfield = None
    valid_fields = {'TITLE', 'KEYWDS', 'JRNL', 'AUTHOR'}
    valid_jrnl_subfields = {'AUTH', 'TITL', 'REF', 'PMID', 'DOI'}
    with gzip.GzipFile(fileobj=io.BytesIO(gzipped_content)) as f:
        for line in f:
            line = line.decode('utf-8').strip()
            field = line[:6].strip()
            content = line[10:].strip()
            if field in valid_fields:
                current_field = field
                if field == 'JRNL':
                    jrnl_subfield = content.split()[0]
                    if jrnl_subfield in valid_jrnl_subfields:
                        parsed_data[f'JRNL_{jrnl_subfield}'].append(' '.join(content.split()[1:]))
                    continue
                parsed_data[field].append(content)
            elif current_field in valid_fields and line.startswith(' '):
                if current_field == 'JRNL':
                    if jrnl_subfield in valid_jrnl_subfields:
                        # Remove line numbers if present
                        content = re.sub(r'^\d+\s*', '', content)
                        parsed_data[f'JRNL_{jrnl_subfield}'].append(content)
                else:
                    # Remove line numbers if present
                    content = re.sub(r'^\d+\s*', '', content)
                    parsed_data[current_field].append(content)
    for key in parsed_data:
        parsed_data[key] = ' '.join(parsed_data[key]).strip()
    return dict(parsed_data)


def find_common_authors(author_str, jrnl_auth_str):
    author_set = set(re.split(r',\s*', author_str))
    jrnl_auth_set = set(re.split(r',\s*', jrnl_auth_str))
    return ','.join(author_set.intersection(jrnl_auth_set))


def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['TITLE', 'KEYWDS', 'AUTHOR', 'JRNL_AUTH',
                                          'JRNL_TITL', 'JRNL_REF', 'JRNL_PMID', 'JRNL_DOI', 'COMMON_AUTHORS']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            subj_id = row['subjId']
            pdb_content = fetch_pdb_file(subj_id)
            if pdb_content:
                pdb_data = parse_pdb_content(pdb_content)
                print(pdb_data)
                row.update(pdb_data)
                row['COMMON_AUTHORS'] = find_common_authors(
                    pdb_data.get('AUTHOR', ''), pdb_data.get('JRNL_AUTH', ''))
            writer.writerow(row)


def main():
    args = parse_args()
    if args.output_file:
        output_file = args.output_file
    else:
        input_file_base = os.path.splitext(args.input_file)[0]
        output_file = f"{input_file_base}_w_pdb_metadata.csv"
    process_csv(args.input_file, output_file)


if __name__ == "__main__":
    main()
