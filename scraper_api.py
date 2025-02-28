from flask import Flask, request, jsonify
from scraper import scrape_job_post  # Importing scraper function
import re

app = Flask(__name__)

def extract_job_id(profile_link):
    match = re.search(r'currentJobId=(\d+)', profile_link)
    if match:
        return match.group(1)  # Extracts the job ID
    return None

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json  # Get JSON input
    profile_link = data.get("profile_link")  # Get job post link
    
    if not profile_link:
        return jsonify({"error": "Profile link is required"}), 400
    
    job_id = extract_job_id(profile_link)
    if not job_id:
        return jsonify({"error": "Invalid LinkedIn job link format"}), 400
    
    # Call scraper function
    job_data = scrape_job_post(profile_link)
    
    if job_data:
        return jsonify(job_data)  # Return scraped job details
    else:
        return jsonify({"error": "Failed to fetch job details"}), 500

if __name__ == '__main__':
    app.run(debug=True)
