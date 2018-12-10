from selenium import webdriver

from unittest import TestCase, main

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
        self.driver.get('http://www.emu86.org/')

    def close_page(self):
        self.driver.quit()

    def get_by_x_path(self, value):
        return self.driver.find_element_by_xpath(value)

    def getById(self, id):
        return self.driver.find_element_by_id(id)

    def option_test(self, flag):
        self.driver = webdriver.Chrome()
        self.load_page()
        lang_flag = '//*[@id="content-main"]/h5/form/select/option['
        lang_flag += str(flag) + ']'
        self.get_by_x_path(lang_flag).click()
        self.getById('subButton').click()
        option_path = '//*[@id="sample"]/option'
        option_range = 17
        if flag == 3 or flag == 4 or flag == 5:
            option_range = 15
        for sample_opt in range(1, option_range):
            self.get_by_x_path('//*[@id="sample"]').click()
            opt_num_path = option_path + '[' + str(sample_opt) + ']'
            self.get_by_x_path(opt_num_path).click()
            val = ""
            if sample_opt != 1:
                file_name = '../tests/'
                if flag == 1:
                    file_name += 'Intel/'
                elif flag == 2:
                    file_name += 'ATT/'
                elif flag == 3:
                    file_name += 'MIPS_ASM/'
                elif flag == 4:
                    file_name += 'MIPS_MML/'
                else:
                    file_name += 'RISCV/'
                file_name += sample[str(sample_opt - 1)]
                file = open(file_name, 'r')
                val = file.read()
                file.close()
            code = self.get_by_x_path('//*[@id="id_code"]')
            code_val = code.get_attribute('value')
            text_area = repr(code_val)
            self.assertEqual(text_area, repr(val))
        self.close_page()

    def test_options(self):
        for flag in range(1, 6):
            self.option_test(flag)


if __name__ == '__main__':
    main()
