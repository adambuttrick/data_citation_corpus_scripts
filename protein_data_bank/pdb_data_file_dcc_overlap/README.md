# PDB and Data Citation Corpus overlap analysis

Script to compare PDB-DOI pairs from aggregated PDB data with entries in the Data Citation Corpus.

## Usage
```
python pdb_data_file_dcc_overlap.py -p PDB_CSV -d DCC_CSV [-o OUTPUT_TXT] [-m MISSING_PAIRS_CSV]
```

## Arguments
- `-p`, `--pdb_file`: Path to the aggregate PDB data CSV file (required)
- `-d`, `--dcc_file`: Path to the Data Citation Corpus CSV file (required)
- `-o`, `--output_file`: Path to the output report file (default: stats.txt)
- `-m`, `--missing_pairs_file`: Path to the output CSV file for missing pairs (default: missing_pairs.csv)

## Output
1. Generates a text report (default: stats.txt) containing:
   - Total PDB-DOI pairs
   - Number of matched pairs
   - Percentage of matched pairs
   - Number of missing pairs

2. Creates a CSV file (default: missing_pairs.csv) listing PDB-DOI pairs found in the PDB data but missing from the Data Citation Corpus.