import time

import requests
from src.Executor import Executor
from configuration.config import username, password, url_login, action_login, get_place_ids_urls, place_ids_csv, \
    enrich_url
from bs4 import BeautifulSoup
import json
from html import unescape


class Navigator:

    def create_session(self):
        executor = Executor()
        with requests.session() as session:
            session.cookies.clear()
            response = session.get(url_login)
            soup = BeautifulSoup(response.text, 'lxml')
            token = soup.find('input', id='user_csrf_token').get('value')
            data = {
                'action': action_login,
                'user_username': username,
                'user_password': password,
                'user_csfr_token': token,
            }

            response_post = session.post(url_login, data=data)

            listing_request_header = {
                'sec-ch-ua': '\'Not A;Brand\';v=\'99\': \'Chromium\';v=\'96\': \'Microsoft Edge\';v=\'96\'',
                'Accept': 'application/json',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '\'Windows\'',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Accept-Encoding': 'gzip: deflate: br',
                'Accept-Language': 'en-US:en;q=0.9:es;q=0.8',
                'Connection': 'keep-alive',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML: like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43'
            }

            for place_id, place_id_url in get_place_ids_urls(place_ids_csv).items():
                page_number = 1
                previous_status_code = 200
                while (previous_status_code == 200):
                    time.sleep(5)
                    listinq_request = enrich_url(place_id_url, {"page": page_number})
                    page_number += 1
                    response = session.get(listinq_request, headers=listing_request_header)
                    previous_status_code = response.status_code

                    if previous_status_code == 200:
                        print(previous_status_code)
                        html_content = json.loads(response.text)
                        html_content = html_content["html"]
                        html_content = html_content.replace(u'\u202F', '')
                        html_content = unescape(html_content)
                        executor.run_scraper(place_id, page_number, html_content)

            session.cookies.clear()






