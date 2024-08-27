# Create Repository Distribution CSV

Counts repositories from a combined DCC CSV file, calculates percentages relative to the total, and outputs a deduplicated list of repositories with their counts and percentages.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python dedupe_repo_names_w_counts.py -i INPUT_FILE -o OUTPUT_FILE
```

### Arguments

- `-i`, `--input_file`: Path to the input CSV file
- `-o`, `--output_file`: Path to the output CSV file

## Input

Inputs is a combined DCC CSV file with a 'repository' column containing repository names.

## Output

Output is a CSV file with the following columns:
- repository: The name of the repository
- count: The number of occurrences of the repository
- percent_total: The percentage of the total entries this repository represents
