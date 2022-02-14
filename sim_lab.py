from sklearn.feature_extraction.text import CountVectorizer
from DTM import *
from db_controller import *
from konlpy.tag import Okt, Kkma
import sys

def text_slice(documents:list): # db에서 꺼낸 기사 데이터 정제 -> [' 기사본문 ', ' 기사본문 ', ... ' 기사본문 ']의 형태
	cn = Cleaning_Noise()
	result = []
	for docu in documents:
		clean_data = cn.cleaning(docu[0].strip('\n'))
		result.append(clean_data)	
	return result

def compare_same_section(db_name:str, section:str, documents:list, title_set:list): # 동일 섹션 내 기사 비교
	with open(f'{db_name}_{section}.txt', 'a', encoding='utf-8') as file:
		tf_idf = TF_IDF_FUNCTION()
		num_set = list(range(len(documents)))
		for a in num_set:
			if a == num_set[-1]:break
			for b in num_set[a+1:]:	
				data = [documents[a], documents[b]]
				dtm_matrix = tf_idf.dtm(data)
				ti_matrix = tf_idf.tf_idf(dtm_matrix)
				value = tf_idf.cos_sim(ti_matrix)
				file.write(f'{title_set[a][0]} / {title_set[b][0]} 유사도 : {value}' + '\n')

def compare_diff_section(db_name, sc1, sc2, sc1_docu, sc2_docu, sc1_title, sc2_title):   # 다른 섹션 내 기사 비교
	with open(f'{db_name}_{sc1}_{sc2}.txt', 'a', encoding='utf-8') as file:
		tf_idf = TF_IDF_FUNCTION()
		if len(sc1_docu) > len(sc2_docu):
			sc1_num_set, sc2_num_set = list(range(len(sc1_docu))), list(range(len(sc2_docu)))
			for sc2_idx in sc2_num_set:
				for sc1_idx in sc1_num_set[sc2_idx+1:]:
					lab_data = [sc2_docu[sc2_idx], sc1_docu[sc1_idx]]
					dtm_matrix = tf_idf.dtm(lab_data)
					ti_matrix = tf_idf.tf_idf(dtm_matrix)
					value = tf_idf.cos_sim(ti_matrix)
					file.write(f'{sc2_title[sc2_idx]} / {sc1_title[sc1_idx]} 유사도 : {value}' + '\n')
		else:
			sc1_num_set, sc2_num_set = list(range(len(sc1_docu))), list(range(len(sc2_docu)))
			for sc1_idx in sc1_num_set:
				for sc2_idx in sc2_num_set[sc1_idx+1:]:
					lab_data = [sc1_docu[sc1_idx], sc2_docu[sc2_idx]]
					dtm_matrix = tf_idf.dtm(lab_data)
					ti_matrix = tf_idf.tf_idf(dtm_matrix)
					value = tf_idf.cos_sim(ti_matrix)
					file.write(f'{sc1_title[sc1_idx]} / {sc2_title[sc2_idx]} 유사도 : {value}' + '\n')
		
def same_section_lab(db_names:list, section_list):
	for db_name in db_names:
		for section in section_list:
			title_set = select_title(db_name, section)
			data = select_article(db_name, section)
			data = text_slice(data)
			compare_same_section(db_name, section, data, title_set)

def diff_section_lab(db_names:list, section_list):
	num_set = list(range(len(section_list)))
	for db_name in db_names:
		for sc1 in num_set:
			if sc1 == num_set[-1]:break
			for sc2 in num_set[sc1+1:]:
				data1_title = select_title(db_name, section_list[sc1])
				data2_title = select_title(db_name, section_list[sc2])
				data1_title = text_slice(data1_title)
				data2_title = text_slice(data2_title)
				data1 = select_article(db_name, section_list[sc1])
				data2 = select_article(db_name, section_list[sc2])
				data1 = text_slice(data1)
				data2 = text_slice(data2)
				compare_diff_section(db_name, section_list[sc1], section_list[sc2], data1, data2, data1_title, data2_title)

db_names = ['all_0831_1546.db']
section_list = ['politics','society','economy','world','life','it']

#same_section_lab(db_names, section_list)
diff_section_lab(db_names, section_list)