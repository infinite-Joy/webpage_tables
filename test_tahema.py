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
        t = Tahema(website)
        assert "TehamaPublic.CountyRecords.com" in t.driver.title

    def test__get_all_table_elements(self):
        website = "./tahema_county_table_data.html"
        t = Tahema(website)
        for item in t._get_all_table_elements():
            if item == ['VIEW', '2016014255', 'DEED OF TRUST', '12/01/2016', 'MILLER, EVELYN']:
                assert True
                break

    def test_tabulate_data(self):
        website = "./tahema_county_table_data.html"
        t = Tahema(website)
        tops = list(itertools.islice(t.tabulate_data(), 5))
        assert tops[0] == ['VIEW', '2016014255', 'DEED OF TRUST', '12/01/2016', 'MILLER, EVELYN']


if __name__ == '__main__':
    unittest.main()
