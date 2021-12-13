from src.DataStructures import TransformationDefinition, TransformationOptions

from src.Pipeline import Pipeline
from src.Reader import DBReader
from src.Writer import CSVWriter, DBWriter
from src.Extractor import Extractor
import io
import pandas as pd
from configuration import config
from configuration.config import all_listing_ids_query,area_query,price_query,listings_table_name,sql_count_query


class Executor:
    """This class manages the dataframe trnasformation process until it is written to a Database """
    pandas_db_writer = DBWriter()
    pandas_db_reader = DBReader()

    def run_scraper(self, place_id, page_number, html_file):
        """This method performs different xpath queries of the subjects that we are in need"""
        query_place_id = place_id
        extractor = Extractor()

        all_listing_ids = extractor.query_file(io.StringIO(html_file), all_listing_ids_query)
        all_areas = extractor.query_file(io.StringIO(html_file), area_query)
        all_prices = extractor.query_file(io.StringIO(html_file), price_query)
        listing_id_column = extractor.create_column_from_string_list("listing_id", all_listing_ids)
        area_column = extractor.create_column_from_string_list("area", extractor.get_text_for_nodes(all_areas))
        price_column = extractor.create_column_from_string_list("price", extractor.get_text_for_nodes(all_prices))

        # for python 3.9 or greater
        # listings_dictionary = area_column|price_column|listing_id_column
        listings_dictionary = {**area_column, **price_column, **listing_id_column}

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        try:
            listings_dataframe = pd.DataFrame.from_dict(listings_dictionary)
            obtained_dataframe = self.run_pipeline(listings_dataframe,query_place_id)
            self.write_result(obtained_dataframe)
        except:
            print("dataframe could not be created columns not of same length")
            pass

    def run_pipeline(self,listings_dataframe,query_place_id):
        """Contains all the transformation steps of the original dataframe
           in order to obtain the expected one. In the future this objects are expected
           to be created automatically from a configuration file. """
        pipeline_steps = [
            TransformationDefinition(name='literal',
                                     options=TransformationOptions(input_column='place_id', literal=query_place_id)),
            TransformationDefinition(name='cast', options=TransformationOptions(datatype='str')),
            TransformationDefinition(name='extract', options=TransformationOptions(input_column='listing_id',
                                                                                   regex=r'listing_id\=(.*)\|realtor_id')),
            TransformationDefinition(name='duplicate',
                                     options=TransformationOptions(input_column='area', output_column="room_count")),
            TransformationDefinition(name='extract',
                                     options=TransformationOptions(input_column='area', regex=r'-\s([0-9]+)\smÂ²')),
            TransformationDefinition(name='replace',
                                     options=TransformationOptions(input_column='room_count', old_string='Studio',
                                                                   new_string='Appartement 1 piÃ¨ces')),
            TransformationDefinition(name='replace',
                                     options=TransformationOptions(input_column='price', old_string=' ',
                                                                   new_string='')),
            TransformationDefinition(name='extract',
                                     options=TransformationOptions(input_column='room_count',
                                                                   regex=r't\s([0-9]+)\spi')),
            TransformationDefinition(name='extract',
                                     options=TransformationOptions(input_column='price', regex=r'([0-9]+)')),
            TransformationDefinition(name='add_current_date',
                                     options=TransformationOptions(input_column='register_date')),
            TransformationDefinition(name='to_numeric',
                                     options=TransformationOptions(input_column='listing_id')),
            TransformationDefinition(name='to_numeric',
                                     options=TransformationOptions(input_column='place_id')),
            TransformationDefinition(name='to_numeric',
                                     options=TransformationOptions(input_column='area')),
            TransformationDefinition(name='to_numeric',
                                     options=TransformationOptions(input_column='room_count')),
            TransformationDefinition(name='to_numeric',
                                     options=TransformationOptions(input_column='price'))

        ]

        transformation_pipeline = Pipeline(listings_dataframe, pipeline_steps)
        transformation_pipeline.apply_transformations()
        return transformation_pipeline.work_dataframe

    def write_result(self,dataframe):
        self.pandas_db_writer.write(dataframe, listings_table_name,config.get_pandas_dbconn())
        count_lines_in_table = self.pandas_db_reader.read(sql_count_query, config.get_pandas_dbconn())
        config.get_pandas_dbconn().close()
        print(count_lines_in_table)
