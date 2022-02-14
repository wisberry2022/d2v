from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from collections import namedtuple
from bs4 import BeautifulSoup
import selenium.webdriver
import schedule
import datetime
import sqlite3
import requests
import time

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

def driver_initialize():
	driver = webdriver.Chrome(options=options)
	url = 'https://news.naver.com'
	driver.get(url)
	return driver

def db_creater(section):
	name = f'{section}_{datetime.datetime.now().strftime("%m%d_%H%M")}'
	db = sqlite3.connect(f'{name}.db')
	curs = db.cursor()
	curs.execute('CREATE TABLE article (id, section, title, content)')
	return db, curs

def checking_duplicate(curs, title):
	sql = 'SELECT title FROM article WHERE title == ?'
	result = curs.execute(sql, [title])
	if (not result.fetchone()):
		return 1
	else:
		return 0

def tuple_to_db(curs, db, tuple):
	sql = f'INSERT INTO article (id, section, title, content) values(?,?,?,?)'
	curs.execute(sql, [tuple[0], tuple[1], tuple[2], tuple[3]])
	db.commit()
		
def crawling(section_list, driver, db, curs):
	now = time.localtime().tm_hour
	id = 1
	result = namedtuple('article', ['id', 'section', 'title', 'content'])
	while time.localtime().tm_hour < 23:
		try:
			for section in section_list:
				for idx in range(1,6):
					driver.find_element_by_xpath(f'//*[@id="section_{section}"]/div[2]/div/ul/li[{idx}]/a').click()
					title = driver.find_element_by_id('articleTitle').text
					content = driver.find_element_by_class_name('_article_body_contents').text	
					content = content.rstrip('\n')
					if checking_duplicate(curs, title):
						print(id)
						_article = result(id, section, title, content)
						tuple_to_db(curs, db, _article)
						driver.find_element_by_xpath('//*[@id="lnb"]/ul/li[1]/a').click()
						id += 1
					else:
						driver.find_element_by_xpath('//*[@id="lnb"]/ul/li[1]/a').click()
		except:
			driver.find_element_by_xpath(f'//*[@id="lnb"]/ul/li[1]/a').click()
		
def crawl():
	section_list = ['politics','economy','society','life','world','it']
	driver = driver_initialize()
	db, curs = db_creater('all')
	crawling(section_list, driver, db, curs)

crawl()

#schedule.every().day.at("08:58").do(crawl)

#while True:
#	schedule.run_pending()
	