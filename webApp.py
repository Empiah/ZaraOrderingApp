
from selenium import webdriver
import re

driver = webdriver.Chrome(executable_path='/Users/ophipps/Documents/Apps/chromedriver')
driver.maximize_window()
url_home = 'https://www.zara.com/uk/'
url_booking = 'https://www.zara.com/uk/en/knotted-wrap-skirt-p02975878.html?v1=47358279&v2=1445670'

driver.get(url_home)


"""
import time
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/Users/ophipps/Documents/Apps/chromedriver')
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
"""