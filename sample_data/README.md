# Sample Data Output Description

This directory contains sampled data from the Data Citation Corpus (DCC) file. The samples are organized to represent the distribution of entries in the original dataset, with additional categories for random sampling and entries with unspecified repositories.

## Directory Structure and Representation

The main sample directory contains the following subdirectories, each representing a different category based on the repository's representation in the total dataset:

1. High_(>10%)
2. Medium_(1-10%)
3. Low_(0.1-1%)
4. Very_Low_(<0.1%)
5. Unspecified
6. Random_Sample

This structure reflects the actual distribution of entries in the Data Citation Corpus:

- "High_(>10%)" contains samples from repositories that account for more than 10% of the total entries.
- "Medium_(1-10%)" represents repositories contributing between 1% and 10% of entries.
- "Low_(0.1-1%)" includes repositories with 0.1% to 1% of total entries.
- "Very_Low_(<0.1%)" covers repositories with less than 0.1% representation.
- "Unspecified" contains entries where the repository information was not provided.
- "Random_Sample" offers a completely random selection from the entire dataset, regardless of repository distribution.

## Sample Files

In each subdirectory, there are three sets of sample files:

1. sample_1.csv and sample_1.json
2. sample_2.csv and sample_2.json
3. sample_3.csv and sample_3.json

Each sample contains 50,000 randomly selected items from its respective category, maintaining the proportional representation of the original dataset.

## Data Contents

The CSV files contain the raw data in tabular format, while the JSON files present the same data in a structured, hierarchical format. Each item in the samples typically includes information such as:

| Field         | Description                                     | Required? |
|---------------|-------------------------------------------------|-----------|
| id            | Internal identifier for the citation            | Yes       |
| created       | Date of item's incorporation into the corpus    | Yes       |
| updated       | Date of item's most recent update in corpus     | Yes       |
| repository    | Repository where cited data is stored           | No        |
| publisher     | Publisher for the article citing the data       | No        |
| journal       | Journal for the article citing the data         | No        |
| title         | Title of cited data                             | No        |
| publication   | DOI of article where data is cited              | Yes       |
| dataset       | DOI or accession number of cited data           | Yes       |
| publishedDate | Date when citing article was published          | No        |
| source        | Source where citation was harvested             | Yes       |
| subjects      | Subject information for dataset                 | No        |
| affiliations  | Affiliation information for creator of cited data | No      |
| funders       | Funding information for cited data              | No        |

## Notes

When using this data, please refer to the original [Data Citation Corpus documentation](https://support.datacite.org/docs/data-citation-corpus) for detailed descriptions of each field and any data usage guidelines or restrictions.