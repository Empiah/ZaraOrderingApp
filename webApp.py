from selenium import webdriver
import re

driver = webdriver.Chrome()
driver.maximize_window()
url_home = 'https://www.zara.com/uk/'
url_booking = 'https://www.zara.com/uk/en/knotted-wrap-skirt-p02975878.html?v1=47358279&v2=1445670'

driver.get(url_home)
