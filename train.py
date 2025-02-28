import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE  
from scipy.sparse import hstack, csr_matrix  
from sklearn.feature_extraction.text import TfidfVectorizer

# 🚨 Scam-related keywords
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

# ========== LOAD DATA ==========
df = pd.read_csv("job_dataset_final_processed.csv")

# Ensure no missing values in 'fraudulent' column
df["fraudulent"] = df["fraudulent"].fillna(0).astype(int)
df.dropna(inplace=True)  # Drop any remaining NaN rows

# Check class distribution before SMOTE
print("📊 Class distribution before SMOTE:", df["fraudulent"].value_counts())

# ========== TEXT FEATURE PROCESSING (TF-IDF) ==========
text_features = ["title", "company_name", "description", "location"]
df[text_features] = df[text_features].fillna(" ")  # Replace NaN with empty string

# Train TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=7000)
text_tfidf = tfidf_vectorizer.fit_transform(df[text_features].agg(" ".join, axis=1)) 

# Save the vectorizer
with open("tfidf_vectorizer.pkl", "wb") as file:
    pickle.dump(tfidf_vectorizer, file)
print("✅ TF-IDF vectorizer saved!")

# ========== SCAM KEYWORD COUNT FEATURE ==========
def count_scam_keywords(text):
    return sum(word in text.lower() for word in scam_keywords)

df["scam_word_count"] = df["description"].apply(count_scam_keywords)

# ========== CATEGORICAL FEATURE ENCODING ==========
categorical_features = [
    "telecommuting", "has_company_logo", "has_questions", "employment_type",
    "required_experience", "required_education", "industry", "function",
    "paid", "job_type", "duration", "salary_range", "department", "legitimacy_score"
]

label_encoders = {}
for col in categorical_features:
    df[col] = df[col].astype(str)  # Convert to string before encoding
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoder for later use

# Convert categorical data to sparse matrix
X_categorical = csr_matrix(df[categorical_features].values)

# ========== MERGE FEATURES ==========
scam_count_feature = csr_matrix(df["scam_word_count"].values.reshape(-1, 1))  # Convert to sparse matrix
X = hstack([X_categorical, text_tfidf, df["scam_word_count"].values.reshape(-1, 1)])

# Ensure target variable is an integer
y = df["fraudulent"]

# ✅ Split **before** SMOTE
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Apply SMOTE **only on the training set**
smote = SMOTE(sampling_strategy=0.7, random_state=42)  # Increase from 0.5 to 0.7
X_train_resampled, y_train_resampled = smote.fit_resample(X_train.toarray(), y_train)

# Convert back to sparse matrix after SMOTE
X_train_resampled = csr_matrix(X_train_resampled)

# Check class distribution after SMOTE
unique, counts = np.unique(y_train_resampled, return_counts=True)
print("📊 Class distribution after SMOTE:", dict(zip(unique, counts)))

# ========== TRAIN RANDOM FOREST MODEL ==========
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
model.fit(X_train_resampled, y_train_resampled)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.4f}")

# Print classification report
print("\n🔍 Classification Report:")
print(classification_report(y_test, y_pred))

# Display feature importance (Including scam word count)
importances = model.feature_importances_[: len(categorical_features)]  # Categorical features first
print("\n📊 Feature Importances (Categorical Only):")
for feature, importance in zip(categorical_features, importances):
    print(f"{feature}: {importance:.4f}")

# Add scam word count importance
scam_importance = model.feature_importances_[len(categorical_features)]  # Scam word count feature
print(f"scam_word_count: {scam_importance:.4f}")

# ========== SAVE MODEL & ENCODERS ==========
with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("label_encoders.pkl", "wb") as file:
    pickle.dump(label_encoders, file)

print("✅ Model trained and saved as random_forest_model.pkl")
print("✅ Label encoders saved as label_encoders.pkl")
