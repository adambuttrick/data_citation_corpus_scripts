# Combine DCC CSV files

Processes and combines multiple Data Citation Corpus (DCC) CSV files from , normalizing subject and object IDs and handling duplicate entries based on update timestamps.


## Usage
```
python csv_combiner.py -i INPUT_DIR [-o OUTPUT_DIR] [-v]
```

### Arguments

- `-i`, `--input_dir`: (Required) Path to the input directory containing the DCC CSV files
- `-o`, `--output_dir`: (Optional) Path to the output directory (default: "combined_files")
- `-v`, `--verbose`: (Optional) Enable verbose logging for debugging

## Input

Script expects the CSV files from the DCC data file, specifically a top-level directory contiaing CSV files in a "csv" directory. Each CSV file should contain at least the following columns:
- objId
- subjId
- updated

## Output

Script generates a single combined CSV file named "combined_output.csv" in the specified output directory.



