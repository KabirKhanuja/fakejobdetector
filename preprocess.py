import pandas as pd

job_data = pd.read_csv("job_dataset_final.csv")
company_scores = pd.read_csv("company_legitimacy_scores.csv")

job_data.columns = job_data.columns.str.strip().str.lower()
company_scores.columns = company_scores.columns.str.strip().str.lower()

print("Job Data Columns:", job_data.columns.tolist())
print("Company Scores Columns:", company_scores.columns.tolist())


job_data_final = job_data.merge(company_scores, on="company_name", how="left")


print("Final Columns After Merge:", job_data_final.columns.tolist())

if "legitimacy_score" in job_data_final.columns:
    job_data_final["legitimacy_score"] = job_data_final["legitimacy_score"].fillna(0)
else:
    print("❌ 'legitimacy_score' column is missing after merge!")

if "legitimacy_score_x" in job_data_final.columns and "legitimacy_score_y" in job_data_final.columns:
    job_data_final["legitimacy_score"] = job_data_final["legitimacy_score_y"].fillna(0)
    job_data_final.drop(["legitimacy_score_x", "legitimacy_score_y"], axis=1, inplace=True)

job_data_final.to_csv("job_dataset_final.csv", index=False)
print("✅ job_dataset_final.csv updated successfully with legitimacy_score!")
