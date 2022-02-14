from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from collections import namedtuple
import selenium.webdriver
import datetime
import sqlite3
import requests
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)
url = 'https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%EC%9D%98_%EC%86%8C%EC%84%A4%EA%B0%80_%EB%AA%A9%EB%A1%9D'
driver.get(url)
driver.implicitly_wait(5)

result = ''

for idx in range(1,9):
	text = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div[1]/ul[{idx}]').text
	result += text
	
content = result.split('\n')
content = [x for x in content if len(x) <= 3]
print(content)