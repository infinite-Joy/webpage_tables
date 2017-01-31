import os
import  itertools
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

current_working_dir = os.getcwd()

rate = 0


def log_it(e):
    pass


class Tahema(object):
    """
    will parse through the webpages of Tahema county website
    and get the relevant information.
    """
    def __init__(self, website):
        super(Tahema, self).__init__()
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
        print(self.driver.current_url)
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
                    yield (cell, cell_text)
                else:
                    yield cell_text

    def get_grouped_data(self, data, view_indx):
        # return ([data[i + j] for j in range(5)] for i in view_indices)
        while True:
            grouped_data = []
            k = [data[view_indx + j] for j in range(5)]
            grouped_data.append(k)
            try:
                if self.check_instrument_type(k):
                    self.click_on_view(k)
                    parsed_view_page_table = self.parse_view_page()
                    grouped_data.append(self.clean_view_page_data(parsed_view_page_table))
                    # self.driver.key_down(Keys.CONTROL).send_keys(key.LEFT).key_up(Keys.CONTROL).perform()
                    self.driver.send_keys(Keys.LEFT_ALT) # go back
            except TypeError:
                pass
            yield grouped_data

    def tabulate_data(self):
        """
        clean the tabular data from the website and give a list of lists
        """
        data = [single_data for single_data in self._get_all_table_elements()]
        view_indices = (i for i, item in enumerate(data) if "VIEW" in item)
        grouped_data = self.get_grouped_data(data, view_indices)
        return grouped_data

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
        if self.check_instrument_type(row):
            view_element = row[0][0]

            # before each call there is a rate limiter of 1 second
            time.sleep(rate)
            view_element.click()

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

        start = self.get_starting_index(parsed_view_page_table)
        documents = {parsed_view_page_table[i]: parsed_view_page_table[i+1] for i in range(start, start + 11, 2)}
        return documents

    def build_csv(self, grouped_data):
        pass

    def __exit__(self, *args):
        """
        give all the exit code
        this will execute when the browser leaves the with block
        """
        self.driver.quit()


if __name__ == '__main__':
    website = "http://tehamapublic.countyrecords.com/scripts/hfweb.asp?formuser=public&Application=TEH"
    with Tahema(website) as t:
        t.get_official_records()
        t.search_by_recording_date("12/01/2016", "12/01/2016")
        tops = list(itertools.islice(t.tabulate_data(), 5))
        print(tops)
    # website = "./view_page.html"
    # with Tahema(website) as t:
    #     for rows in t.parse_view_page():
    #         print(rows)
