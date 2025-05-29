import os
import pandas as pd

# Define paths
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "raw_jobs_global.csv")

# Country-specific files: filename -> country
country_files = {
    "indeed_jobs_us.csv": "USA",
    "indeed_jobs_in.csv": "India",
    "indeed_jobs_uk.csv": "UK",
    # Add more files/countries if needed
}

all_data = []

for filename, country in country_files.items():
    file_path = os.path.join(RAW_DIR, filename)
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                print(f"Skipped empty file for {country}: {filename}")
                continue
            df["country"] = country
            all_data.append(df)
            print(f"Loaded {len(df)} rows from {country}")
        except pd.errors.EmptyDataError:
            print(f"Skipped empty file (error) for {country}: {filename}")
    else:
        print(f"File not found: {file_path}")

# Combine and save
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Saved combined data to {OUTPUT_FILE} with {len(combined_df)} rows.")
else:
    print("\n⚠️ No valid job data found to combine.")
