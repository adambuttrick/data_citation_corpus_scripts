import os
import csv
import argparse
import requests
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Reconcile European Nucleotide Archive entries in the data citation corpus file with EMBL data')
    parser.add_argument('-i', '--input_csv', help='Path to input CSV file')
    parser.add_argument('-o', '--output_csv',
                        help='Path to output CSV file (optional)')
    return parser.parse_args()


def fetch_embl_data(subj_id):
    url = f"https://www.ebi.ac.uk/ena/browser/api/embl/{subj_id}?lineLimit=1000"
    response = requests.get(url)
    return response.status_code, response.text if response.status_code == 200 else None


def parse_embl_data(embl_text):
    # Extracted from EMBL Data Format - https://bibiserv.cebitec.uni-bielefeld.de/sadr/data_formats/embl_df.html
    # RX (Reference Cross-reference): optional line type which contains a cross-reference to an external citation or abstract database.
    # RA (Reference Author): lists the authors of the paper (or other work) cited.
    # RT (Reference Title): give the title of the paper (or other work).
    # RL (Reference Location): contains the conventional citation information for the reference.
    # CC: free text comments about the entry, and may be used to convey any sort of information thought to be useful.
    data = defaultdict(list)
    current_section = None
    for line in embl_text.split('\n'):
        if line.startswith('RX'):
            data['RX'].append(line[5:].strip())
        elif line.startswith('RA'):
            data['RA'].append(line[5:].strip())
        elif line.startswith('RT'):
            data['RT'].append(line[5:].strip())
        elif line.startswith('RL'):
            data['RL'].append(line[5:].strip())
        elif line.startswith('CC'):
            data['CC'].append(line[5:].strip())
    return {k: ' '.join(v) for k, v in data.items()}


def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + \
            ['URL', 'subjId_valid', 'error_code', 'RX', 'RA', 'RT', 'RL', 'CC']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            subj_id = row['subjId']
            url = f"https://www.ebi.ac.uk/ena/browser/api/embl/{subj_id}?lineLimit=1000"
            row['URL'] = url
            status_code, embl_text = fetch_embl_data(subj_id)
            if status_code == 200:
                row['subjId_valid'] = 'True'
                row['error_code'] = ''
                embl_data = parse_embl_data(embl_text)
                row.update(embl_data)
            else:
                row['subjId_valid'] = 'False'
                row['error_code'] = str(status_code)
                row.update({
                    'RX': '',
                    'RA': '',
                    'RT': '',
                    'RL': '',
                    'CC': ''
                })
            writer.writerow(row)


def main():
    args = parse_arguments()
    input_file = args.input_csv
    if args.output_csv:
        output_file = args.output_csv
    else:
        input_base = os.path.splitext(input_file)[0]
        output_file = f"{input_base}_w_embl_data.csv"
    process_csv(input_file, output_file)


if __name__ == '__main__':
    main()
