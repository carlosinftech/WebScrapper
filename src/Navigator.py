import time

import requests
from src.Executor import Executor
from configuration.config import username, password, url_login, action_login, get_place_ids_urls, place_ids_csv, \
    enrich_url, listings_request_header,STATUS_OK
from bs4 import BeautifulSoup
import json
from html import unescape


class Navigator:
    """Handles the interaction with the website """

    def create_session(self):
        """Opens a session perform login into the website and delivers the html content to the executor"""
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

            for place_id, place_id_url in get_place_ids_urls(place_ids_csv).items():
                page_number = 1
                previous_status_code = STATUS_OK
                while previous_status_code == STATUS_OK:
                    listinq_request = enrich_url(place_id_url, {"page": page_number})
                    page_number += 1
                    response = session.get(listinq_request, headers=listings_request_header)
                    previous_status_code = response.status_code

                    if previous_status_code == STATUS_OK:
                        print(previous_status_code)
                        html_content = json.loads(response.text)
                        html_content = html_content["html"]
                        html_content = html_content.replace(u'\u202F', '')
                        html_content = unescape(html_content)
                        executor.run_scraper(place_id, page_number, html_content)

            session.cookies.clear()






