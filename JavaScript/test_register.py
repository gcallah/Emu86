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

    def binary_val(self, value):
        if value >= 0:
            return bin(value).split('b')[-1]
        else:
            pos_b = bin(value * -1).split('b')[-1]
            pos_b_lst = []
            for num in pos_b:
                pos_b_lst.append(num)
            pos_b_lst.reverse()
            one = False
            for index in range(len(pos_b_lst)):
                if one and pos_b_lst[index] == '1':
                    pos_b_lst[index] = '0'
                elif one and pos_b_lst[index] == '0':
                    pos_b_lst[index] = '1'
                elif pos_b_lst[index] == '1':
                    one = True
            pos_b_lst.reverse()
            neg_b = "".join(pos_b_lst)
            neg_b = (32 - len(pos_b)) * '1' + neg_b
            return neg_b

    def test_reg(self):
        self.driver = webdriver.Chrome()
        self.load_page()
        lang_flag = '//*[@id="content-main"]/h5/form/select/option['
        lang_flag += str(1) + ']'
        self.get_by_x_path(lang_flag).click()
        self.get_by_id('subButton').click()
        option_path = '//*[@id="sample"]/option'
        self.get_by_x_path('//*[@id="sample"]').click()
        registers = ['EAX', 'EBX', 'ECX', 'EDX']
        # for sample_opt in range(8, 17):
        for sample_opt in range(2, 17):
            self.get_by_id('clear-button').click()
            opt_num_path = option_path + '[' + str(sample_opt) + ']'
            self.get_by_x_path(opt_num_path).click()
            self.get_by_id('run-button').click()
            for reg in registers:
                reg_intel = self.get_by_name(reg)
                reg_val = int(reg_intel.get_attribute('value'))
                reg_intel.click()
                message = 'Binary value of ' + reg + ': '
                message += self.binary_val(reg_val)
                alert = self.driver.switch_to.alert
                alert_message = alert.text
                alert.accept()
                self.assertEqual(message, alert_message)
        self.close_page()


if __name__ == '__main__':
    main()
