import requests

from lxml import etree


class Extractor:
    """This class manages the methods for extracting data from html files using xpath"""
    def __init__(self):
        self.parser = etree.HTMLParser()

    def query_file(self,html_file, xpath_query):
        tree = etree.parse(html_file,self.parser)
        root_node = tree.getroot()
        xpath_query_result = root_node.xpath(xpath_query)
        return xpath_query_result

    def query_node(self,xpath_node,xpath_query):
        xpath_query_result = xpath_node.xpath(xpath_query)
        return xpath_query_result

    def get_text_for_nodes(self,xpath_node_list):
        return [xpath_node.text for xpath_node in xpath_node_list]

    def get_tag_for_nodes(self,xpath_node_list):
        return [xpath_node.tag for xpath_node in xpath_node_list]

    def create_column_from_xpath_nodes(self,column_name,xpath_node_list,xpath_query):
        return {column_name: [self.get_tag_for_nodes(self.query_node(node,xpath_query))for node in xpath_node_list]}

    def create_column_from_string_list(self,column_name,string_list):
        return {column_name: string_list}


