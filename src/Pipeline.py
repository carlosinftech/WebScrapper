from src.Transformer import Transformer

class Pipeline:
    """Class used to represent a pandas dataframe transformation pipeline. """

    def __init__(self,work_dataframe,transformations_list):
        self.work_dataframe = work_dataframe
        self.transformations_list = transformations_list
        self.transformer = Transformer()
        self.__transformation_map = self.__build_transformation_map()

    def __build_transformation_map(self):
        """This map allows to connect strings with the different functions to be executed. """
        return{
            'strip':self.transformer.strip,
            'cast':self.transformer.cast,
            'extract': self.transformer.extract,
            'replace':self.transformer.replace,
            'get_replace': self.transformer.get_replace,
            'duplicate':self.transformer.duplicate,
            'literal':self.transformer.literal,
            'add_current_date':self.transformer.add_current_date,
            'to_numeric':self.transformer.to_numeric
        }

    def apply_transformations(self):
        """Class used to represent a pandas dataframe transformation pipeline. """
        for i in range(len(self.transformations_list)):
            transformation = self.transformations_list[i]
            transformation_function = self.__transformation_map.get(transformation.name,self.transformer.dummy_function(self.work_dataframe,transformation.options))
            self.work_dataframe = transformation_function(self.work_dataframe,transformation.options)


