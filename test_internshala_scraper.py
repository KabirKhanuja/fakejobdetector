

import requests

SCRAPINGDOG_API_KEY = "67c08725951dde454419cf31"
JOB_ID = "4160836596"

# ScrapingDog LinkedIn Job API endpoint
api_url = f"https://api.scrapingdog.com/linkedinjobs?api_key={SCRAPINGDOG_API_KEY}&job_id={JOB_ID}"

response = requests.get(api_url)
print(response.status_code)
print(response.text)  # Check the response
