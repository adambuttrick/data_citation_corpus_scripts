# Dedupe repositories w/ counts

Script to deduplicate repository list from combined data citation corpus CSV file and count the number of times each repository is referenced.

## Usage
```
python dedupe_repo_names_w_counts.py -i INPUT_FILE -o OUTPUT_FILE
```

## Arguments
- `-i`, `--input_file`: Path to input CSV file (required)
- `-o`, `--output_file`: Path to output CSV file (default is 'dedupe_repo_names_w_counts.csv')

## Input
Combined data citation corpus CSV file with a 'repository' column.

## Output
CSV file with deduplicated repository names and their counts.


## Notes
To quickly cat the files while dropping the headers from every file but the first: `awk 'FNR==1 && NR!=1{next;}{print}' *.csv > combined_output.csv`