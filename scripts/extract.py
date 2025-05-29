# scripts/extract.py

import pandas as pd

def extract_raw_jobs():
    # Simulate reading raw data, or load your raw data file here
    data = [
        {"title": "Data Scientist", "company": "ABC Corp", "location": "New York", "description": "Experience with Python, ML"},
        {"title": "Software Engineer", "company": "XYZ Inc", "location": "San Francisco", "description": "Java, Cloud skills needed"},
    ]
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} job listings")
    df.to_csv("data/processed/raw_jobs.csv", index=False)
    print("Saved raw_jobs.csv to data/processed/")

if __name__ == "__main__":
    extract_raw_jobs()
