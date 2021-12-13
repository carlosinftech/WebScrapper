
class Writer():

    def write(self,source_dataframe):
       pass


class CSVWriter(Writer):

    def write(self,source_dataframe,destination):
        source_dataframe.to_csv(destination,index=False)


class DBWriter(Writer):

    def write(self,source_dataframe,table_name,dbconn):
        source_dataframe.to_sql(name=table_name,con=dbconn, if_exists = 'append', chunksize = 1000,index=False)