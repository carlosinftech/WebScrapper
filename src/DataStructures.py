

class TransformationDefinition:

  def __init__(self, name,options):
    self.name = name
    self.options = options

class TransformationOptions:
  def __init__(self,  input_column='', output_column='',datatype = '',regex = '',old_string = '', new_string = '',literal = ''):
    self.input_column = input_column
    self.output_column = output_column
    self.datatype = datatype
    self.regex = regex
    self.old_string = old_string
    self.new_string = new_string
    self.literal = literal
