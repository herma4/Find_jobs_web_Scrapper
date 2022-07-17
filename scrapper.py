import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

limit = 50

def extract_indeed_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    searchCountPages = soup.find("div", id="searchCountPages").text
    searchCountPages = searchCountPages.split("결과")[-1]
    searchCountPages = re.sub("[^0-9]", "", searchCountPages)
    searchCountPages = int(searchCountPages)
    max_indeed_page =  searchCountPages // limit
    print("max_indeed_page", max_indeed_page)
    if max_indeed_page>10:
        max_indeed_page = 10
    else:
        max_indeed_page = max_indeed_page
    return max_indeed_page

def extract_indeed_jobs(url, last_page):
    jobs = []
    for page in tqdm(range(last_page)):
        result = requests.get(url + "&start=" + str(page*limit))
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", class_="job_seen_beacon")
        for result in results:
            title = result.find("h2").text
            companyName = result.find("span", class_="companyName").text
            companyLocation = result.find("div", class_="companyLocation").text
            jobUrl = "https://indeed.com" + result.find("a")["href"]
            jobs.append({
                "title": title, 
                "companyName": companyName, 
                "companyLocation": companyLocation, 
                "link": jobUrl})
    return jobs

def get_jobs(word):
    INDEED_URL = "https://indeed.com/jobs?q=" + str(word) + "&limit=" + str(limit)
    last_page = extract_indeed_page(INDEED_URL)
    jobs = extract_indeed_jobs(INDEED_URL, last_page)
    return jobs