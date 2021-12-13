import pandas as pd

class Transformer:
    """This class defines all the transformations that can be applied to a dataframe in this project."""

    def dummy_function(self,dataframe,options):
        return dataframe

    def strip(self,dataframe,options):
        """Removes leading and trailing spaces from column"""
        dataframe[options.input_column] = dataframe[options.input_column].astype(str).str.strip()
        return dataframe

    def cast(self,dataframe,options):
        """Cast all columns to specified datatype."""
        dataframe = dataframe.astype(options.datatype)
        return dataframe

    def literal(self, dataframe, options):
        """Add literal column."""
        dataframe[options.input_column] = options.literal
        return dataframe

    def extract(self,dataframe,options):
        """Extracts information from cell using regex"""
        dataframe[options.input_column] = dataframe[options.input_column].astype(str).str.extract(options.regex)
        return dataframe.copy()

    def replace(self,dataframe,options):
        """Replace substring in column"""
        dataframe[options.input_column] = dataframe[options.input_column].astype(str).str.replace(options.old_string,options.new_string,regex=False)
        return dataframe

    def get_replace(self,dataframe,options):
        """Replace substring in column"""
        dataframe[options.input_column] = dataframe.get(options.input_column).astype(str).str.replace(options.old_string,options.new_string,regex=False)
        return dataframe

    def add_current_date(self,dataframe,options):
        """Add new column containing current date field"""
        dataframe[options.input_column] = pd.to_datetime("today")
        return dataframe

    def to_numeric(self,dataframe,options):
        """Cast pandas column to numeric value"""
        dataframe[options.input_column] = pd.to_numeric(dataframe[options.input_column])
        return dataframe

    def duplicate(self,dataframe,options):
        """Creates a new column based on the values of an old one. """
        dataframe[options.output_column] = dataframe[options.input_column].copy()
        return dataframe.copy()


