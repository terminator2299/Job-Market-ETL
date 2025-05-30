import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for seaborn
sns.set(style="whitegrid")

# Path to the transformed jobs data
file_path = "data/processed/jobs_transformed.csv"

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load the dataset
df = pd.read_csv(file_path)

# Drop rows with missing salary info
df = df.dropna(subset=["salary_min", "salary_max"])

# Create average salary column
df["average_salary"] = (df["salary_min"] + df["salary_max"]) / 2

# Plot salary distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["average_salary"], bins=30, kde=True, color="skyblue")
plt.title("Salary Distribution of Jobs", fontsize=16)
plt.xlabel("Average Salary", fontsize=12)
plt.ylabel("Job Count", fontsize=12)
plt.tight_layout()
plt.show()
