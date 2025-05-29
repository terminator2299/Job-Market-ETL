# scripts/transform.py

import pandas as pd
from .utils import parse_salary


def transform_jobs():
    df = pd.read_csv("data/processed/raw_jobs.csv")
    
    # Example: Add a salary column with dummy salary data for testing
    df['salary'] = ["$100,000", "$120,000"]
    
    # Parse salary to numeric
    df['salary_parsed'] = df['salary'].apply(parse_salary)
    
    # Example: Extract skills from description (simple split)
    df['skills'] = df['description'].str.lower().str.replace(',', '').str.split()
    
    df.to_csv("data/processed/jobs_transformed.csv", index=False)
    print("Saved jobs_transformed.csv to data/processed/")

if __name__ == "__main__":
    transform_jobs()
