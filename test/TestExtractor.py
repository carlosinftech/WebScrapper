import unittest


from pathlib import Path
from Extractor import Extractor
import codecs
import io


class TestTransformer(unittest.TestCase):

    def test_query_file(self):
        extractor = Extractor()
        f = codecs.open('../test/resources/page_sample.html', "r", "utf-8")
        html_file = f.read()
        f.close()
        obtained = extractor.query_file(io.StringIO(html_file),"//div[@class='listing-item search-listing-result__item']")
        self.assertEqual(len(obtained),12)



    def test_query_node(self):
        extractor = Extractor()
        f = codecs.open('../test/resources/page_sample.html', "r", "utf-8")
        html_file = f.read()
        f.close()
        all_listings_query = "//div[@class='listing-item search-listing-result__item']" \
                             "/div[@class='listing-item__content']" \
                             "/a[@class='listing-item__characteristics no-underline']"
        size_query = "div[@class='listing-characteristic margin-bottom']"
        price_query = "div[@class='listing-price margin-bottom']"
        place_query = "div[@class='text--muted text--small']"
        xpath_query = "|".join(["/".join([all_listings_query,size_query]),
                               "/".join([all_listings_query, price_query]),
                               "/".join([all_listings_query,place_query])])
        all_nodes =  extractor.query_file(io.StringIO(html_file),xpath_query)

        expected = {"listing_id":"1971642179","place_id":"2259,2260","price":"92.000 €","area":"24 m²","room_count":"1"}


        ##obtained = extractor.node_to_string_list(extractor.query_node(first_listing_node,xpath_query))
        obtained = extractor.node_list_to_string_list(all_nodes)
        self.assertEqual(expected, obtained)

    def test_node_to_string_list(self):
        extractor = Extractor()
        f = codecs.open('../test/resources/page_sample.html', "r", "utf-8")
        html_file = f.read()
        f.close()
        node_list = extractor.query_file(io.StringIO(html_file), "//div[@class='listing-item search-listing-result__item']")
        obtained = extractor.node_to_string_list(node_list)
        expected = """ """

        self.assertEqual(expected, obtained)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()