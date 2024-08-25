import os
import csv
import json
import logging
import argparse
import numpy as np
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Sample DCC data and convert to JSON')
    parser.add_argument('-i', '--input_file',
                        help='Path to the main data CSV file')
    parser.add_argument('-r', '--repo_distribution_file',
                        help='Path to the repository distribution CSV file')
    parser.add_argument('-o', '--output_dir', default="sample",
                        help='Path to the output directory')
    parser.add_argument('-s', '--samples_per_group', type=int,
                        help='Number of samples to take per group')
    parser.add_argument('-n', '--num_files', type=int, default=1,
                        help='Number of sample files to create per group')
    return parser.parse_args()


def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully loaded data from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {str(e)}")
        raise


def load_repo_distribution(file_path):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['repository', 'percent_total']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
        logging.info(f"Successfully loaded repository distribution from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error loading repository distribution from {file_path}: {str(e)}")
        raise


def group_repositories(repo_df):
    repo_df = repo_df.sort_values('percent_total', ascending=False)
    groups = {
        'High (>10%)': [],
        'Medium (1-10%)': [],
        'Low (0.1-1%)': [],
        'Very Low (<0.1%)': [],
        'Unspecified': []
    }
    for _, row in repo_df.iterrows():
        repo = row['repository']
        percent = row['percent_total']
        if pd.isna(repo) or repo.strip() == '':
            continue
        if percent > 0.1:
            groups['High (>10%)'].append(repo)
        elif percent > 0.01:
            groups['Medium (1-10%)'].append(repo)
        elif percent > 0.001:
            groups['Low (0.1-1%)'].append(repo)
        else:
            groups['Very Low (<0.1%)'].append(repo)

    logging.info(f"Grouped repositories: {', '.join(f'{k}: {len(v)}' for k, v in groups.items())}")
    return groups


def sample_data(data_df, repo_groups, samples_per_group, num_files):
    sampled_data = {}
    unspecified_repos_data = data_df[data_df['repository'].isna() | (
        data_df['repository'].str.strip() == '')]
    if not unspecified_repos_data.empty:
        sampled_data['Unspecified'] = [unspecified_repos_data.sample(
            n=min(len(unspecified_repos_data), samples_per_group)) for _ in range(num_files)]
        logging.info(f"Created {num_files} samples for 'Unspecified' repository group")
    for group_name, repos in repo_groups.items():
        if group_name == 'Unspecified':
            continue
        group_data = data_df[data_df['repository'].isin(repos)]
        if len(group_data) <= samples_per_group:
            sampled_data[group_name] = [group_data] * num_files
            logging.info(f"Group {group_name}: Using all {len(group_data)} available samples for each file")
        else:
            sampled_data[group_name] = [group_data.sample(
                n=samples_per_group) for _ in range(num_files)]
            logging.info(f"Group {group_name}: Created {num_files} samples, each with {samples_per_group} samples out of {len(group_data)} available")
    return sampled_data


def create_random_sample(data_df, samples_per_group, num_files):
    random_samples = []
    for _ in range(num_files):
        random_sample = data_df.sample(n=min(len(data_df), samples_per_group))
        random_samples.append(random_sample)
    logging.info(f"Created {num_files} random samples, each with {samples_per_group} samples out of {len(data_df)} available")
    return random_samples


def create_nested_object(data, keys):
    for key in keys:
        if key in data and pd.notna(data[key]):
            return {
                "title": data[key],
                "external_id": None
            }
    return None


def convert_to_array(value):
    if pd.isna(value):
        return []
    return [item.strip() for item in str(value).split(';') if item.strip()]


def transform_row(row):
    def replace_nan(value):
        return None if pd.isna(value) else value
    transformed = {
        "id": replace_nan(row.get("id")),
        "created": replace_nan(row.get("created")),
        "updated": replace_nan(row.get("updated")),
        "repository": create_nested_object(row, ["repository"]),
        "publisher": create_nested_object(row, ["publisher"]),
        "journal": create_nested_object(row, ["journal"]),
        "title": replace_nan(row.get("title")),
        "objId": replace_nan(row.get("objId")),
        "subjId": replace_nan(row.get("subjId")),
        "publishedDate": replace_nan(row.get("publishedDate")),
        "accessionNumber": replace_nan(row.get("accessionNumber")),
        "doi": replace_nan(row.get("doi")),
        "relationTypeId": replace_nan(row.get("relationTypeId")),
        "source": replace_nan(row.get("source")),
        "affiliations": convert_to_array(row.get("affiliations")),
        "funders": convert_to_array(row.get("funders")),
        "subjects": convert_to_array(row.get("subjects"))
    }
    return transformed


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def write_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2,
                      ensure_ascii=False, cls=NpEncoder)
        logging.info(f"JSON data has been written to {file_path}")
    except IOError as e:
        logging.error(f"Error writing to JSON file: {e}")
        raise


def generate_output(sampled_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for group_name, samples in sampled_data.items():
        group_dir = os.path.join(output_dir, group_name.replace(' ', '_'))
        os.makedirs(group_dir, exist_ok=True)
        for i, sample_df in enumerate(samples):
            csv_file_name = f"sample_{i+1}.csv"
            json_file_name = f"sample_{i+1}.json"
            csv_file_path = os.path.join(group_dir, csv_file_name)
            json_file_path = os.path.join(group_dir, json_file_name)
            sample_df.to_csv(csv_file_path, index=False)
            logging.info(f"Saved CSV sample to {csv_file_path}")
            transformed_data = [transform_row(row)
                                for _, row in sample_df.iterrows()]
            write_json(transformed_data, json_file_path)
            logging.info(f"Saved JSON sample to {json_file_path}")


def main():
    args = parse_arguments()
    try:
        data_df = load_data(args.input_file)
        repo_df = load_repo_distribution(args.repo_distribution_file)
        repo_groups = group_repositories(repo_df)
        sampled_data = sample_data(
            data_df, repo_groups, args.samples_per_group, args.num_files)
        generate_output(sampled_data, args.output_dir)
        random_samples = create_random_sample(
            data_df, args.samples_per_group, args.num_files)
        random_output_dir = os.path.join(args.output_dir, "Random_Sample")
        generate_output({"Random": random_samples}, random_output_dir)

        logging.info(
            "Data sampling, CSV saving, and JSON serialization completed successfully")
    except Exception as e:
        logging.error(f"An error occurred during execution: {str(e)}")


if __name__ == "__main__":
    main()
