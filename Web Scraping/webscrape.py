# This is a project given by roadmap.sh

import requests
import csv
from bs4 import BeautifulSoup

URL = 'https://realpython.github.io/fake-jobs/'
response = requests.get(URL)

print(response.status_code) # If we get 200, it is good to go

soup = BeautifulSoup(response.content, "html.parser") #fetching the html and putting it in soup variable

job_titles = soup.find_all("h2", class_="title") #find all h2 tags with the class 'title'

for title in job_titles:
    print(title.text.strip()) #text gets the word inside the text and strip removes extra spaces
    
job_elements = soup.find_all("div", class_ = "card-content")

jobs_list = []

for job_element in job_elements:
    title = job_element.find("h2", class_ = "title").text.strip()
    company = job_element.find("h3", class_ = "company").text.strip()
    location = job_element.find("p", class_="location").text.strip()
    link_url = job_element.find_all("a")[1]["href"]
    
    jobs_list.append({
        "Job Title" : title,
        "Company" : company,
        "Location": location,
        "URL": link_url
    })

filename = 'scrape.csv'
keys = ["Job Title", "Company", "Location", "URL"]

with open(filename, "w", newline="", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(jobs_list)