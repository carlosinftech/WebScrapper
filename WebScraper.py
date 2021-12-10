import codecs

from DataStructures import TransformationDefinition, TransformationOptions
from Navigator import Navigator
from Pipeline import Pipeline
from Transformer import Transformer
from src.Extractor import Extractor
import io
import pandas as pd

def connect(url):
    navigator = Navigator()
    full_html = navigator.get_html_from_url("https://www.meilleursagents.com/annonces/achat/search/?item_types=ITEM_TYPE.APARTMENT&place_ids=32682&page=1")
    navigator.obtain_last_page_node(full_html)

def run_scraper(url):
    # Use a breakpoint in the code line below to debug your script.
    #TODO put pipeline in conf file

    query_place_id = '2259'
    f = codecs.open('test/resources/page_sample.html', "r", "utf-8")
    html_file = f.read()
    f.close()
    extractor = Extractor()

    area_query =  "//div[@class='listing-characteristic margin-bottom']"
    price_query = "//div[@class='listing-price margin-bottom']"
    all_listing_ids_query = "//div[@class='listing-item search-listing-result__item']//@data-wa-data"

    #TODO query file just once
    all_listing_ids = extractor.query_file(io.StringIO(html_file), all_listing_ids_query)
    all_areas = extractor.query_file(io.StringIO(html_file), area_query)
    all_prices = extractor.query_file(io.StringIO(html_file), price_query)
    listing_id_column = extractor.create_column_from_string_list("listing_id", all_listing_ids)
    area_column = extractor.create_column_from_string_list("area", extractor.get_text_for_nodes(all_areas))
    price_column = extractor.create_column_from_string_list("price",extractor.get_text_for_nodes(all_prices))

    listings_dictionary = area_column|price_column|listing_id_column

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    listings_dataframe = pd.DataFrame.from_dict(listings_dictionary)


    pipeline_steps = [
        TransformationDefinition(name='literal',
                                 options=TransformationOptions(input_column='place_id', literal=query_place_id)),
        TransformationDefinition(name='cast', options=TransformationOptions(datatype='str')),
        TransformationDefinition(name='extract', options=TransformationOptions(input_column='listing_id', regex=r'listing_id\=(.*)\|realtor_id')),
        TransformationDefinition(name='duplicate',
                                 options=TransformationOptions(input_column='area', output_column="room_count")),
        TransformationDefinition(name='extract',
                                 options=TransformationOptions(input_column='area', regex=r'-\s(.*)\sm²')),

        TransformationDefinition(name='replace',
                                 options=TransformationOptions(input_column='room_count', old_string='Studio',
                                                               new_string='Appartement 1 pièces')),
        TransformationDefinition(name='replace',
                                 options=TransformationOptions(input_column='price', old_string='\\u202f',
                                                               new_string='')),
        TransformationDefinition(name='extract',
                                 options=TransformationOptions(input_column='price', regex=r'\s(.*)\s€')),
        TransformationDefinition(name='extract',
                                 options=TransformationOptions(input_column='room_count', regex=r't\s(.*)\spi')),

    ]


    transformation_pipeline = Pipeline(listings_dataframe,pipeline_steps)
    transformation_pipeline.apply_transformations()
    print(transformation_pipeline.work_dataframe)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    url = "https://www.meilleursagents.com/annonces/achat/search/?item_types=ITEM_TYPE.APARTMENT&place_ids=2259,2260&page=1"
    run_scraper(url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
