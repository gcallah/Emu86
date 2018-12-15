from random import randint
from selenium import webdriver

from unittest import TestCase, main


class TestSave(TestCase):

    def load_page(self):
        self.driver.get('http://www.emu86.org/')

    def close_page(self):
        self.driver.quit()

    def get_by_x_path(self, value):
        return self.driver.find_element_by_xpath(value)

    def get_by_id(self, id):
        return self.driver.find_element_by_id(id)

    def create_file_name(self):
        name = []
        for i in range(0, 10):
            ord_let = randint(0,25)
            letter = chr(ord('a') + ord_let)
            name.append(letter)
            if i == 6:
                name.append(".")
        return "".join(name)

    def test_save(self):
        self.driver = webdriver.Chrome()
        self.load_page()
        self.get_by_id('subButton').click()
        option_path = '//*[@id="sample"]/option'
        self.get_by_x_path('//*[@id="sample"]').click()
        self.get_by_x_path(option_path + '[' + str(13) + ']').click()
        self.get_by_id('save-button').click()
        save_prompt = self.driver.switch_to.alert
        file_name = self.create_file_name()
        save_prompt.send_keys(file_name)
        save_prompt.accept()
        valid_file = "Invalid file name: " + file_name
        if file_name[-4:] == ".asm":
            valid_file = ""
        try:
            alert = self.driver.switch_to.alert
            alert_message = alert.text
            alert.accept()
            self.assertEqual(alert_message, valid_file)
        except Exception:
            self.assertEqual("",valid_file)
        self.close_page()


if __name__ == '__main__':
    main()
