import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re

# API Keys
SERPAPI_KEY = "YOUR_API_KEY"
SCRAPINGDOG_API_KEY = "YOUR_API_KEY"

# Set up Selenium for Brave Browser
options = Options()
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

chromedriver_path = "/usr/local/bin/chromedriver"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

def scrape_internshala_selenium(url):
    """Scrape Internshala job details using Selenium."""
    driver.get(url)
    time.sleep(5)

    try:
        job_title = driver.find_element(By.CLASS_NAME, "heading_4_5.profile").text.strip()
    except:
        job_title = "Unknown"

    try:
        company_name = driver.find_element(By.CLASS_NAME, "heading_6.company_name").text.strip()
    except:
        company_name = "Unknown"

    try:
        job_description = driver.find_element(By.CLASS_NAME, "internship_details").text.strip()
    except:
        job_description = "No description available"

    try:
        duration = driver.find_elements(By.CLASS_NAME, "item_body")[1].text.strip()
    except:
        duration = "Not specified"

    try:
        stipend = driver.find_element(By.CLASS_NAME, "stipend").text.strip()
    except:
        stipend = "Unpaid / Not specified"

    try:
        location = driver.find_element(By.ID, "location_names").text.strip()
    except:
        location = "Not specified"

    return {
        "source": "internshala",
        "job_title": job_title,
        "company_name": company_name,
        "description": job_description,
        "duration": duration,
        "stipend": stipend,
        "location": location
    }

def extract_job_id(linkedin_url):
    """Extract Job ID from a LinkedIn job posting URL."""
    match = re.search(r'/jobs/view/(\d+)', linkedin_url)
    return match.group(1) if match else None

def scrape_linkedin_job(linkedin_url):
    """Scrape LinkedIn job details using ScrapingDog API."""
    job_id = extract_job_id(linkedin_url)
    if not job_id:
        print(f"⚠️ Invalid LinkedIn job URL: {linkedin_url}")
        return None

    api_url = f"https://api.scrapingdog.com/linkedinjobs?api_key={SCRAPINGDOG_API_KEY}&job_id={job_id}"
    response = requests.get(api_url)

    print(f"🔍 Fetching LinkedIn job: {linkedin_url}")
    print(f"🔍 Response Status Code: {response.status_code}")
    print(f"🔍 Response Data: {response.text}")
    print(f"Extracted Job ID: {job_id}")

    if response.status_code != 200:
        print(f"❌ Failed to fetch LinkedIn job details: {linkedin_url}")
        return None

    try:
        job_data = response.json()
    except Exception as e:
        print(f"❌ JSON Decoding Error: {e}")
        return None

    if isinstance(job_data, list) and len(job_data) > 0:
        job_data = job_data[0]
    elif isinstance(job_data, dict):
        pass
    else:
        print("❌ Unexpected response format from ScrapingDog API:", job_data)
        return None

    return {
        "source": "linkedin",
        "job_position": job_data.get("job_position", "Unknown"),
        "company_name": job_data.get("company_name", "Unknown"),
        "job_description": job_data.get("job_description", "No description available"),
        "job_location": job_data.get("job_location", "Not specified")
    }

def search_linkedin(company_name=None):
    """Check company legitimacy via SerpAPI with user input."""
    if not company_name:
        company_name = input("🔍 Enter the company name to search on LinkedIn: ").strip()

    query = f'LinkedIn "{company_name}" site:linkedin.com/company'
    search_url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={SERPAPI_KEY}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    print(f"🔍 Searching for: {company_name} on LinkedIn...")

    if response.status_code != 200:
        return 0.0  

    data = response.json()
    results = data.get("organic_results", [])

    for result in results:
        link = result.get("link", "")
        title = result.get("title", "").lower()

        extracted_company_name = title.replace("linkedin - ", "").strip()
        similarity_score = SequenceMatcher(None, company_name.lower(), extracted_company_name).ratio() * 100

        if "linkedin.com/company" in link and similarity_score > 80:
            print(f"✅ Found: {link} (Similarity: {similarity_score:.2f}%)")
            return 1.0  

    print(f"❌ No exact match for: {company_name}")
    return 0.3  

def process_job_details(job_details):
    """Process job details and store them in job_data."""
    if not job_details:
        return

    source = job_details.get("source", "unknown")

    if source == "linkedin":
        job_title = job_details.get("job_position", "Unknown")
        company_name = job_details.get("company_name", "Unknown")
        job_description = job_details.get("job_description", "No description available")
        job_location = job_details.get("job_location", "Not specified")
        duration = "Not specified"
        stipend = "Not specified"

    elif source == "internshala":
        job_title = job_details.get("job_title", "Unknown")
        company_name = job_details.get("company_name", "Unknown")
        job_description = job_details.get("description", "No description available")
        job_location = job_details.get("location", "Not specified")
        duration = job_details.get("duration", "Not specified")
        stipend = job_details.get("stipend", "Not specified")

    else:
        print("❌ Unknown source, skipping...")
        return

    job_data["job_title"].append(job_title)
    job_data["company_name"].append(company_name)
    job_data["description"].append(job_description)
    job_data["duration"].append(duration)
    job_data["stipend"].append(stipend)
    job_data["location"].append(job_location)

    legitimacy_score = search_linkedin(company_name)
    job_data["legitimacy_score"].append(legitimacy_score)

    print(f"✅ Processed: {job_title} ({company_name}) - Score: {legitimacy_score}")
    time.sleep(2)

job_urls = [
    "https://internshala.com/internship/detail/work-from-home-virtual-assistance-internship-at-infinity-magazine1740660373",
    "https://www.linkedin.com/jobs/view/4160836596/"
]

job_data = {"job_title": [], "company_name": [], "description": [], "duration": [], "stipend": [], "location": [], "legitimacy_score": []}

for url in job_urls:
    job_details = scrape_internshala_selenium(url) if "internshala.com" in url else scrape_linkedin_job(url)
    if job_details:
        process_job_details(job_details)

driver.quit()

df = pd.DataFrame(job_data)
df.to_csv("job_scrape_results.csv", index=False)
print("✅ job_scrape_results.csv has been created!")
