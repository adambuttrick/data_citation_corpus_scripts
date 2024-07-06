import csv
import math
import time
import requests
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="DOI Comparison System")
    parser.add_argument('-c', '--complete', required=True,
                        help="Path to complete dataset CSV")
    parser.add_argument('-s', '--sample', required=True,
                        help="Path to sample dataset CSV")
    parser.add_argument('-o', '--output', required=True,
                        help="Path to output summary CSV")
    return parser.parse_args()


def process_csv(file_path):
    result = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subj_id = row['subjId']
            obj_id = row['objId']
            if subj_id not in result:
                result[subj_id] = set()
            result[subj_id].add(obj_id)
    return result


def query_pubtator(subj_id):
    base_url = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/search/"
    dois = set()
    page = 1
    total_pages = 1
    last_request_time = 0
    while page <= total_pages:
        params = {
            'text': subj_id,
            'page': page
        }
        response = requests.get(base_url, params=params)
        last_request_time = time.time()
        response.raise_for_status()
        data = response.json()
        if page == 1:
            total_pages = data.get('total_pages', 1)
        for result in data['results']:
            if 'doi' in result:
                dois.add(result['doi'])
        page += 1
        time.sleep(3)
    return dois


def process_csv(file_path):
    result = {}
    doi_counts = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subj_id = row['subjId']
            obj_id = row['objId']
            if subj_id not in result:
                result[subj_id] = set()
                doi_counts[subj_id] = 0
            result[subj_id].add(obj_id)
            doi_counts[subj_id] += 1
    return result, doi_counts


def compare_and_write_dois(subj_id, complete_dois, pubtator_dois, writer, complete_doi_counts):
    complete_set = complete_dois.get(subj_id, set())
    pubtator_set = pubtator_dois
    overlap = complete_set.intersection(pubtator_set)
    overlap_count = len(overlap)
    overlap_percentage = (overlap_count / len(complete_set)
                          ) * 100 if complete_set else 0
    unique_complete = complete_set - pubtator_set
    unique_pubtator = pubtator_set - complete_set
    count_data_citation_corpus = complete_doi_counts.get(subj_id, 0)
    count_pubtator3 = len(pubtator_set)
    writer.writerow([
        subj_id,
        overlap_count,
        f"{overlap_percentage:.2f}%",
        count_data_citation_corpus,
        count_pubtator3,
        ','.join(overlap),
        ','.join(unique_complete),
        ','.join(unique_pubtator)
    ])


def process_and_write(complete_data, complete_doi_counts, sample_data, output_path):
    headers = ['subjId', 'Count Overlap', 'Percentage Overlap', 'Count Data Citation Corpus',
               'Count PubTator3', 'Overlapping DOIs', 'Unique Complete DOIs', 'Unique PubTator DOIs']
    total_subjects = len(sample_data)
    with open(output_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for index, subj_id in enumerate(sample_data.keys(), start=1):
            print(f"Processing subject {index} of {total_subjects}: {subj_id}")
            pubtator_dois = query_pubtator(subj_id)
            compare_and_write_dois(
                subj_id, complete_data, pubtator_dois, writer, complete_doi_counts)


def main():
    args = parse_arguments()
    try:
        complete_data, complete_doi_counts = process_csv(args.complete)
        sample_data, sample_doi_counts = process_csv(args.sample)
        process_and_write(complete_data, complete_doi_counts, sample_data, args.output)
        print(f"Summary CSV written to {args.output}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
