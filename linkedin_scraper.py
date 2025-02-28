import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_linkedin_job(job_url):
    # Configure Selenium (Headless Mode)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(job_url)
    
    time.sleep(3)  # Allow page to load

    try:
        # Extract Job Title
        title = driver.find_element(By.CLASS_NAME, "top-card-layout__title").text

        # Extract Company Name
        company = driver.find_element(By.CLASS_NAME, "topcard__org-name-link").text

        # Extract Job Location
        location = driver.find_element(By.CLASS_NAME, "topcard__flavor--bullet").text

        # Extract Job Description
        description = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup").text

        # Extract Employment Type (Full-time, Internship, etc.)
        employment_type = driver.find_element(By.XPATH, "//li[contains(@class, 'description__job-criteria-item')][1]").text

        # Extract Job Function
        job_function = driver.find_element(By.XPATH, "//li[contains(@class, 'description__job-criteria-item')][2]").text

        # Extract Industry (if available)
        try:
            industry = driver.find_element(By.XPATH, "//li[contains(@class, 'description__job-criteria-item')][3]").text
        except:
            industry = "Not Specified"

        # Store extracted data in dictionary
        job_details = {
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "employment_type": employment_type,
            "job_function": job_function,
            "industry": industry
        }

    except Exception as e:
        print(f"Error: {e}")
        job_details = None

    driver.quit()
    return job_details

# Example Usage:
if __name__ == "__main__":
    job_url = "https://www.linkedin.com/jobs/view/XXXXX"  # Replace with actual LinkedIn job link
    data = scrape_linkedin_job(job_url)
    print(data)
