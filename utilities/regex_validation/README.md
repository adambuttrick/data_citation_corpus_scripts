# regex validation

Script to validate subject IDs in the data citation corpus CSV files based on a repository name and regex pattern. Use the [Bioregistry](https://bioregistry.io) or a similar resource to derive the regex patterns for each repository.

## Usage

```
python regex_validation.py -i INPUT_FILE -r REPOSITORY -p PATTERN
```

## Arguments

- `-i`, `--input_file`: Input CSV file (required)
- `-r`, `--repository`: Repository name to filter (required)
- `-p`, `--pattern`: Regex pattern for subjID validation (required)


## Output

- Valid rows: `<normalized_repository_name>_valid.csv`
- Invalid rows: `<normalized_repository_name>_invalid.csv`

The normalized filename removes spaces, special characters, and file extensions from the repository name.

## Notes

This is a naive form of validation of the data and some repositories may require additional validation criteria for their subject IDs.