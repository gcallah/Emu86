from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

mydriver = webdriver.Chrome()

def getById(id):
    return mydriver.find_element_by_id(id)

def getByXPath(value):
    return mydriver.find_element_by_xpath(value)

def getLink(linkText):
    return mydriver.find_element_by_link_text(linkText)

mydriver.get('http://www.emu86.org/');
getByXPath('//*[@id="user-tools"]/a[2]').click()
getByXPath('//*[@id="content-main"]/div/details[2]/summary').click()
getByXPath('//*[@id="content-main"]/div/details[2]/details[1]/summary').click()
getByXPath('//*[@id="content-main"]/div/details[2]/details[1]/ul/li[14]/a').click()
assert mydriver.current_url == 'https://github.com/gcallah/Emu86/blob/master/tests/Intel/power.asm'

