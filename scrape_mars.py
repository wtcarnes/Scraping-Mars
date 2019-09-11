import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def nasa_scrape():

    browser = init_browser()

    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    nasa_title = soup.find("div",class_="content_title").text
    nasa_p = soup.find("div", class_="article_teaser_body").text

    print(nasa_title)
    print(nasa_p)
    
    return nasa_scrape   
    
 

