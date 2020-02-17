#imports
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit Yelp site
    url = ""
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #-------------------------------------------
    # Insert Scraping Code that parses yelp for the relevant data
    #-------------------------------------------

    # Close the browser after scraping
    browser.quit()

    # Return results
    return yelp_data