import os
import csv
import time
import argparse
import requests
from thefuzz import fuzz


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process CSV data using OpenAlex API")
    parser.add_argument("-i", "--input_file",
                        help="Path to the input CSV file")
    parser.add_argument("-o", "--output_file",
                        help="Path to the output CSV file")
    return parser.parse_args()


def get_openalex_data(doi=None, title=None):
    base_url = "https://api.openalex.org/works"
    params = {}
    if doi:
        params["filter"] = f"doi:https://doi.org/{doi}"
    elif title:
        params["search"] = f"{title}"
    else:
        return None
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["results"][0] if data["results"] else None
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None


def transform_name(name):
    parts = name.split()
    if len(parts) == 1:
        return name.upper()
    last_name = parts[-1].upper()
    initials = '.'.join(part[0].upper() for part in parts[:-1])
    return f"{initials}.{last_name}"


def match_authors(api_authors, common_authors):
    common_author_list = [author.strip()
                          for author in common_authors.split(',')]
    matched_authors = []
    for api_author in api_authors:
        display_name = api_author["author"]["display_name"]
        transformed_name = transform_name(display_name)
        for common_author in common_author_list:
            if common_author == transformed_name:
                matched_authors.append(api_author)
                break
            elif fuzz.ratio(transformed_name, common_author) > 80:
                matched_authors.append(api_author)
                break
    return matched_authors


def extract_affiliations(matched_authors):
    affiliations = []
    ror_ids = []
    for author in matched_authors:
        for institution in author.get("institutions", []):
            affiliations.append(institution.get("display_name", ""))
            ror_ids.append(institution.get("ror", ""))
    return ";".join(affiliations), ";".join(ror_ids)


def search_work(title):
    return get_openalex_data(title=title)


def process_record(row):
    result = row.copy()
    if row.get('JRNL_DOI') and row.get('COMMON_AUTHORS'):
        work_data = get_openalex_data(doi=row['JRNL_DOI'])
    elif row.get('JRNL_TITL'):
        work_data = search_work(row['JRNL_TITL'])
    else:
        work_data = None
    if work_data:
        matched_authors = match_authors(work_data.get(
            "authorships", []), row['COMMON_AUTHORS'])
        affiliations, ror_ids = extract_affiliations(matched_authors)
        result['Retrieved_DOI'] = work_data.get("doi", "")
        result['OpenAlex_ID'] = work_data.get("id", "")
        result['Author_Affiliations'] = affiliations
        result['ROR_IDs'] = ror_ids
    else:
        result['Retrieved_DOI'] = ""
        result['OpenAlex_ID'] = ""
        result['Author_Affiliations'] = ""
        result['ROR_IDs'] = ""
    time.sleep(1)
    return result


def process_and_write_iteratively(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + \
            ['Retrieved_DOI', 'OpenAlex_ID', 'Author_Affiliations', 'ROR_IDs']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            processed_row = process_record(row)
            writer.writerow(processed_row)
        print(f"Processing complete. Results written to {output_file}")


def main():
    args = parse_arguments()
    if args.output_file:
        output_file = args.output_file
    else:
        input_file_base = os.path.splitext(args.input_file)[0]
        output_file = f"{input_file_base}_reconciled_w_openalex.csv"

    process_and_write_iteratively(args.input_file, output_file)


if __name__ == "__main__":
    main()
