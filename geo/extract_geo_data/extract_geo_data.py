import os
import re
import csv
import argparse
import requests
from datetime import datetime
from time import sleep


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process GEO data and extract contact information.")
    parser.add_argument("-i", "--input_file", required=True,
                        help="Path to the input CSV file")
    parser.add_argument("-o", "--output_file",
                        help="Path to the output CSV file")
    parser.add_argument("-d", "--output_dir",
                        help="Directory to save output files")
    parser.add_argument("-f", "--file_download", action="store_true",
                        help="Download raw GEO data files")
    return parser.parse_args()


def create_output_directories(base_dir=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not base_dir:
        base_dir = os.path.join(os.getcwd(), f"geo_output_{timestamp}")
    raw_dir = os.path.join(base_dir, f"raw_{timestamp}")
    os.makedirs(raw_dir, exist_ok=True)
    return base_dir, raw_dir, timestamp


def fetch_geo_data(subj_id):
    url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={subj_id}&targ=self&view=brief&form=text"
    response = requests.get(url)
    return response.text, response.status_code, url


def get_ror_id(org_name):
    if org_name is None or not re.search(r"[a-zA-Z]", org_name):
        return None
    org_name = re.sub(r'[{."\\]', "", org_name)
    ror_api_url = "https://api.ror.org/organizations"
    matched = requests.get(ror_api_url, {"affiliation": org_name})
    if matched.status_code != 200:
        return None
    matched = matched.json()
    for matched_org in matched["items"]:
        if matched_org["chosen"]:
            return matched_org["organization"]["id"]
    return None


def parse_geo_data(data):
    contact_name = ""
    contact_institute = ""
    contact_country = ""
    affiliation = ""
    for line in data.split('\n'):
        if "contact_name" in line.lower():
            name_parts = line.split('=', 1)[1].strip().split(',')
            contact_name = ' '.join(part.strip()
                                    for part in name_parts if part.strip())
        elif "contact_institute" in line.lower():
            contact_institute = line.split('=', 1)[1].strip()
        elif "contact_country" in line.lower():
            contact_country = line.split('=', 1)[1].strip()
    if contact_institute and contact_country:
        affiliation = f"{contact_institute}, {contact_country}"
    elif contact_institute:
        affiliation = contact_institute
    ror_id = get_ror_id(affiliation)
    return {
        "contact_name": contact_name,
        "contact_institute": contact_institute,
        "contact_country": contact_country,
        "affiliation": affiliation,
        "ror_id": ror_id
    }


def process_csv(input_file, raw_dir, output_csv, download_files):
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_csv, 'w', newline='', encoding='utf-8') as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + ['url', 'response_code', 'success',
                                          'contact_name', 'contact_institute', 'contact_country', 'affiliation', 'ror_id']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            subj_id = row['subjId']
            geo_data, status_code, url = fetch_geo_data(subj_id)
            row['url'] = url
            row['response_code'] = status_code
            row['success'] = status_code == 200
            if status_code == 200:
                if download_files:
                    with open(os.path.join(raw_dir, f"{subj_id}_raw.txt"), 'w', encoding='utf-8') as f:
                        f.write(geo_data)
                parsed_data = parse_geo_data(geo_data)
                row.update(parsed_data)
            else:
                row.update({k: '' for k in [
                           'contact_name', 'contact_institute', 'contact_country', 'affiliation', 'ror_id']})
            writer.writerow(row)
            sleep(2)


def main():
    args = parse_args()
    if args.output_file:
        output_file = args.output_file
    else:
        input_file_base = os.path.splitext(args.input_file)[0]
        output_file = f"{input_file_base}_w_GEO_data.csv"
    if args.file_download:
        base_dir, raw_dir, timestamp = create_output_directories(
            args.output_dir)
        print(f"Raw files saved in {raw_dir}")
        process_csv(args.input_file, raw_dir, output_file, args.file_download)
    else:
        process_csv(args.input_file, None, output_file, False)
    print(f"Processing complete.")
    print(f"Processed CSV saved as {output_file}")


if __name__ == "__main__":
    main()
