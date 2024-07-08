# PDB bulk data extractor

Script to process [Protein Data Bank (PDB)](https://www.rcsb.org)  files and extract metadata into a CSV file.

## Usage
```
python pdb_bulk_data_extract.py -i INPUT_DIR [-o OUTPUT_CSV] [-t THREADS]
```

## Arguments
- `-i`, `--input_dir`: Directory containing PDB files (required)
- `-o`, `--output_file`: Output CSV file (default: pdb_metadata.csv)
- `-t`, `--threads`: Number of threads to use (default: 4)

## Output
Creates a CSV file with the following columns:

- PDB_ID: Identifier of the PDB entry
- TITLE: The title of the deposit
- KEYWDS: Keywords describing the contents of the entry
- AUTHOR: The list of authors who deposited the structure
- JRNL_AUTH: Authors of the primary citation
- JRNL_TITL: Title of the article associated with the deposits
- JRNL_REF: Reference to the publication, including journal name, volume, page numbers, and year
- JRNL_PMID: PubMed identifier for the primary citation
- JRNL_DOI: Digital Object Identifier for the primary citation
- COMMON_AUTHORS: Intersection of authors listed in AUTHOR and JRNL_AUTH fields

## Obtaining PDB Files
All PDB files can be obtained using the following rsync command:

```
rsync -avz --delete --copy-links --port=33444 rsync.rcsb.org::ftp_data/structures/all/pdb/ .
```