import os
import csv
import logging
import argparse
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process and combine CSV files.")
    parser.add_argument("-i", "--input_dir", required=True,
                        help="Path to the input directory")
    parser.add_argument("-o", "--output_dir", default="combined_files",
                        help="Path to the output directory")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    return parser.parse_args()


def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format='%(asctime)s - %(levelname)s - %(message)s')


def discover_files(input_dir):
    csv_files = []
    csv_dir = os.path.join(input_dir, "csv")
    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(csv_dir, file))
    return csv_files


def normalize_doi(doi):
    if not doi:
        return ''
    for prefix in ['http://doi.org/', 'https://doi.org/', 'http://dx.doi.org/', 'https://dx.doi.org/']:
        if doi.lower().startswith(prefix):
            doi = doi.lower().strip()
            doi = doi[len(prefix):]
    return doi


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")


def process_files(csv_files, csv_output):
    data_dict = {}
    logging.info(f"Processing {len(csv_files)} CSV files")
    for file in csv_files:
        logging.debug(f"Processing CSV file: {file}")
        try:
            with open(file, 'r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    normalized_objid = normalize_doi(row['objId'])
                    normalized_subjid = normalize_doi(row['subjId'])
                    key = f"{normalized_objid}|{normalized_subjid}"
                    updated = parse_date(row['updated'])
                    if key not in data_dict or updated > parse_date(data_dict[key]['updated']):
                        data_dict[key] = row
        except Exception as e:
            logging.error(f"Error processing CSV file {file}: {str(e)}")
    logging.info(f"Writing processed CSV data to {csv_output}")
    with open(csv_output, 'w', encoding='utf-8') as outfile:
        if data_dict:
            writer = csv.DictWriter(outfile, fieldnames=next(
                iter(data_dict.values())).keys())
            writer.writeheader()
            writer.writerows(data_dict.values())


def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    logging.info("Starting file processing")
    if not args.input_dir:
        logging.error(
            "Input directory is required. Use -i or --input_dir to specify it.")
        return
    csv_files = discover_files(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    logging.info(f"Output directory set to: {args.output_dir}")
    csv_output = os.path.join(args.output_dir, "combined_output.csv")
    process_files(csv_files, csv_output)
    logging.info("All files processed.")


if __name__ == "__main__":
    main()
