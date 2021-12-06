import requests
from requests_html import HTMLSession
import woob

class Extractor:

    def consume_page(self,url):
        return requests.get(url).text


