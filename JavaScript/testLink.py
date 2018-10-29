from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from unittest import TestCase, main

driver = webdriver.Chrome()

link = {
    '1': 'area.asm',
    '2': 'arithmetic_expression.asm',
    '3': 'arithmetic_shift.asm',
    '4': 'array.asm', 
    '5': 'array_average_test.asm',
    '6': 'cel_to_fah.asm',
    '7': 'change_array_elem_test.asm',
    '8': 'data.asm',
    '9': 'int_square_root.asm',
    '10': 'key_test.asm',
    '11': 'log.asm',
    '12': 'loop.asm',
    '13': 'mem_register_test.asm',
    '14': 'power.asm',
    '15': 'sum_test.asm'
}

class TestMemory(TestCase):

    def load_page(self):
        driver.get('http://www.emu86.org/')

    def close_page(self):
        driver.quit()

    def get_by_x_path(self, value):
        return driver.find_element_by_xpath(value)

    def getById(self, id):
        return driver.find_element_by_id(id)

    def test_link(self, low1 = 0, high1=16):
        for sample in range(1, 16):
            self.load_page()
            self.getById('subButton').click()
            main_x_path = '//*[@id="content-main"]/div/details[2]/'
            self.get_by_x_path('//*[@id="user-tools"]/a[2]').click()
            self.get_by_x_path(main_x_path + 'summary').click()
            self.get_by_x_path(main_x_path + 'details[1]/summary').click()
            sub_path = 'details[1]/ul/li[' + str(sample) + ']/a'
            self.get_by_x_path(main_x_path + sub_path).click()
            link_clicked = 'https://github.com/gcallah/Emu86/'
            link_clicked += 'blob/master/tests/Intel/' + link[str(sample)]
            self.assertEqual(driver.current_url, link_clicked)

        self.close_page()

if __name__ == '__main__':
    main()

