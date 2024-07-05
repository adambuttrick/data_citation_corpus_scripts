# Extract GEO Data

Script to extact data files from NCBI Gene Expression Omnibus entries for given subject IDs, extract contact information, and reconcile with corresponding data citation corpus entries file. Searches for an assigns ROR IDs to institutions. Optionally downloads raw GEO data files from which additional metadata is derived

## Installation

```
pip install -r requirements.txt
```
## Usage
```
python extract_geo_data.py -i INPUT_CSV [-o OUTPUT_CSV] [-d OUTPUT_DIR] [-f]
```
## Arguments
```
-i, --input_file: Input CSV file (required)
-o, --output_file: Output CSV file (optional)
-d, --output_dir: Directory to save raw GEO data files (optional)
-f, --file_download: Flag to download raw GEO data files (optional)
```
## Output

Creates a new CSV with additional columns for GEO data extracted from the file and ROR IDs.