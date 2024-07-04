# Extract EMBL data

Script to reconcile European Nucleotide Archive entries from the data citation corpuse with EMBL API data.

## Installation
```
pip install -r requirements.txt
```

## Usage

```
python extract_embl_data.py -i INPUT_CSV [-o OUTPUT_CSV]
```

## Arguments

- `-i`, `--input_csv`: Path to input CSV file (required)
- `-o`, `--output_csv`: Path to output CSV file (optional)

## Output

Adds columns to the input CSV:
- URL (URL used to retrieve EMBL data)
- subjId_valid (Whether 200 response/accession ID was found in API)
- error_code (HTTP response code from API)
- RX, RA, RT, RL, CC (EMBL data fields)

If no output file is specified, creates `<input_filename>_w_embl_data.csv`.

## Notes
EMBL data fields, derived from [EMBL Data Format](https://bibiserv.cebitec.uni-bielefeld.de/sadr/data_formats/embl_df.html)
- RX (Reference Cross-reference): optional line type which contains a cross-reference to an external citation or abstract database.
- RA (Reference Author): lists the authors of the paper (or other work) cited.
- RT (Reference Title): give the title of the paper (or other work).
- RL (Reference Location): contains the conventional citation information for the reference.
- CC: free text comments about the entry, and may be used to convey any sort of information thought to be useful.