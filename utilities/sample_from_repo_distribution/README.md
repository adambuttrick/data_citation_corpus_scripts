# DCC Data Sampler

Samples and processes data from a combined Data Citation Corpus (DCC) CSV file, based on repository distribution and creates additional samples for unspecified and random data.

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
├── Medium_(1-10%)/
├── Low_(0.1-1%)/
├── Very_Low_(<0.1%)/
├── Unspecified/
└── Random_Sample/
```

Each directory contains sample files (both CSV and JSON) based on the specified parameters.

## Repository Grouping

Repositories are grouped based on their percentage of the total data:

- High (>10%)
- Medium (1-10%)
- Low (0.1-1%)
- Very Low (<0.1%)

## Additional Sampling

In addition to the repository-based samples, the script provides two more types of samples:

1. **Unspecified Data**: Entries with missing or empty repository information are grouped under the "Unspecified" category. These are sampled separately to ensure representation of data without clear repository attribution.

2. **Random Sampling**: A random sample is created from across all input data, including both specified and unspecified repository entries. This provides an unbiased representation of the entire dataset.
