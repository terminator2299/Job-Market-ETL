# analysis/summary_reports.py

import pandas as pd

def summary_reports():
    df = pd.read_csv("data/processed/jobs_transformed.csv")
    
    print("Columns:", df.columns.tolist())
    
    # Top paying roles by location
    top_roles = df.groupby(['location', 'title'])['salary_parsed'].mean().reset_index()
    top_roles = top_roles.sort_values('salary_parsed', ascending=False)
    print("\nTop paying roles by location (sample):")
    print(top_roles.head())
    
    # Skills demand
    all_skills = df.explode('skills')
    skills_demand = all_skills['skills'].value_counts().reset_index()
    skills_demand.columns = ['skill', 'demand']
    print("\nTop in-demand skills:")
    print(skills_demand.head())

if __name__ == "__main__":
    summary_reports()
