import pandas
from  urllib.parse import urlparse, parse_qsl, urlencode,urlunparse,quote
from sqlalchemy import create_engine

#site_web
username = 'lapepa@gmail.com'
password = 'Pollito123$'
url_login = 'https://www.meilleursagents.com/_signin?show=signin'
action_login = 'signin'
place_ids_csv = 'configuration/place_ids.csv'
base_url_listings = 'https://www.meilleursagents.com/annonces/achat/search/?item_types=ITEM_TYPE.APARTMENT'
STATUS_OK = 200

listings_request_header = {
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

#xpath
area_query = "//div[@class='listing-characteristic margin-bottom']"
price_query = "//div[@class='listing-price margin-bottom']"
all_listing_ids_query = "//div[@class='listing-item search-listing-result__item']//@data-wa-data"

#database

DBPARAMS = {
    'database': 'meilleursagents',
    'user': 'meilleursagents',
    'password': 'pikachu42!@',
    'host': 'localhost',
    'port': 5432
}
dbconn = None
listings_table_name = 'listings'
price_average_table= 'price_average'
price_range_table= 'price_range'
postal_code_place_id_table = "postal_code_place_id"
CITY_CODES_DF = pandas.read_csv(place_ids_csv)
sql_count_query = 'select count(*) from listings'
sql_price_average = """ select postal_code, price_average from(
select place_id ,cast(round(avg(price)/100) AS INTEGER) as price_average  from listings GROUP BY place_id) as a
INNER JOIN postal_code_place_id as b USING(place_id)"""
sql_price_range = """
        SELECT postal_code, listing_id, cast(round(price/100000) AS INTEGER) as price FROM listings INNER JOIN postal_code_place_id  USING(place_id)
"""

create_commands = [
        """
        DROP VIEW v_listings;
        """,
        """
        DROP TABLE IF EXISTS listings;
        """,
        """
        CREATE TABLE listings (
            listing_id INTEGER,
            place_id INTEGER NOT NULL,
            price INTEGER,
            area SMALLINT,
            room_count SMALLINT,
            register_date DATE NOT NULL
        );
        """,
        """
        CREATE OR REPLACE VIEW v_listings AS   (
                SELECT
                place_id,
                listing_id,
                min(register_date) AS first_seen,
                max(register_date) AS last_seen,
                array_agg(price ORDER BY register_date) AS prices
                FROM listings
                GROUP BY
                place_id,
                listing_id
        );
        """
    ]


def get_pandas_dbconn():
    if dbconn is None:
        uri = 'postgresql://{}:{}@{}:{}/{}'.format(
            DBPARAMS["user"],
            quote(DBPARAMS["password"]),
            DBPARAMS["host"],
            DBPARAMS["port"],
            DBPARAMS["database"]
        )
        print(uri)
        return create_engine(uri).connect()
    return dbconn


def get_place_ids_urls(place_ids_csv):

    place_ids =  CITY_CODES_DF['place_id'].to_list()
    url = "https://www.meilleursagents.com/annonces/achat/search/?item_types=ITEM_TYPE.APARTMENT"
    url_map = {}
    for place_id in place_ids:
        url_params = {"place_ids":place_id}
        final_url = enrich_url(url,url_params)
        url_map[place_id] = final_url
    return url_map

    {place_id:url_parse(url_template,place)}

def enrich_url(url, url_params):
    url_parse = urlparse(url)
    query = url_parse.query
    url_dict = dict(parse_qsl(query))
    url_dict.update(url_params)
    url_new_query = urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    return urlunparse(url_parse)

