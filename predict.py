import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# Load trained model
with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)

# Define the same features used during training
features = [
    "telecommuting",
    "has_company_logo",
    "has_questions",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function",
    "paid",
    "job_type",
    "duration",
    "legitimacy_score"
]

# Set fraud detection threshold
THRESHOLD = 0.3  # Lowering from 0.5 to 0.3 for better fraud detection

# Function to predict if a job posting is fraudulent
def predict_fraud(job_data):
    df = pd.DataFrame([job_data])

    # Encode categorical values (ensure it matches training encoding)
    for col in features:
        if df[col].dtype == "object":
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    # Ensure all features are present
    df = df[features]

    # Get fraud probability
    proba = model.predict_proba(df)[0][1]  # Probability of fraud

    # Apply threshold
    prediction = 1 if proba > THRESHOLD else 0

    return f"Fraudulent (⚠️ {proba:.2f})" if prediction == 1 else f"Legit (✅ {proba:.2f})"

sample_job = {
    "telecommuting": 0,
    "has_company_logo": 1,
    "has_questions": 0,
    "employment_type": "Full-time",
    "required_experience": "Mid-Senior level",
    "required_education": "Bachelor's Degree",
    "industry": "IT",
    "function": "Engineering",
    "paid": 0,
    "job_type": "Contract",
    "duration": "3 months",
    "legitimacy_score": 0.0
}

# Run prediction
result = predict_fraud(sample_job)
print(f"Job Posting is: {result}")
