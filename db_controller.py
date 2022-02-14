import sqlite3
from konlpy.tag import Okt

okt = Okt()

def select_article(db_name, section, id=False, title=False):
	db = sqlite3.connect(f'{db_name}')
	curs = db.cursor()
	if (id):
		if (title):
			sql = f'SELECT id, title, content FROM article WHERE section == ?'
			result = curs.execute(sql, [section]).fetchall()
			return result
		sql = f'SELECT id, content FROM article WHERE section == ?'
		result = curs.execute(sql, [section]).fetchall()
		return result
	else:
		sql = f'SELECT content FROM article WHERE section == ?'
		result = curs.execute(sql, [section]).fetchall()
		return result

def select_title(db_name, section):
	db = sqlite3.connect(f'{db_name}')
	curs = db.cursor()
	sql = f'SELECT title FROM article WHERE section == ?'
	result = curs.execute(sql, [section]).fetchall()
	return result


def select_article_by_keyword(db_name, section, keyword):
	db = sqlite3.connect(db_name)
	curs = db.cursor()
	sql = f'SELECT title FROM article WHERE section == ?'
	titles = curs.execute(sql, [section]).fetchall()
	titles = [title[0] for title in titles if keyword in okt.morphs(title[0])]
	sql = f'SELECT content FROM article WHERE title == ?'
	result = []
	for title in titles:
		content = curs.execute(sql, [title]).fetchall()
		result.append(content[0][0])
	return result