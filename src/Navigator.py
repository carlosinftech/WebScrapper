import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

class Navigator:

    def get_html_from_url(self,url):
        #options = Options()
        #options.add_argument("--headless")
        browser = webdriver.Firefox()

        listings = browser.get(url)
        return browser.page_source

    def obtain_last_page_node(self,page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        for item in soup.findAll('a', attrs={'class': 'pagination__button pagination__page'}):
            print(item.text)


