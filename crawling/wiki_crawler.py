from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from collections import namedtuple
from bs4 import BeautifulSoup
import selenium.webdriver
import datetime
import sqlite3
import requests
import time

id = 1
options = webdriver.ChromeOptions()
#options.add_argument("headless")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

def make_author_list():
	driver = webdriver.Chrome(options=options)
	url = 'https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%EC%9D%98_%EC%86%8C%EC%84%A4%EA%B0%80_%EB%AA%A9%EB%A1%9D'
	driver.get(url)
	result = ''
	for idx in range(1,9):
		text = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div[1]/ul[{idx}]').text
		result += text
	author_list = [author for author in result.split('\n') if len(author) <= 3]
	return driver, author_list

def db_creater(section):
	name = f'{section}_{datetime.datetime.now().strftime("%m%d_%H%M")}'
	db = sqlite3.connect(f'{name}.db')
	curs = db.cursor()
	curs.execute('CREATE TABLE wiki (id, section, title, content)')
	return db, curs

def tuple_to_db(curs, db, tuple):
	sql = f'INSERT INTO wiki (id, section, title, content) values(?,?,?,?)'
	curs.execute(sql, [tuple[0], tuple[1], tuple[2], tuple[3]])
	db.commit()
		
def crawling(name_list, driver, db, curs):
	now = time.localtime().tm_hour
	global id
	result = namedtuple('wiki', ['id', 'section', 'title', 'content'])
	try:
		for name in name_list:
			url = 'https://ko.wikipedia.org/wiki/'
			n_url = url + name
			driver.get(n_url)
			text = ''
			for idx in range(1,5):
				try:
					content = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div[1]/p[{idx}]').text	
					text += content
				except:
					pass
			_wiki = result(id, 'wiki', name, text)
			tuple_to_db(curs, db, _wiki)
			id += 1
	except:
		pass
		

driver, author_list = make_author_list()
print(author_list)
db, curs = db_creater('wiki')
crawling(author_list, driver, db, curs)

