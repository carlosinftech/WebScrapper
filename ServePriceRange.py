import requests
from configuration import config
from configuration.config import flask_url,flask_request_header,sql_price_range
from src.Reader import DBReader
import pandas as pd

def serve_price_range():
    #response = requests.get(flask_url, headers=flask_request_header)
    #print(response.text)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    pandas_db_reader = DBReader()
    price_range_df = pandas_db_reader.read(sql_price_range, config.get_pandas_dbconn())
    print(price_range_df)

if __name__ == '__main__':
    serve_price_range()
