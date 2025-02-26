import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE  # Handle class imbalance

# Load dataset
df = pd.read_csv("job_dataset_final.csv")

# Drop rows with missing values (optional)
df.dropna(inplace=True)

# Select relevant features
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
target = "fraudulent"

# Encode categorical variables
label_encoders = {}
for col in features:
    if df[col].dtype == "object":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le  # Store encoder for future use

# Prepare dataset
X = df[features]
y = df[target]

# Handle imbalanced data using SMOTE
smote = SMOTE(sampling_strategy=0.5, random_state=42)  # Balances classes
X, y = smote.fit_resample(X, y)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model with tuning
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.4f}")

# Print classification report for fraud detection
print("\n🔍 Classification Report:")
print(classification_report(y_test, y_pred))

# Feature Importance Check
importances = model.feature_importances_
print("\n📊 Feature Importances:")
for feature, importance in zip(features, importances):
    print(f"{feature}: {importance:.4f}")

# Save the trained model
with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Model trained and saved as random_forest_model.pkl")
