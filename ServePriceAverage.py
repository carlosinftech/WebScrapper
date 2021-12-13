import requests
from configuration import config
from configuration.config import flask_url,flask_request_header,sql_price_average
from src.Reader import DBReader

def serve_price_average():
    #response = requests.get(flask_url, headers=flask_request_header)
    #print(response.text)
    pandas_db_reader = DBReader()
    price_average_df = pandas_db_reader.read(sql_price_average, config.get_pandas_dbconn())
    print(price_average_df)

if __name__ == '__main__':
    serve_price_average()
