import sqlite3

def select_text(db_name, section, id=False, title=False):
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

def select_title(db_name, section):
	db = sqlite3.connect(f'{db_name}')
	curs = db.cursor()
	sql = f'SELECT title FROM article WHERE section == ?'
	result = curs.execute(sql, [section]).fetchall()
	return result


result1 = select_text('all_0831_1546.db','it', True)
result2 = select_text('all_0831_1546.db', 'it', True, True)
result3 = select_title('all_0831_1546.db', 'it')

#print(result1)
print(result3)