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


    def test_get_grouped_data(self):
        website = "./tahema_county_table_data.html"
        with Tahema(website) as t:
            data = [single_data for single_data in t._get_all_table_elements()]
            tops = list(itertools.islice(data, 50))
            view_indices = (i for i, item in enumerate(tops) if "VIEW" in item)
            grouped_data = [item for view_indx in view_indices for item in t.get_grouped_data(tops, view_indx)]
            print(list(grouped_data))
            self.assertEqual(len(list(grouped_data)),
                1,
                'test for get_grouped_data')
            self.assertEqual(len(list(grouped_data)[0]),
                1,
                'message')

    def test_tabulate_data(self):
        website = "./tahema_county_table_data.html"
        with Tahema(website) as t:
            tops = list(itertools.islice(t.tabulate_data(), 5))
            self.assertEqual(tops[0][0][1], "VIEW", 'view element and view text')

    def test_check_instrument_type(self):
        row = ['VIEW', '2016014255', 'DEED OF TRUST', '12/01/2016', 'MILLER, EVELYN']
        self.assertTrue(Tahema.check_instrument_type(row),
            'row has a deed of trust')
        row = [1, 2, 'DEED', 4, 5]
        self.assertTrue(Tahema.check_instrument_type(row),
            'row has check instrument type deed')

    @unittest.expectedFailure
    def test_click_on_view(self):
        website = "./tahema_county_table_data.html"
        with Tahema(website) as t:
            tops = list(itertools.islice(t.tabulate_data(), 5))
            t.click_on_view(tops[0])
            self.fail(t.driver.current_url,
                "something",
                'the user moves to a webpage with title something: fix this test')


    def test_parse_view_page(self):
        website = "./view_page.html"
        with Tahema(website) as t:
            table_text = [text for text in t.parse_view_page()]
            self.assertTrue("document not available" in table_text,
                'should give all the tabular data in view page')

    def test_clean_view_page_date(self):
        website = "./view_page.html"
        with Tahema(website) as t:
            table_text = [text for text in t.parse_view_page()]
            res = t.clean_view_page_data(table_text)
            print(res)
            self.assertEqual(len(res),
                6,
                'only valid tabular data should come of the view page')


if __name__ == '__main__':
    unittest.main()
