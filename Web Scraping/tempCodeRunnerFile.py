# This is a project given by roadmap.sh

import requests
import csv
from bs4 import BeautifulSoup

URL = 'https://realpython.github.io/fake-jobs/'
response = requests.get(URL)

print(response.status_code)