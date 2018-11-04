import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from unittest import TestCase, main
NUM_TESTS = 10

driver = webdriver.Chrome()

class TestMemory(TestCase):

    def load_page(self):
        driver.get('http://www.emu86.org/')

    def close_page(self):
        driver.quit()

    def getById(self, id):
        return driver.find_element_by_id(id)

    def enterInputs(self, inputBox, value):
        inputBox.send_keys(value)

    def set_Mem(self, loc, val):
        self.getById('subButton').click()
        inputBox = self.getById('memText')
        self.enterInputs(inputBox, hex(loc).upper().split('X')[-1])
        inputVal = self.getById('valueText')
        self.enterInputs(inputVal, hex(val).upper().split('X')[-1])
        self.getById('setMem').click()

    def test_mem(self, low1 = 0, high1=16):
        for i in range(0, NUM_TESTS):
            self.load_page()
            a = random.randint(low1, high1)
            b = random.randint(low1, high1)
            validInput = True
            try:
                int_form = int(hex(b).upper().split('X')[-1])
            except:
                validInput = False
            self.set_Mem(a, b)
            try:
                driver.switch_to.alert.accept();
                if validInput:
                    print("Valid Input: " + "Alert raised!")
                else:
                    print("Invalid Input: " + "OK!")
            except:
                test_string = "Alert not raised!"
                if validInput:
                    print("Valid Input: " + "OK!")
                else:
                    print("Invalid Input: " + "Alert raised!")

        self.close_page()

if __name__ == '__main__':
    main()