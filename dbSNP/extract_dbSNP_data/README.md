# Extract dbSNP data

Script to query dbSNP API for given SNP IDs, extract citation IDs and submitter handles, and append data to a CSV file.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python extract_dbSNP_data.py -i INPUT_CSV [-o OUTPUT_CSV]
```

## Arguments

- `-i`, `--input_file`: Input CSV file (required)
- `-o`, `--output_file`: Output CSV file (optional)

## Output

Creates a new CSV with additional columns for API response data, citation IDs, and submitter handles.