import csv
import argparse
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Compare PDB and DOI data from two CSV files.")
    parser.add_argument("-p", "--pdb_file", required=True,
                        help="Path to the aggregate PDB data file")
    parser.add_argument("-d", "--dcc_file", required=True,
                        help="Path to the data citation corpus CSV file")
    parser.add_argument("-o", "--output_file", default="stats.txt",
                        help="Path to the output report file")
    parser.add_argument("-m", "--missing_pairs_file", default="missing_pairs.csv",
                        help="Path to the output CSV file for missing pairs")
    return parser.parse_args()


def parse_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        return list(reader)


def normalize_doi(doi):
    if not doi:
        return ''
    doi = doi.lower().strip()
    for prefix in ['http://doi.org/', 'https://doi.org/', 'http://dx.doi.org/', 'https://dx.doi.org/']:
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi


def extract_pdb_doi_pairs(pdb_rows):
    pairs = []
    for row in pdb_rows:
        pdb_id = row['PDB_ID'].lower().strip()
        doi = normalize_doi(row['JRNL_DOI'])
        print(f"PDB: {pdb_id} - {doi}")  # Debug print
        if doi:
            pairs.append((pdb_id, doi))
    return pairs


def extract_dcc_doi_pairs(dcc_rows):
    pairs = []
    for row in dcc_rows:
        subj_id = row['subjId'].lower().strip()
        obj_id = normalize_doi(row['objId'])
        print(f"DCC: {subj_id} - {obj_id}") 
        pairs.append((subj_id, obj_id))
    return pairs


def create_id_doi_mapping(pairs):
    mapping = defaultdict(set)
    for id_, doi in pairs:
        mapping[id_].add(doi)
    return mapping


def compare_mappings(pdb_mapping, dcc_mapping):
    total_pdb_pairs = sum(len(dois) for dois in pdb_mapping.values())
    matched_pairs = 0
    missing_pairs = []
    for pdb_id, pdb_dois in pdb_mapping.items():
        if pdb_id in dcc_mapping:
            matched = pdb_dois.intersection(dcc_mapping[pdb_id])
            matched_pairs += len(matched)
            missing = pdb_dois - matched
        else:
            missing = pdb_dois
        for doi in missing:
            missing_pairs.append((pdb_id, doi))
    percentage = (matched_pairs / total_pdb_pairs) * \
        100 if total_pdb_pairs > 0 else 0
    return {
        "total_pdb_pairs": total_pdb_pairs,
        "matched_pairs": matched_pairs,
        "percentage": percentage,
        "missing_pairs": missing_pairs
    }


def generate_report(stats, output_file):
    with open(output_file, 'w') as f:
        f.write("PDB and DOI Comparison Report\n")
        f.write("============================\n\n")
        f.write(f"Total PDB-DOI pairs: {stats['total_pdb_pairs']}\n")
        f.write(f"Matched pairs: {stats['matched_pairs']}\n")
        f.write(f"Percentage matched: {stats['percentage']:.2f}%\n")
        f.write(f"Missing pairs: {len(stats['missing_pairs'])}\n")


def write_missing_pairs(missing_pairs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['PDB_ID', 'DOI'])
        writer.writerows(missing_pairs)


def main():
    args = parse_arguments()
    pdb_rows = parse_csv_file(args.pdb_file)
    dcc_rows = parse_csv_file(args.dcc_file)
    pdb_pairs = extract_pdb_doi_pairs(pdb_rows)
    dcc_pairs = extract_dcc_doi_pairs(dcc_rows)
    pdb_mapping = create_id_doi_mapping(pdb_pairs)
    dcc_mapping = create_id_doi_mapping(dcc_pairs)
    stats = compare_mappings(pdb_mapping, dcc_mapping)
    generate_report(stats, args.output_file)
    write_missing_pairs(stats['missing_pairs'], args.missing_pairs_file)
    print(f"Report generated: {args.output_file}")
    print(f"Missing pairs CSV generated: {args.missing_pairs_file}")


if __name__ == "__main__":
    main()
