from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_fraud  # Import fraud prediction function

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get JSON data from frontend

    # Ensure job description is provided
    job_description = data.get("description", "").strip()
    company_name = data.get("company_name", "").strip()  # Get company name

    if not job_description:
        return jsonify({"error": "Job description is required"}), 400

    # Construct job dictionary
    job_data = {
        "title": "Unknown",
        "company_name": company_name if company_name else "Unknown",
        "description": job_description,
        "location": "Unknown",
        "telecommuting": 0,
        "has_company_logo": 0,
        "has_questions": 0,
        "employment_type": "Unknown",
        "required_experience": "Unknown",
        "required_education": "Unknown",
        "industry": "Unknown",
        "function": "Unknown",
        "paid": 0,
        "job_type": "Unknown",
        "duration": "Unknown",
        "salary_range": "Unknown",
        "department": "Unknown",
        "legitimacy_score": 0.5  # Neutral score if unknown
    }

    # Call prediction function
    prediction_result = predict_fraud(job_data)

    return jsonify({"prediction": prediction_result})

if __name__ == '__main__':
    app.run(debug=True)
