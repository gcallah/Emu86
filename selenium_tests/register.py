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

    def binary_val_hex(self, value):
        '''
        Determine if the value is negative or positive
        After converting the value to decimal without the negative sign to hex
        Call the binary conversion on the converted decimal number
        '''
        neg = False
        if value[0] == "-":
            neg = True
            value = int(value[1:], 16)
        else:
            value = int(value, 16)
        if neg:
            value *= -1
        return self.binary_val_dec(value)

    def binary_val_dec(self, value):
        value = int(value)
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

    def reg_test(self, lang, reg_lst):
        self.driver = webdriver.Chrome()
        self.load_page()
        lang_flag = '//*[@id="content-main"]/h5/form/select/option['
        lang_flag += str(lang) + ']'
        # set the number system
        num_sys = "dec"
        if lang == 3:
            num_sys = "hex"
        self.get_by_x_path(lang_flag).click()
        self.get_by_id('subButton').click()
        option_path = '//*[@id="sample"]/option'
        self.get_by_x_path('//*[@id="sample"]').click()
        # for each sample, run the register click test
        for sample_opt in range(2, 17):
            # make sure to reinitialize before running
            self.get_by_id('clear-button').click()
            opt_num_path = option_path + '[' + str(sample_opt) + ']'
            self.get_by_x_path(opt_num_path).click()
            self.get_by_id('run-button').click()
            # go through each register in the list and click!
            for reg in reg_lst:
                reg_intel = self.get_by_name(reg)
                reg_val = reg_intel.get_attribute('value')
                reg_intel.click()
                message = 'Binary value of ' + reg + ': '
                if num_sys == "dec":
                    message += self.binary_val_dec(reg_val)
                else:
                    message += self.binary_val_hex(reg_val)
                alert = self.driver.switch_to.alert
                alert_message = alert.text
                alert.accept()
                # check to see if the binary message is the same as the
                # alert message
                self.assertEqual(message, alert_message)
        self.close_page()

    def test_reg_conversion(self):
        # testing register clicks for Intel in decimal
        self.reg_test(1, ['EAX', 'EBX', 'ECX', 'EDX'])

        # create the register list for mips
        mips_reg = []
        for i in range(1, 18):
            mips_reg.append("R" + str(i))

        # testing register clicks for MIPS in hex
        self.reg_test(3, mips_reg)


if __name__ == '__main__':
    main()
