# PubTator3-Data Citation Corpus overlap analysis

Script to compare DOIs associated with a subject ID in the data citation corpus with those retrieved from the [PubTator3](https://www.ncbi.nlm.nih.gov/research/pubtator3/) tagging for a sample dataset. Processes data citation corpus entries, queries the PubTator3 API, and generates a summary of the DOI overlap and unique entries.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python doi_comparison_system.py -c COMPLETE_FILE -s SAMPLE_FILE -o OUTPUT_FILE
```

## Arguments

- `-c`, `--complete`: Path to complete dataset CSV file (complete set of valid rows for a repo in the corpus, required)
- `-s`, `--sample`: Path to sample dataset CSV file (sample from valid rows for a repo, required)
- `-o`, `--output`: Path to output summary CSV file (required)

## Output

Generates a CSV file with the following columns:
- subjId: Subject ID
- Count Overlap: Number of overlapping DOIs
- Percentage Overlap: Percentage of overlapping DOIs
- Count Data Citation Corpus: Number of DOIs in the complete dataset
- Count PubTator3: Number of DOIs returned by PubTator3 API
- Overlapping DOIs: Comma-separated list of overlapping DOIs
- Unique Complete DOIs: Comma-separated list of DOIs unique to the complete dataset
- Unique PubTator DOIs: Comma-separated list of DOIs unique to PubTator3 results

## Notes

Pubtator3 API rate limiting seemed fairly bad and returned slightly differnt result counts, so rate limit is set very conservatively to 1 request per 3 secs.