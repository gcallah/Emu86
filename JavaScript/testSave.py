from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()

from unittest import TestCase, main

class TestSave(TestCase):

    def load_page(self):
        driver.get('http://www.emu86.org/')

    def close_page(self):
        driver.quit()

    def get_by_x_path(self, value):
        return driver.find_element_by_xpath(value)

    def getById(self, id):
        return driver.find_element_by_id(id)

    def test_save(self):
        self.load_page()
        self.getById('subButton').click()
        option_path = '//*[@id="sample"]/option'
        self.get_by_x_path('//*[@id="sample"]').click()
        self.get_by_x_path(option_path + '[' + str(13) + ']').click()
        self.getById('save-button').click()
        save_prompt = driver.switch_to.alert
        save_prompt.send_keys("power.hello")
        save_prompt.accept();
        try:
            driver.switch_to.alert.accept();
            print("Alert raised!")
        except:
            print("Valid file name")
        driver.close()

if __name__ == '__main__':
    main()
