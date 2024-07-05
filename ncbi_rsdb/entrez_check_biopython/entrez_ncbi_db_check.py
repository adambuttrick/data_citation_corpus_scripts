import os
import csv
import argparse
from time import sleep
from Bio import Entrez, SeqIO


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Query NCBI for accession numbers and process results')
    parser.add_argument('-i', '--input_file',
                        required=True, help='Input CSV file')
    parser.add_argument('-e', '--email', required=True,
                        help="Email address for Entrez API")
    parser.add_argument('-o', '--output_file', help='Output CSV file')
    return parser.parse_args()


def query_ncbi(accession_number):
    try:
        handle = Entrez.efetch(
            db="nuccore", id=accession_number, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()
        lab_host = ''
        for feature in record.features:
            if feature.type == "source":
                lab_host = feature.qualifiers.get('lab_host', [''])[0]
        ncbi_base_url = "https://www.ncbi.nlm.nih.gov/nuccore/"
        ncbi_url = f"{ncbi_base_url}{accession_number}"
        return True, ncbi_url, lab_host
    except Exception as e:
        print(e)
        return False, None, None


def process_and_write(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Valid', 'NCBI_URL', 'Lab_Host']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            accession_number = row['accessionNumber']
            ncbi_url, lab_host, valid = query_ncbi(accession_number)
            row.update({
                'Valid': valid,
                'NCBI_URL': ncbi_url,
                'Lab_Host': lab_host
            })
            writer.writerow(row)
            sleep(1)
    print(f"Processing complete. Results written to {output_file}")


def main():
    args = parse_arguments()
    Entrez.email = args.email
    if args.output_file:
        output_file = args.output_file
    else:
        input_file_base = os.path.splitext(args.input_file)[0]
        output_file = f"{input_file_base}_w_ncbi_data.csv"
    process_and_write(args.input_file, output_file)


if __name__ == "__main__":
    main()
