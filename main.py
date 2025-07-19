from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import get_key
from time import sleep
import pandas
import sys


USERNAME = get_key(".env", key_to_get="username")
PASSWORD = get_key(".env", key_to_get="password")

# Get ROLE and LOCATION from command-line arguments, or use defaults
if len(sys.argv) > 2:
    ROLE = sys.argv[1]
    LOCATION = sys.argv[2]
else:
    ROLE = "React Developer"
    LOCATION = "Pune"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.linkedin.com/jobs/")

username = driver.find_element(By.NAME, "session_key")
username.send_keys(USERNAME)

password = driver.find_element(By.NAME, "session_password")
password.send_keys(PASSWORD)

submit_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
submit_button.click()

sleep(8)
driver.maximize_window()
sleep(2)

search_field = driver.find_element(By.TAG_NAME, 'input')
search_field.clear()
search_field.send_keys(f"{ROLE} in {LOCATION}", Keys.ENTER)

# location_field = driver.find_elements(By.TAG_NAME, 'input')
# location_field[3].clear()
# location_field[3].send_keys(LOCATION, Keys.ENTER)
sleep(4)

job_page = driver.page_source
soup = BeautifulSoup(job_page, "html.parser")

jobs_title_tag = soup.select(selector="a div div div div div strong")
jobs_company_tag = soup.find_all(name="div", class_="artdeco-entity-lockup__subtitle ember-view")
jobs_location_tag = soup.find_all(name="div", class_="artdeco-entity-lockup__caption ember-view")


job_titles = [title.text.strip() for title in jobs_title_tag]
companies = [company.text.strip() for company in jobs_company_tag]
job_locations = [location.text.strip() for location in jobs_location_tag]
job_list = []

print(f"{len(job_titles)} "
      f"{len(job_locations)} "
      f"{len(companies)}")

if len(job_titles) == len(companies) == len(job_locations) != 0:
    for i in range(len(job_titles)):
        job_list.append({
            "Role": f"{job_titles[i]}",
            "Company": f"{companies[i]}",
            "Location": f"{job_locations[i]}"
        })

    new_jobs_df = pandas.DataFrame(job_list)
    print(new_jobs_df)

    try:
        existing_jobs_df = pandas.read_csv("./jobs.csv")
        # Ensure columns are consistent, especially if the CSV was empty or had different columns initially
        existing_jobs_df = existing_jobs_df[['Role', 'Company', 'Location']]
    except FileNotFoundError:
        existing_jobs_df = pandas.DataFrame(columns=['Role', 'Company', 'Location'])

    # Combine existing and new jobs
    combined_jobs_df = pandas.concat([existing_jobs_df, new_jobs_df], ignore_index=True)

    # Remove duplicates based on 'Role', 'Company', 'Location'
    deduplicated_jobs_df = combined_jobs_df.drop_duplicates(subset=['Role', 'Company', 'Location'], keep='first')

    # Save to CSV without index
    deduplicated_jobs_df.to_csv("./jobs.csv", index=False, encoding="utf-8")
    print("Updated jobs.csv with new and deduplicated entries.")

else:
    print("Could not find jobs!")

driver.quit()
