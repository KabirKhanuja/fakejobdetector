import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# 🚨 Scam-related keywords for better fraud detection
scam_keywords = [
    # Fake job phrases
    "no experience required", "work from home", "immediate hire", "quick hire", "instant approval",
    "hiring now", "entry level", "unlimited earnings", "weekly payout", "daily payout",
    "easy money", "earn money fast", "flexible hours", "guaranteed job", "limited positions available",

    # Clickbait & suspicious terms
    "make money online", "start earning today", "100% free", "no upfront cost", "sign up bonus",
    "click here to apply", "apply instantly", "work anytime", "be your own boss",
    "send your details", "no resume needed", "earn up to", "get rich quick",
    
    # Payment & salary scams
    "cash daily", "instant cash", "bitcoin payment", "no background check", "high paying with no experience",
    "earn $", "make $", "get paid instantly", "earn cash now", "money guaranteed",
    
    # Pyramid schemes & MLM scams
    "refer and earn", "investment opportunity", "pyramid scheme", "multi-level marketing", 
    "residual income", "network marketing", "downline commission", "recruitment bonus",
    
    # Job description red flags
    "minimal work", "too good to be true", "training provided", "no skills required", 
    "easy task", "work remotely with no experience", "earn commission only",
    
    # Contract & hidden details
    "work under minimal supervision", "mystery shopper", "sign up now", "hurry limited spots"
]

# Load dataset
df = pd.read_csv("job_dataset_final.csv")

# Select text fields
text_features = ["title", "company_name", "description", "location"]
df[text_features] = df[text_features].fillna(" ")  # Fill NaN with empty string

# Combine text fields into a single column
text_data = df[text_features].agg(" ".join, axis=1)

# Initialize TF-IDF Vectorizer with scam words added to vocabulary
tfidf_vectorizer = TfidfVectorizer(max_features=5000, vocabulary=scam_keywords)

# Fit the vectorizer
tfidf_vectorizer.fit(text_data)

# Save the trained vectorizer
with open("tfidf_vectorizer.pkl", "wb") as file:
    pickle.dump(tfidf_vectorizer, file)

print("✅ TF-IDF Vectorizer updated with scam keywords!")
