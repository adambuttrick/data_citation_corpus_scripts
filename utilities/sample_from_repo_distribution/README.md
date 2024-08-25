# DCC Data Sampler

Samples and processes data from a combined Data Citation Corpus (DCC) CSV file, based on repository distribution.


## Installation
```
pip install -r requirements.txt
```

## Usage
```
python sample_dcc_data.py -i INPUT_FILE -r REPO_DISTRIBUTION_FILE -o OUTPUT_DIR -s SAMPLES_PER_GROUP [-n NUM_FILES]
```

### Arguments

- `-i`, `--input_file`: Path to the main data CSV file
- `-r`, `--repo_distribution_file`: Path to the repository distribution CSV file
- `-o`, `--output_dir`: Path to the output directory (default: "sample")
- `-s`, `--samples_per_group`: Number of samples to take per group
- `-n`, `--num_files`: Number of sample files to create per group (default: 1)

## Output

The script creates a directory structure in the specified output directory:

```
output_dir/
├── High_(>10%)/
│   ├── sample_1.csv
│   ├── sample_1.json
│   └── ...
├── Medium_(1-10%)/
│   ├── sample_1.csv
│   ├── sample_1.json
│   └── ...
├── Low_(0.1-1%)/
│   ├── sample_1.csv
│   ├── sample_1.json
│   └── ...
├── Very_Low_(<0.1%)/
│   ├── sample_1.csv
│   ├── sample_1.json
│   └── ...
└── Unspecified/
    ├── sample_1.csv
    ├── sample_1.json
    └── ...
```

Each sample file contains the specified number of randomly selected entries from the corresponding repository group.

## Repository Grouping

Repositories are grouped based on their percentage of the total data:

- High (>10%)
- Medium (1-10%)
- Low (0.1-1%)
- Very Low (<0.1%)
- Unspecified (for entries with missing or empty repository information)

