import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import hstack, csr_matrix  # For sparse matrix operations

# ========== LOAD TRAINED COMPONENTS ==========
with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("tfidf_vectorizer.pkl", "rb") as file:
    tfidf_vectorizer = pickle.load(file)

with open("label_encoders.pkl", "rb") as file:
    label_encoders = pickle.load(file)

# ========== SCAM KEYWORDS LIST ==========
scam_keywords = [
    "no experience required", "work from home", "immediate hire", "quick hire", "instant approval",
    "hiring now", "entry level", "unlimited earnings", "weekly payout", "daily payout",
    "easy money", "earn money fast", "flexible hours", "guaranteed job", "limited positions available",
    "make money online", "start earning today", "100% free", "no upfront cost", "sign up bonus",
    "click here to apply", "apply instantly", "work anytime", "be your own boss",
    "send your details", "no resume needed", "earn up to", "get rich quick",
    "cash daily", "instant cash", "bitcoin payment", "no background check", "high paying with no experience",
    "earn $", "make $", "get paid instantly", "earn cash now", "money guaranteed",
    "refer and earn", "investment opportunity", "pyramid scheme", "multi-level marketing", 
    "residual income", "network marketing", "downline commission", "recruitment bonus",
    "minimal work", "too good to be true", "training provided", "no skills required", 
    "easy task", "work remotely with no experience", "earn commission only",
    "work under minimal supervision", "mystery shopper", "sign up now", "hurry limited spots"
]

# Function to count scam words
def count_scam_keywords(text):
    return sum(word in text.lower() for word in scam_keywords)

# ========== FEATURE CONFIGURATION ==========
text_features = ["title", "company_name", "description", "location"]
categorical_features = [
    "telecommuting", "has_company_logo", "has_questions",
    "employment_type", "required_experience", "required_education",
    "industry", "function", "paid", "job_type", "duration",
    "salary_range", "department", "legitimacy_score"
]

# Fraud detection threshold (lowered for better fraud capture)
THRESHOLD = 0.08  

def predict_fraud(job_data):
    """
    Predicts whether a job posting is fraudulent based on given job details.
    
    Args:
        job_data (dict): Job posting details.
    
    Returns:
        str: Prediction result with fraud probability.
    """
    df = pd.DataFrame([job_data])

    # ========== HANDLE TEXT FEATURES (TF-IDF) ==========
    for col in text_features:
        df[col] = df.get(col, "").astype(str)  # Ensure string format

    text_tfidf = tfidf_vectorizer.transform(df[text_features].agg(" ".join, axis=1))

    # ========== SCAM WORD COUNT FEATURE ==========
    df["scam_word_count"] = df["description"].apply(count_scam_keywords)
    scam_count_feature = csr_matrix(df["scam_word_count"].values.reshape(-1, 1))  # Convert to sparse matrix

    # ========== HANDLE CATEGORICAL FEATURES ==========
    for col in categorical_features:
        if col not in df:
            df[col] = "Unknown"  # Fill missing columns

    for col in categorical_features:
        if col in label_encoders:
            le = label_encoders[col]
            
            # Ensure "Unknown" exists in label encoder
            if "Unknown" not in le.classes_:
                le.classes_ = np.append(le.classes_, "Unknown")

            # Encode known values, map unknowns to "Unknown"
            df[col] = df[col].apply(lambda x: x if x in le.classes_ else "Unknown")
            df[col] = le.transform(df[col])

    # Convert categorical features to sparse matrix
    X_categorical = csr_matrix(df[categorical_features].values)

    # ========== MERGE FEATURES ==========
    X = hstack([X_categorical, text_tfidf, scam_count_feature], format="csr")

    # ========== PREDICT FRAUDULENCE ==========
    proba = model.predict_proba(X)[0][1]  # Fraud probability
    prediction = 1 if proba > THRESHOLD else 0

    return f"Fraudulent (⚠️ {proba:.2f})" if prediction == 1 else f"Legit (✅ {proba:.2f})"

# ========== TEST CASE ==========
sample_job = {
    "title": "Marketing Manager",
    "company_name": "Coca-Cola",
    "description": "We are looking for a skilled Marketing Manager to oversee campaigns and brand strategies at Coca-Cola. The ideal candidate has experience in digital marketing, branding, and team leadership.",
    "location": "Atlanta, GA",
    "telecommuting": 0,
    "has_company_logo": 1,
    "has_questions": 1,
    "employment_type": "Full-time",
    "required_experience": "Manager",
    "required_education": "Bachelor's Degree in Marketing",
    "industry": "Beverage",
    "function": "Marketing",
    "paid": 1,
    "job_type": "Permanent",
    "duration": "N/A",
    "salary_range": "$80,000-$100,000 per year",
    "department": "Marketing",
    "legitimacy_score": 1.0  
}






result = predict_fraud(sample_job)
print(f"Job Posting is: {result}")
