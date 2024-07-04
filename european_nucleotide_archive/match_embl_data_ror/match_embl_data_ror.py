import csv
import argparse
import re
import requests
import os
from flair.data import Sentence
from flair.models import SequenceTagger

ROR_URL = "https://api.ror.org/organizations"
MODEL_PATH = 'flair/ner-english'


def load_ner_model():
    return SequenceTagger.load(MODEL_PATH)


def extract_organisation_names(text, model):
    sentence = Sentence(text)
    model.predict(sentence)
    names = {entity.text for entity in sentence.get_spans(
        'ner') if entity.tag == 'ORG'}
    # INSDC is the International Nucleotide Sequence Database Collaboration to which most
    # entries appear to have been originally submitted, so exclude this value
    names = [name for name in names if name.strip() != "INSDC"]
    return list(names)


def get_ror_id(org_name):
    if org_name is None or not re.search(r"[a-zA-Z]", org_name):
        return None
    org_name = re.sub(r'[{."\\]', "", org_name)
    matched = requests.get(ROR_URL, {"affiliation": org_name})
    if matched.status_code != 200:
        return None
    matched = matched.json()
    for matched_org in matched["items"]:
        if matched_org["chosen"]:
            return matched_org["organization"]["id"]
    return None


def process_row(row, model):
    combined_text = row['RL'] + ' ' + row['CC']
    org_names = extract_organisation_names(combined_text, model)
    matched_ids = []
    for org_name in org_names:
        ror_id = get_ror_id(org_name)
        if ror_id:
            matched_ids.append(ror_id)
    row['matched_ids'] = ';'.join(matched_ids)
    row['extracted_orgs'] = ';'.join(org_names)
    return row


def parse_arguments():
    args = argparse.ArgumentParser(
        description="Process CSV containing European Nucleotide Archive entries in reconciled with EMBL data and attempt to match ROR IDs")
    args.add_argument("-i", "--input_file", required=True,
                      help="Path to the input CSV file")
    args.add_argument("-o", "--output_file",
                      help="Path to the output CSV file")
    return args.parse_args()


def main():
    args = parse_arguments()
    model = load_ner_model()

    if args.output_file:
        output_file = args.output_file
    else:
        input_base = os.path.splitext(args.input_file)[0]
        output_file = f"{input_base}_extracted_org_names_matched_ror.csv"

    with open(args.input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + ['matched_ids', 'extracted_orgs']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['subjId_valid'] == "True":
                if row['RL'] or row['CC']:
                    processed_row = process_row(row, model)
                    writer.writerow(processed_row)
                else:
                    row['matched_ids'] = ''
                    row['extracted_orgs'] = ''
                    writer.writerow(row)
            else:
                row['matched_ids'] = ''
                row['extracted_orgs'] = ''
                writer.writerow(row)
    print(f"Processing complete. Output written to {output_file}")


if __name__ == "__main__":
    main()
