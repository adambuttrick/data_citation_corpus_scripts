Here's a concise README for the match_embl_data_ror.py script:

# match_embl_data_ror

Script to process CSV files containing European Nucleotide Archive entries reconciled with EMBL data, extracting organization names and matching ROR IDs. Uses the `ner-english-large` model from the [Flair library](https://github.com/flairNLP/flair?tab=readme-ov-file) for named entity recognition (NER) to identify organization names and the ROR API to retrieve the associated ROR IDs.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python match_embl_data_ror.py -i INPUT_FILE [-o OUTPUT_FILE]
```

## Arguments

- `-i`, `--input_file`: Path to input CSV file (required)
- `-o`, `--output_file`: Path to output CSV file (optional)

## Output

Adds columns to the input CSV:
- matched_ids: Semicolon-separated list of matched ROR IDs
- extracted_orgs: Semicolon-separated list of extracted organization names

If no output file is specified, creates `<input_filename>_w_embl_data.csv`.
