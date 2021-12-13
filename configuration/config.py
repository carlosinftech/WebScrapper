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
    city_codes_df = pandas.read_csv(place_ids_csv)
    place_ids =  city_codes_df['place_ids'].to_list()
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

