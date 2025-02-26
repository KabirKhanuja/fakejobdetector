import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def search_linkedin(company_name):
    query = f'LinkedIn "{company_name}" site:linkedin.com/company'
    search_url = f"https://www.google.com/search?q={query}"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return 0.0  # No result found → suspicious company

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("a")
    
    for result in results:
        link = result.get("href")
        if "linkedin.com/company" in link:
            return 1.0  # Company exists → more legit

    return 0.3  # Partial confidence → company might exist

# List of company names to check
company_names = ["Google", "XYZ Fake Ltd", "Amazon", "ABC Pvt Ltd"]

# Store results in a dictionary
company_scores = {"company_name": [], "legitimacy_score": []}

for company in company_names:
    formatted_company = company.lower().replace(" ", "_")  # Normalize company name
    score = search_linkedin(company)
    
    company_scores["company_name"].append(formatted_company)  # Store formatted name
    company_scores["legitimacy_score"].append(score)
    
    print(f"Checked: {company} → Score: {score}")
    time.sleep(2)  # To avoid being blocked by Google

# Convert dictionary to DataFrame
df = pd.DataFrame(company_scores)

# Save results to CSV
df.to_csv("company_legitimacy_scores.csv", index=False)
print("✅ company_legitimacy_scores.csv has been created!")
