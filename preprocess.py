import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

job_data = pd.read_csv("job_dataset_final.csv")
company_scores = pd.read_csv("company_legitimacy_scores.csv")
scraped_jobs = pd.read_csv("job_scrape_results.csv")

job_data.columns = job_data.columns.str.strip().str.lower()
company_scores.columns = company_scores.columns.str.strip().str.lower()
scraped_jobs.columns = scraped_jobs.columns.str.strip().str.lower()

print("Job Data Columns:", job_data.columns.tolist())
print("Company Scores Columns:", company_scores.columns.tolist())
print("Scraped Jobs Columns:", scraped_jobs.columns.tolist())

column_mapping = {
    "job_title": "title",
    "job_position": "title", 
    "company_name": "company_name",
    "description": "description",
    "job_description": "description",  
    "location": "location",
    "job_location": "location", 
    "duration": "duration",
    "stipend": "salary_range"  
}

scraped_jobs.rename(columns=column_mapping, inplace=True)

scraped_jobs = scraped_jobs[job_data.columns.intersection(scraped_jobs.columns)]

job_data_final = pd.concat([job_data, scraped_jobs], ignore_index=True)

job_data_final = job_data_final.merge(company_scores, on="company_name", how="left")

if "legitimacy_score_x" in job_data_final.columns and "legitimacy_score_y" in job_data_final.columns:
    job_data_final["legitimacy_score"] = job_data_final["legitimacy_score_y"].fillna(0)
    job_data_final.drop(["legitimacy_score_x", "legitimacy_score_y"], axis=1, inplace=True)
elif "legitimacy_score" in job_data_final.columns:
    job_data_final["legitimacy_score"] = job_data_final["legitimacy_score"].fillna(0)
else:
    print("❌ 'legitimacy_score' column is missing after merge!")

job_data_final.to_csv("job_dataset_final_updated.csv", index=False)
print("✅ job_dataset_final_updated.csv saved!")


categorical_features = [
    "telecommuting", "has_company_logo", "has_questions",
    "employment_type", "required_experience", "required_education",
    "industry", "function", "paid", "job_type", "duration",
    "salary_range", "department", "legitimacy_score"
]

label_encoders = {}

for col in categorical_features:
    job_data_final[col] = job_data_final[col].astype(str)  

    le = LabelEncoder()
    job_data_final[col] = le.fit_transform(job_data_final[col]) 

    label_encoders[col] = le  

job_data_final.to_csv("job_dataset_final_processed.csv", index=False)
print("✅ job_dataset_final_processed.csv saved!")

with open("label_encoders.pkl", "wb") as file:
    pickle.dump(label_encoders, file)

print("✅ Label encoders saved in label_encoders.pkl")
print("🎯 Preprocessing complete! Encoded dataset and label encoders are ready.")
