# PDB Metadata Extractor

Script to process valid Protein Data Bank (PDB) entries from the data citation corpus, extract metadata from the corresponding wwPDB entry, and append it to a CSV file. 


## Installation

```
pip install -r requirements.txt
```

## Usage

```
python script.py -i INPUT_CSV [-o OUTPUT_CSV]
```

## Arguments

- `-i`, --input_file`: Input CSV file (required)
- `-o`, `--output_file`: Output CSV file (optional)


## Functionality

1. Reads input CSV (output from previous accession number validation)
2. Fetches PDB files from wwPDB using the URL structure:
   `https://files.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb{subj_id.lower()}.ent.gz`
3. Extracts metadata (TITLE, KEYWDS, AUTHOR, JRNL fields) from PDB file
   a. See [pdb_metadata_example](https://drive.google.com/drive/folders/192Yuo3MrftTBAyYhQXSgeowlUnLkoAXw?usp=drive_link) for entity file 
4. Appends metadata to CSV
5. Identifies common authors between deposit and referenced publication in metadata
6. Writes results to output CSV

## Output
Creates a new CSV with additional columns for PDB metadata.
