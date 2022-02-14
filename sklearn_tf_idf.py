from sklearn.feature_extraction.text import TfidfVectorizer
from DTM import *
from preprocess import *
from db_controller import *
from konlpy.tag import Okt, Kkma
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

def text_slice(documents:list): # db에서 꺼낸 기사 데이터 정제 -> [' 기사본문 ', ' 기사본문 ', ... ' 기사본문 ']의 형태
	cn = Cleaning_Noise()
	result = []
	for docu in documents:
		clean_data = cn.cleaning(docu[0].strip('\n'))
		result.append(clean_data)	
	return result

def compare_same_section(db_name:str, documents:list, section:str): # 동일 섹션 내 기사 비교
	with open(f'{db_name}_{section}.txt', 'a') as file:
		tf_idf = TF_IDF_FUNCTION()
		tfidfv = TfidfVectorizer().fit(documents)
		ti_matrix = tfidfv.transform(documents).toarray()
		num_set = list(range(len(documents)))
		for a in num_set:
			if a == num_set[-1]:break
			for b in num_set[a+1:]:	
				data = [ti_matrix[a], ti_matrix[b]]
				value = tf_idf.cos_sim(data)
				if value >= 0.001:
					file.write(f'{documents[a]} / {documents[b]} 유사도 : {value}' + '\n')
				else:
					pass

def compare_diff_section(db_name:str, sc1:str, sc2:str, sc1_docu, sc2_docu):   # 다른 섹션 내 기사 비교
	with open(f'{db_name}_{sc1}_{sc2}.txt','a') as file:
		tf_idf = TF_IDF_FUNCTION()
		sc1_tf_idf = TfidfVectorizer().fit(sc1_docu)
		sc2_tf_idf = TfidfVectorizer().fit(sc2_docu)
		sc1_ti_matrix = sc1_tf_idf.transform(sc1_docu).toarray()
		sc2_ti_matrix = sc2_tf_idf.transform(sc2_docu).toarray()
		if len(sc1_docu) > len(sc2_docu):
			sc1_num_set, sc2_num_set = list(range(len(sc1_docu))), list(range(len(sc2_docu)))
			for sc2_idx in sc2_num_set:
				for sc1_idx in sc1_num_set[sc2_idx+1:]:
					data = [sc2_ti_matrix[sc2_idx], sc1_ti_matrix[sc1_idx]]
					value = tf_idf.cos_sim(data)
					if value >= 0.0:
						file.write(f'{sc2_docu[sc2_idx]} / {sc1_docu[sc1_idx]} 유사도 : {value}' + '\n')
					else:
						pass
		else:
			sc1_num_set, sc2_num_set = list(range(len(sc1_docu))), list(range(len(sc2_docu)))
			for sc1_idx in sc1_num_set:
				for sc2_idx in sc2_num_set[sc1_idx+1:]:
					data = [sc1_ti_matrix[sc1_idx], sc2_ti_matrix[sc2_idx]]
					value = tf_idf.cos_sim(data)
					if value >= 0.0:
						file.write(f'{sc1_docu[sc1_idx]} / {sc2_docu[sc2_idx]} 유사도 : {value}' + '\n')
					else:
						pass
		
def same_section_lab(db_names:list, section_list):
	for db_name in db_names:
		for section in section_list:
			data = select_title(db_name, section)
			data = text_slice(data)
			compare_same_section(db_name, data, section)

def diff_section_lab(db_names:list, section_list):
	num_set = list(range(len(section_list)))
	for db_name in db_names:
		for sc1 in num_set:
			if sc1 == num_set[-1]:break
			for sc2 in num_set[sc1+1:]:
				data1 = select_title(db_name, section_list[sc1])
				data2 = select_title(db_name, section_list[sc2])
				data1 = text_slice(data1)
				data2 = text_slice(data2)
#				print(f'{section_list[sc1]}_data1:', data1[:3])
#				print(f'{section_list[sc2]}_data2:', data2[:3])
				compare_diff_section(db_name, section_list[sc1], section_list[sc2], data1, data2)
				

db_names = ['all_0831_1546.db']
section_list = ['politics','society','economy','world','life','it']

diff_section_lab(db_names, section_list)
#same_section_lab(db_names, section_list)