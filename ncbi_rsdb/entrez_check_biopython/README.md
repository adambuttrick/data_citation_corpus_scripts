
# Entrez NCBI DB Check

Script to query NCBI for accession numbers, verify their existence, and return the NCBI URL and lab host details.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python entrez_ncbi_db_check.py -i INPUT_CSV [-o OUTPUT_CSV]
```

## Arguments

```
-i, --input_file: Input CSV file (required)
-o, --output_file: Output CSV file (optional)
```

## Output

Creates a new CSV with additional columns for the NCBI URL, lab host, and validity of each accession number.