import unittest
import itertools

from tahema import Tahema

class CrawlerTest(unittest.TestCase):
    def setUp(self):
        """docstring for CrawlerTest."""
        pass

    def tearDown(self):
        pass

    def test_get_official_records(self):
        website = "./tahema_home.html"
        with Tahema(website) as t:
            t = Tahema(website)
            self.assertTrue("TehamaPublic.CountyRecords.com" in t.driver.title)

    def test__get_all_table_elements(self):
        website = "./tahema_county_table_data.html"

        def execute_test_case(item):
            try:
                if item[2] == 'DEED OF TRUST':
                    assertTrue(isinstance(item[0], tuple))
            except IndexError as e:
                # handling this in case of item not being build.
                # we only want to see if there is atleast one valid item
                pass

        with Tahema(website) as t:
            for item in t._get_all_table_elements():
                execute_test_case(item)


    def test_tabulate_data(self):
        website = "./tahema_county_table_data.html"
        with Tahema(website) as t:
            tops = list(itertools.islice(t.tabulate_data(), 5))
            self.assertEqual(tops[0][0][1], "VIEW", 'view element and view text')

    def test_check_instrument_type(self):
        row = ['VIEW', '2016014255', 'DEED OF TRUST', '12/01/2016', 'MILLER, EVELYN']
        self.assert_(Tahema.check_instrument_type(row),
            'row has a deed of trust')
        row = [1, 2, 'DEED', 4, 5]
        self.assert_(Tahema.check_instrument_type(row),
            'row has check instrument type deed')



if __name__ == '__main__':
    unittest.main()
