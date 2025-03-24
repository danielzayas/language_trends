## Programing Language Trends

Programming language popularity over time, as measured by the # of `git push` to Github:

![language_trends](https://github.com/user-attachments/assets/8c636b3b-4c94-40de-be71-a80fd3b95e08)

## Data

`languages.csv` data through 2024 Q3 was sourced from https://github.com/github/innovationgraph/blob/main/data/languages.csv on 2024-03-23 around 11pm PT.

I also create a new Issue https://github.com/github/innovationgraph/issues/47 to ask for more recent data (2024 Q4, 2025 Q1, etc.).

## Acknowledgements

1. Github for publishing the CSV. Y'all should really improve the data visualization on your https://innovationgraph.github.com/global-metrics/programming-languages page though.
2. @madnight for creating a beautiful UI under the AGPL 3.0 license at https://github.com/madnight/githut, but sadly the last quarter in the data source is 2024 Q1.

## Open Questions

Filterting https://madnight.github.io/githut/#/pushes/2024/1, which is powered by https://github.com/madnight/githut, for "PUSHES" through 2024 Q1 tells a very different story about language trends. For example, consider 2024 Q1. Github's `languages.csv` has JavaScript at 18% of pushes versus @madnight's data source has JavaScript at 11% of pushes. Why the large discrepancy?:

I created https://github.com/madnight/githut/issues/120 to ask @madnight if he has any insights on this. 

![Screenshot 2025-03-23 at 10 53 35 PM](https://github.com/user-attachments/assets/bf767658-9a15-49ec-9e99-ab470470832d)

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (install in a virtual environment):
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install pandas matplotlib
  ```

### Generate the SQLite Database

The SQLite database provides faster querying capabilities for the analysis:

```bash
# Activate the virtual environment if not already activated
source .venv/bin/activate

# Convert CSV to SQLite database
python csv_to_sqlite.py
```

This will create a `languages.db` file with a `languages` table containing all the data from the CSV.

### Generate the Visualization

To create the language trends visualization:

```bash
# Activate the virtual environment if not already activated
source .venv/bin/activate

# Run the visualization script
python language_trends.py
```

This will create the `language_trends.png` file showing programming language popularity trends over time.
