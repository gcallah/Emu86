import random

from selenium import webdriver

from unittest import TestCase, main

NUM_TESTS = 10


class TestMemory(TestCase):

    def load_page(self):
        self.driver.get('http://www.emu86.org/')

    def close_page(self):
        self.driver.quit()

    def getById(self, id):
        return self.driver.find_element_by_id(id)

    def get_by_name(self, name):
        return self.driver.find_element_by_name(name)

    def enter_inputs(self, inputBox, value):
        inputBox.send_keys(value)

    def set_mem(self, loc, val):
        '''
        Input the memory location and value into the
        inputs memText and valueTest
        '''
        inputBox = self.getById('memText')
        self.enter_inputs(inputBox, hex(loc).upper().split('X')[-1])
        inputVal = self.getById('valueText')
        self.enter_inputs(inputVal, hex(val).upper().split('X')[-1])
        self.getById('setMem').click()

    def test_mem(self, low1=0, high1=16, low2=0, high2=100000):
        self.driver = webdriver.Chrome()
        self.load_page()
        self.getById('subButton').click()
        for i in range(0, NUM_TESTS):
            a = random.randint(low2, high2)
            b = random.randint(low1, high1)
            message = ""
            try:
                int(hex(b).upper().split('X')[-1])
            except Exception:
                message = "Not a valid value for decimal number system"
            self.set_mem(a, b)
            try:
                alert = self.driver.switch_to.alert
                alert_message = alert.text
                alert.accept()
                self.assertEqual(message, alert_message)
            except Exception:
                loc_val = self.get_by_name(hex(a).upper().split('X')[-1])
                val = loc_val.get_attribute('value')
                self.assertEqual(val, hex(b).upper().split('X')[-1])
                self.assertEqual(message, "")

        self.close_page()


if __name__ == '__main__':
    main()
