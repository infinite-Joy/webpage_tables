import os
import itertools
import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

current_working_dir = os.getcwd()
rate = 1


def log_it(e):
    pass


class WebpageTables(object):
    """
    will parse through the webpages of Tahema county website
    and get the relevant information.
    """
    def __init__(self, website):
        super(WebpageTables, self).__init__()
        self.driver = webdriver.PhantomJS("%s/phantomjs" % current_working_dir)
        self.driver.set_window_size(1120, 550)
        self.driver.get(website)

    def __enter__(self):
        return self

    def get_official_records(self):
        official_records_xpath = "/html/body/div/center/p/select/option[2]"
        official_records_elem = None
        try:
            official_records_elem = self.driver.find_element_by_xpath(official_records_xpath)
        except Exception as e:
            log_it(e)
        try:
            if not official_records_elem:
                partial_link_text = "Official Records"
                official_records_elem = self.driver.find_element_by_partial_link_text(partial_link_text)
        except Exception as e:
            log_it(e)
        official_records_elem.click()
        go_xpath = "html/body/div/center/p/input"
        go_element = self.driver.find_element_by_xpath(go_xpath)
        go_element.click()
        assert "Official Records thru" in self.driver.page_source

    def search_by_recording_date(self, start_date, end_date):
        form_base_xpath = "html/body/form"
        date_input_field_xpath = ("%s/p[3]/table/tbody/tr[3]/td[2]" % form_base_xpath)
        start_date_input_field_xpath = ("%s/input[1]" % date_input_field_xpath)
        start_date_input_field = self.driver.find_element_by_xpath(start_date_input_field_xpath)
        start_date_input_field.send_keys(start_date)

        end_date_input_field_xpath = ("%s/input[2]" % date_input_field_xpath)
        end_date_input_field = self.driver.find_element_by_xpath(end_date_input_field_xpath)
        end_date_input_field.send_keys(end_date)

        search_button_xpath = ("%s/p[4]/input[1]" % form_base_xpath)
        search_button = self.driver.find_element_by_xpath(search_button_xpath)

        # before each call there is a rate limiter of 1 second
        time.sleep(rate)
        search_button.click()

    def _get_all_table_elements(self):
        """
        get the tabular data from the webpage using css idebtifiers
        will give a lot of null and empty strings as well
        """
        for row in self.driver.find_elements_by_css_selector("table"):
            cells = row.find_elements_by_tag_name("td")
            for cell in cells:
                cell_text = cell.text
                if "VIEW" in cell_text:
                    yield (cell.get_attribute("href"), cell_text)
                else:
                    yield cell_text

    def get_grouped_data(self, uncleaned_data, view_indices):
        for view_indx in view_indices:
            k = [uncleaned_data[view_indx + j] for j in range(5)]
            yield k

            # the remaining part will be worked on later
            # try:
            #     if self.check_instrument_type(k):
            #         self.click_on_view(k)
            #         parsed_view_page_table = self.parse_view_page()
            #         yield self.clean_view_page_data(parsed_view_page_table)
            #         self.driver.back()
            #         self.driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
            # except TypeError as err:
            #     print(err)

    def data_and_indices(self):
        data = [single_data for single_data in self._get_all_table_elements()]
        view_indices = (i for i, item in enumerate(data) if "VIEW" in item)
        return (data, view_indices)

    @staticmethod
    def check_instrument_type(row):
        """
        instrument type will be checked if it is deed it deed of trust
        """
        instrument_type = row[2]
        return instrument_type == "DEED" or "DEED OF TRUST"

    def click_on_view(self, row):
        """
        user sees that the instrument type is DEED and clicks on view_element
        """
        view_element = row[0][0]

        # before each call there is a rate limiter of 1 second
        time.sleep(rate)
        try:
            view_element.click()
        except WebDriverException:
            print("Element is not clickable")


    def parse_view_page(self):
        """
        look at the view page and get the results
        """
        for row in self.driver.find_elements_by_css_selector("table"):
            cells = row.find_elements_by_tag_name("td")
            for cell in cells:
                yield cell.text

    def get_starting_index(self, parsed_view_page_table):
        for i, table_text in enumerate(parsed_view_page_table):
            if "Document Number" in table_text:
                return i

    def clean_view_page_data(self, parsed_view_page_table):
        """create the list of documents"""
        start = self.get_starting_index(parsed_view_page_table)
        documents = {}
        if not start:
            return
        for i in itertools.count(start=start, step=2):
            try:
                key = parsed_view_page_table[i]
                val = parsed_view_page_table[i+1]
                documents[key] = val
            except IndexError:
                return documents

    def __exit__(self, *args):
        """
        give all the exit code
        this will execute when the browser leaves the with block
        """
        self.driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some webpages.')
    parser.add_argument('--url', help='give a valid web url')
    website = parser.parse_args()
    with Tahema(website.url) as t:
        t.get_official_records()
        t.search_by_recording_date("12/01/2016", "12/01/2016")
        data, indices = t.data_and_indices()
        for data in t.get_grouped_data(data, indices):
            print(data)
