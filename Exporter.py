
from configuration import config
from configuration.config import sql_price_average,price_average_table,CITY_CODES_DF,postal_code_place_id_table,sql_price_range,price_range_table
from src.Reader import DBReader
from src.Writer import DBWriter

class Exporter:
    """ script that creates tables to serve flask application"""
    pandas_db_reader = DBReader()
    pandas_db_writer = DBWriter()

    def serve_postal_code_place_id(self):
        self.pandas_db_writer.write(CITY_CODES_DF, postal_code_place_id_table, config.get_pandas_dbconn(), 'replace')

    def serve_price_average(self):
        price_average_df = self.pandas_db_reader.read(sql_price_average, config.get_pandas_dbconn())
        self.pandas_db_writer.write(price_average_df,price_average_table, config.get_pandas_dbconn(),'replace')

    def serve_price_range(self):
        price_range_df = self.pandas_db_reader.read(sql_price_range, config.get_pandas_dbconn())
        self.pandas_db_writer.write(price_range_df,price_range_table, config.get_pandas_dbconn(),'replace')

if __name__ == '__main__':
    exporter = Exporter()
    exporter.serve_postal_code_place_id()
    exporter.serve_price_average()
    exporter.serve_price_range()
