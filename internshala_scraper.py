import requests
from bs4 import BeautifulSoup

def scrape_internshala_job(job_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(job_url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch the page")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Extract Job Title
        title = soup.find("h1", class_="profile").text.strip()

        # Extract Company Name
        company = soup.find("div", class_="company_name").text.strip()

        # Extract Location
        location = soup.find("span", class_="location_link").text.strip()

        # Extract Job Description
        description = soup.find("div", class_="internship_details").text.strip()

        # Extract Employment Type (Internship, Full-time, etc.)
        employment_type = soup.find("div", class_="other_detail_item").text.strip()

        # Extract Job Duration
        duration = soup.find("div", class_="item_body").text.strip()

        # Store extracted data in dictionary
        job_details = {
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "employment_type": employment_type,
            "duration": duration
        }

    except Exception as e:
        print(f"Error: {e}")
        job_details = None

    return job_details

# Example Usage:
if __name__ == "__main__":
    job_url = "https://internshala.com/internship/detail/XXXXX"  # Replace with actual Internshala job link
    data = scrape_internshala_job(job_url)
    print(data)
