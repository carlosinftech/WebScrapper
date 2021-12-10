
class Transformer:

    def dummy_function(self,dataframe,options):
        return dataframe

    def strip(self,dataframe,options):
        dataframe[options.input_column] = dataframe[options.input_column].astype(str).str.strip()
        return dataframe

    def cast(self,dataframe,options):
        dataframe = dataframe.astype(options.datatype)
        return dataframe

    def literal(self, dataframe, options):
        dataframe[options.input_column] = options.literal
        return dataframe

    def extract(self,dataframe,options):
        dataframe[options.input_column] = dataframe[options.input_column].astype(str).str.extract(options.regex)
        return dataframe.copy()

    def replace(self,dataframe,options):
        dataframe[options.input_column] = dataframe[options.input_column].astype(str).str.replace(options.old_string,options.new_string,regex=False)
        return dataframe

    def get_replace(self,dataframe,options):
        dataframe[options.input_column] = dataframe.get(options.input_column).astype(str).str.replace(options.old_string,options.new_string,regex=False)
        return dataframe

    def duplicate(self,dataframe,options):
        dataframe[options.output_column] = dataframe[options.input_column].copy()
        return dataframe.copy()


