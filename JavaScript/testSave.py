from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

def getById(id):
    return mydriver.find_element_by_id(id)

def getByXPath(value):
    return mydriver.find_element_by_xpath(value)

mydriver = webdriver.Chrome()
mydriver.get('http://www.emu86.org/')
getById('subButton').click();
getById('sample').click()
getByXPath('//*[@id="sample"]/option[13]').click()
getById('save-button').click()
save_prompt = mydriver.switch_to.alert;
save_prompt.send_keys("power.hello");
save_prompt.accept();
try:
    mydriver.switch_to.alert.accept();
    print("Alert raised!")
except:
    print("Valid file name")
mydriver.close()
