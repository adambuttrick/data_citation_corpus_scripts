import os
import re
import csv
import gzip
import argparse
from collections import defaultdict
from multiprocessing import Pool


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process PDB files and extract metadata")
    parser.add_argument('-i', '--input_dir', required=True,
                        help='Input directory containing PDB files')
    parser.add_argument('-o', '--output_file',
                        default="pdb_metadata.csv", help='Output CSV file')
    parser.add_argument('-t', '--threads', type=int,
                        default=4, help='Number of threads to use')
    return parser.parse_args()


def parse_pdb_content(file_path):
    parsed_data = defaultdict(list)
    current_field = None
    jrnl_subfield = None
    valid_fields = {'TITLE', 'KEYWDS', 'JRNL', 'AUTHOR'}
    valid_jrnl_subfields = {'AUTH', 'TITL', 'REF', 'PMID', 'DOI'}
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            line = line.strip()
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
                        content = re.sub(r'^\d+\s*', '', content)
                        parsed_data[f'JRNL_{jrnl_subfield}'].append(content)
                else:
                    content = re.sub(r'^\d+\s*', '', content)
                    parsed_data[current_field].append(content)
    for key in parsed_data:
        parsed_data[key] = ' '.join(parsed_data[key]).strip()
    return dict(parsed_data)


def find_common_authors(author_str, jrnl_auth_str):
    author_set = set(re.split(r',\s*', author_str))
    jrnl_auth_set = set(re.split(r',\s*', jrnl_auth_str))
    return ','.join(author_set.intersection(jrnl_auth_set))


def process_pdb_file(args):
    file_path, file_name = args
    pdb_id = file_name[3:7]  # Extract PDB ID from file name

    try:
        pdb_data = parse_pdb_content(file_path)
        pdb_data['PDB_ID'] = pdb_id
        pdb_data['COMMON_AUTHORS'] = find_common_authors(
            pdb_data.get('AUTHOR', ''), pdb_data.get('JRNL_AUTH', ''))
        return pdb_data
    except Exception as e:
        print(f"Error processing {file_name}: {str(e)}")
        return None


def main():
    args = parse_args()
    pdb_files = [(os.path.join(args.input_dir, f), f)
                 for f in os.listdir(args.input_dir) if f.endswith('.ent.gz')]
    with open(args.output_file, 'w', newline='') as outfile:
        fieldnames = ['PDB_ID', 'TITLE', 'KEYWDS', 'AUTHOR', 'JRNL_AUTH',
                      'JRNL_TITL', 'JRNL_REF', 'JRNL_PMID', 'JRNL_DOI', 'COMMON_AUTHORS']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        with Pool(args.threads) as p:
            for result in p.imap(process_pdb_file, pdb_files):
                if result:
                    writer.writerow(result)


if __name__ == "__main__":
    main()
