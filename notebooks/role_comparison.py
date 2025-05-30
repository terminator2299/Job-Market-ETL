import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the path
file_path = "data/processed/jobs_transformed.csv"

# Load the dataset
df = pd.read_csv(file_path)

# --- Step 1: Standardize column names if needed ---
df.columns = df.columns.str.lower().str.strip()

# Rename for consistency if needed
if 'salary_min' in df.columns:
    df = df.rename(columns={"salary_min": "min_salary", "salary_max": "max_salary"})
elif 'min_salary' not in df.columns or 'max_salary' not in df.columns:
    raise KeyError("Salary columns 'min_salary' and/or 'max_salary' missing from data.")

if 'title' in df.columns and 'role' not in df.columns:
    df = df.rename(columns={"title": "role"})

# --- Step 2: Drop entries with missing salary or role ---
df = df.dropna(subset=["min_salary", "max_salary", "role"])

# --- Step 3: Clean and Normalize Roles ---
def normalize_role(role):
    role = role.lower()
    if "data scientist" in role:
        return "Data Scientist"
    elif "data analyst" in role:
        return "Data Analyst"
    elif "machine learning" in role:
        return "ML Engineer"
    elif "software engineer" in role:
        return "Software Engineer"
    elif "devops" in role:
        return "DevOps Engineer"
    elif "data engineer" in role:
        return "Data Engineer"
    elif "ai" in role:
        return "AI Engineer"
    else:
        return role.title()

df["role"] = df["role"].apply(normalize_role)

# --- Step 4: Remove internships, entry-level, juniors ---
df = df[~df["role"].str.contains("intern|junior|entry", case=False)]

# Optional: filter only US or specific country to remove INR/GBP
# df = df[df["location"].str.contains("United States|USA", na=False, case=False)]

# --- Step 5: Calculate average salary ---
df["avg_salary"] = (df["min_salary"] + df["max_salary"]) / 2

role_salary = df.groupby("role")["avg_salary"].mean().sort_values(ascending=False).head(15)

# --- Step 6: Plot ---
plt.figure(figsize=(12, 6))
sns.barplot(x=role_salary.values, y=role_salary.index, palette="Blues_r")
plt.xlabel("Average Salary")
plt.ylabel("Role")
plt.title("Average Salary by Role")
plt.tight_layout()
plt.show()
