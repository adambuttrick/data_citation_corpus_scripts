# Check ID Ensembl API

Validates accession numbers from data citation corpus using the Ensembl REST API.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python check_id_ensembl_api.py -i INPUT_FILE -o OUTPUT_FILE
```

## Arguments

- `-i`, `--input_file`: Path to input CSV file (required)
- `-o`, `--output_file`: Path to output CSV file (required)

## Output

Input CSV, with the following columns appended:
- `api_status`: 'valid', 'error', or 'failed'
- `error_message`: Error details if applicable
