import pandas as pd

class Reader():

    def read(self):
       pass



class DBReader(Reader):

    def read(self,dataframe,dbconn):
        dataframe = pd.read_sql('select * from listings', dbconn)
        print(dataframe)
