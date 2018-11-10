from selenium import webdriver

from unittest import TestCase, main

driver = webdriver.Chrome()

sample = {
    '1': 'sum_test.asm',
    '2': 'arithmetic_expression.asm',
    '3': 'arithmetic_shift.asm',
    '4': 'array.asm',
    '5': 'area.asm',
    '6': 'loop.asm',
    '7': 'log.asm',
    '8': 'array_average_test.asm',
    '9': 'cel_to_fah.asm',
    '10': 'change_array_elem_test.asm',
    '11': 'int_square_root.asm',
    '12': 'power.asm',
    '13': 'data.asm',
    '14': 'key_test.asm',
    '15': 'mem_register_test.asm'
}


class TestSample(TestCase):

    def load_page(self):
        driver.get('http://www.emu86.org/')

    def close_page(self):
        driver.quit()

    def get_by_x_path(self, value):
        return driver.find_element_by_xpath(value)

    def getById(self, id):
        return driver.find_element_by_id(id)

    def test_link(self):
        self.load_page()
        self.getById('subButton').click()
        option_path = '//*[@id="sample"]/option'
        for sample_opt in range(1, 17):
            self.get_by_x_path('//*[@id="sample"]').click()
            opt_num_path = option_path + '[' + str(sample_opt) + ']'
            self.get_by_x_path(opt_num_path).click()
            val = ""
            if sample_opt != 1:
                file_name = '../tests/Intel/' + sample[str(sample_opt - 1)]
                file = open(file_name, 'r')
                val = file.read()
                file.close()
            code = self.get_by_x_path('//*[@id="id_code"]')
            code_val = code.get_attribute('value')
            text_area = repr(code_val)
            self.assertEqual(text_area, repr(val))
        self.close_page()


if __name__ == '__main__':
    main()
