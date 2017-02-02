import unittest
import itertools

from webpage_tables import WebpageTables

class CrawlerTest(unittest.TestCase):
    def setUp(self):
        """docstring for CrawlerTest."""
        pass

    def tearDown(self):
        pass

    def test_get_official_records(self):
        website = "./WebpageTables_home.html"
        with WebpageTables(website) as t:
            t = WebpageTables(website)
            self.assertTrue("TehamaPublic.CountyRecords.com" in t.driver.title)

    def test__get_all_table_elements(self):
        website = "./WebpageTables_table_data.html"

        def execute_test_case(items):
            print(list(items))
            self.fail('view is gving none with it')
            self.assertEqual(list(item)[2],
                'DEE OF TRUST',
                'the actual second item has deed')
            self.assertTrue(isinstance(item[0], tuple), 'first item is a tuple')

        with WebpageTables(website) as t:
            # for item in t._get_all_table_elements():
            #     execute_test_case(item)
            execute_test_case(t._get_all_table_elements())


    def test_get_grouped_data(self):
        website = "./WebpageTables_table_data.html"
        with WebpageTables(website) as t:
            data = [single_data for single_data in t._get_all_table_elements()]
            tops = list(itertools.islice(data, 50))
            view_indices = (i for i, item in enumerate(tops) if "VIEW" in item)
            grouped_data = list(t.get_grouped_data(tops, view_indices))

            # tests
            self.assertEqual(grouped_data[0][0][1],
                "VIEW",
                'the first element description')
            self.assertEqual(grouped_data[0][1:],
                ['2016014255', 'DEED OF TRUST', '12/01/2016', 'MILLER, EVELYN'],
                'the rest of the elements')
            self.assertEqual(len(grouped_data),
                1,
                'test for get_grouped_data')
            self.assertEqual(len(list(grouped_data)[0]),
                5,
                'message')

    def test_check_instrument_type(self):
        row = ['VIEW', '2016014255', 'DEED OF TRUST', '12/01/2016', 'MILLER, EVELYN']
        self.assertTrue(WebpageTables.check_instrument_type(row),
            'row has a deed of trust')
        row = [1, 2, 'DEED', 4, 5]
        self.assertTrue(WebpageTables.check_instrument_type(row),
            'row has check instrument type deed')

    @unittest.expectedFailure
    def test_click_on_view(self):
        website = "./WebpageTables_table_data.html"
        with WebpageTables(website) as t:
            tops = list(itertools.islice(t.tabulate_data(), 5))
            t.click_on_view(tops[0])
            self.fail(t.driver.current_url,
                "something",
                'the user moves to a webpage with title something: fix this test')


    def test_parse_view_page(self):
        website = "./view_page.html"
        with WebpageTables(website) as t:
            table_text = [text for text in t.parse_view_page()]
            self.assertTrue("document not available" in table_text,
                'should give all the tabular data in view page')

    def test_clean_view_page_date(self):
        website = "./view_page.html"
        with WebpageTables(website) as t:
            table_text = [text for text in t.parse_view_page()]
            res = t.clean_view_page_data(table_text)
            print(res)
            self.assertEqual(len(res),
                10,
                'only valid tabular data should come of the view page')


if __name__ == '__main__':
    unittest.main()
