import pandas as pd

class Reader():

    def read(self):
       pass



class DBReader(Reader):

    def read(self,db_query,dbconn):
        dataframe = pd.read_sql('select count(*) from listings', dbconn)
        dbconn.close()
        return dataframe