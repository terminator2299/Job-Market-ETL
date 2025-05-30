import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set Seaborn style
sns.set(style="whitegrid")

# Load transformed data
file_path = "data/processed/jobs_transformed.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

df = pd.read_csv(file_path)

# Drop rows with missing company names
df = df.dropna(subset=["company"])

# Count top 10 companies by number of job listings
top_companies = df["company"].value_counts().head(10).reset_index()
top_companies.columns = ["company", "job_count"]

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(data=top_companies, x="job_count", y="company", palette="Blues_r", legend=False)
plt.title("Top 10 Companies Hiring", fontsize=16)
plt.xlabel("Number of Job Listings", fontsize=12)
plt.ylabel("Company", fontsize=12)
plt.tight_layout()
plt.show()
