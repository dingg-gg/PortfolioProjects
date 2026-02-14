# Web Scraper - roadmap.sh project

This project is a Python-based webscraper on[roadmap.sh/projects/job-listings-scraper](https://roadmap.sh/projects/job-listings-scraper).


## Project Overview
The goal of this project is to practice and learn:
1. **Fetching** HTML content from a live URL.  
2. **Parsing** data using BeautifulSoup.  
3. **Traversing** the HTML dom using tags and classes. 
4. **Storing** structured data into CSV file. 


## Thought Process

Before writing the code, I inspected the website to find the website's structure, noticing that every job listing is inside a `<div>` with the class `card-content`.
I made use of this information to loop through the cards one by one.

I used the `requests` library to fetch the page and checked for response. From there, I proceeded to target specific elements inside each card.
I noticed that job titles were in `<h2>` tags , company names in `<h3>` tags and use the `class_` parameter in BeautifulSoup to ensure I was grabbing the correct data and not other random headers on the page.
There are two links inside each card, I need to specifically target the second link in each card.

From there, I used `.strip()` to remove unnecessary newlines and whitespace, ensuring the data is readable.
