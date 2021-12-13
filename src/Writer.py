
class Writer():
    """Generic writer. Defines method for writing dataframe to external sink. """
    def write(self,source_dataframe):
       pass


class CSVWriter(Writer):
    """Writes a dataframe to a csv file. """
    def write(self,source_dataframe,destination):
        source_dataframe.to_csv(destination,index=False)


class DBWriter(Writer):
    """Writes a dataframe to a database """
    def write(self,source_dataframe,table_name,dbconn,if_exists_opt):
        source_dataframe.to_sql(name=table_name,con=dbconn, if_exists = if_exists_opt, chunksize = 1000,index=False)
        dbconn.close()