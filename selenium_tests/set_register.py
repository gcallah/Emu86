from selenium import webdriver

from unittest import TestCase, main


class TestRegisters(TestCase):

    def load_page(self):
        self.driver.get('http://www.emu86.org/')

    def close_page(self):
        self.driver.quit()

    def get_by_x_path(self, value):
        return self.driver.find_element_by_xpath(value)

    def get_by_id(self, id):
        return self.driver.find_element_by_id(id)

    def get_by_name(self, name):
        return self.driver.find_element_by_name(name)

    def enter_inputs(self, input_box, value):
        input_box.clear()
        input_box.send_keys(value)

    def set_reg(self, reg, val):
        reg = self.get_by_name(reg)
        self.enter_inputs(reg, val)

    def reg_test(self, lang, reg, val):
        self.driver = webdriver.Chrome()
        self.load_page()
        # click on the language: Intel or MIPS_ASM
        lang_flag = '//*[@id="content-main"]/h5/form/select/option['
        lang_flag += str(lang) + ']'
        self.get_by_x_path(lang_flag).click()
        self.get_by_id('subButton').click()
        # set the register to be the value upon initializing
        self.set_reg(reg, val)
        # click on the add two numbers sample and run
        option_path = '//*[@id="sample"]/option'
        opt_num_path = option_path + '[' + str(2) + ']'
        self.get_by_x_path(opt_num_path).click()
        self.get_by_id('run-button').click()
        # check to make sure that the register value clicked on
        # is the value inputted
        reg_val = self.get_by_name(reg).get_attribute('value')
        self.assertEqual(reg_val, val)
        self.close_page()

    def test_set_reg(self):
        # write to ECX : 10
        self.reg_test(1, 'ECX', '10')
        # wwrite to R26: 10
        self.reg_test(3, 'R26', '10')


if __name__ == '__main__':
    main()
