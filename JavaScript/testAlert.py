from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

mydriver = webdriver.Chrome()
mydriver.get('http://www.emu86.org/')
validInputBool = True 

def getById(id):
    return mydriver.find_element_by_id(id)

def enterInputs(inputBox, value):
    inputBox.send_keys(value)

alertPopUp = True;
getById('subButton').click()
inputBox = getById('memText')
enterInputs(inputBox, '104')
inputVal = getById('valueText');
enterInputs(inputVal, 'BC');
validInputBool = False;
getById('setMem').click();
try:
	mydriver.switch_to.alert.accept();
	print("Alert raised!")
except:
	print("Valid input")
mydriver.close()