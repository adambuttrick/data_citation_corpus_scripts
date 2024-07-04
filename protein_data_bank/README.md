# Filter CSV based on PDB current holdings file

Script to perform secondary validation of CSV files based on keys from a JSON object derived from the wwPDB current holdings file. This validation follows an initial validation of accession IDs using regexes, as is done for most other repos in the data citation corpus. The current holding JSON file contains information about all entries and is available at https://files.wwpdb.org/pub/pdb/holdings/current_file_holdings.json.gz. The script filters rows in the CSV based on the 'subjId' column matching keys in the JSON object.


## Usage

```
python filter_csv_pdb.py -j JSON_FILE -c CSV_FILE
```

## Arguments

- `-j`, `--json`: Path to JSON file (required)
- `-c`, `--csv`: Path to CSV file (required)

## Output

Creates two output CSV files in the same directory as the input CSV:
- `<input_filename>_valid.csv`: Rows where 'subjId' matches a JSON key
- `<input_filename>_invalid.csv`: Rows where 'subjId' does not match a JSON key

Both output files maintain the same header as the input CSV.