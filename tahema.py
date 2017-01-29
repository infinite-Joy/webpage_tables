import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

current_working_dir = os.getcwd()


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
        search_button.click()

        print(self.driver.current_url)

    def _get_all_table_elements(self):
        for row in self.driver.find_elements_by_css_selector("table"):
            cells = row.find_elements_by_tag_name("td")
            for cell in cells:
                yield cell.text

    def tabulate_data(self):
        data = [single_data for single_data in self._get_all_table_elements()]
        view_indices = (i for i, item in enumerate(data) if "VIEW" in item)
        grouped_data = ([data[i + j] for j in range(5)] for i in view_indices)
        return grouped_data

    def build_csv(self, grouped_data):
        pass


if __name__ == '__main__':
    website = "http://tehamapublic.countyrecords.com/scripts/hfweb.asp?formuser=public&Application=TEH"
    t = Tahema(website)
    t.get_official_records()
    t.search_by_recording_date("12/01/2016", "12/01/2016")
    # t.get_all_table_elements()
    t.tabulate_data()
