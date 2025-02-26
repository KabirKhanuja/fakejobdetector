import pandas as pd

# Load datasets
job_data = pd.read_csv("job_dataset_final.csv")
company_scores = pd.read_csv("company_legitimacy_scores.csv")

# Standardize column names
job_data.columns = job_data.columns.str.strip().str.lower()
company_scores.columns = company_scores.columns.str.strip().str.lower()

# Print column names before merging
print("Job Data Columns:", job_data.columns.tolist())
print("Company Scores Columns:", company_scores.columns.tolist())


# Perform the merge
job_data_final = job_data.merge(company_scores, on="company_name", how="left")


# Debug: Check if 'legitimacy_score' exists after merging
print("Final Columns After Merge:", job_data_final.columns.tolist())

# Ensure legitimacy_score exists before applying fillna
if "legitimacy_score" in job_data_final.columns:
    job_data_final["legitimacy_score"] = job_data_final["legitimacy_score"].fillna(0)
else:
    print("❌ 'legitimacy_score' column is missing after merge!")

# If both columns exist, keep 'legitimacy_score_y' from company_scores
if "legitimacy_score_x" in job_data_final.columns and "legitimacy_score_y" in job_data_final.columns:
    job_data_final["legitimacy_score"] = job_data_final["legitimacy_score_y"].fillna(0)
    job_data_final.drop(["legitimacy_score_x", "legitimacy_score_y"], axis=1, inplace=True)

# Save the cleaned dataset
job_data_final.to_csv("job_dataset_final.csv", index=False)
print("✅ job_dataset_final.csv updated successfully with legitimacy_score!")
