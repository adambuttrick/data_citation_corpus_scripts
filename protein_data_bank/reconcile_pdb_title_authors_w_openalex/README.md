# PDB OpenAlex Data Reconciliation

Script to reconcile data citation corpus + PDB metadata file with OpenAlex API, matching works to extact authors and affiliations.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python reconcile_pdb_title_authors_w_openalex.py -i INPUT_CSV [-o OUTPUT_CSV]
```

## Arguments

- `-i`, `--input_file`: Input CSV file (required)
- `-o`, `--output_file`: Output CSV file (optional)


## Output
Creates a new CSV with additional columns:
- Retrieved_DOI
- OpenAlex_ID (Work ID for OpenAlex retrieve by DOI or Title Search)
- Author_Affiliations (Affiliations matching to COMMON_AUTHORS in the PDB metadata)
- ROR_IDs (ROR IDs for matched author affiliation)
