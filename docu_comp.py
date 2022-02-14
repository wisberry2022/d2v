from db_controller import *
from preprocess import Cleaning_Noise
from konlpy.tag import Okt, Kkma
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from DTM import *
import random

kkma = Kkma()

def text_slice(documents:list):
	cn = Cleaning_Noise()
	result = []
	for docu in documents:
		clean_data = cn.cleaning(docu[0].strip('\n'))
		result.append(clean_data)	
	return result
		
politics = select_article('all_0831_1546.db', 'politics')
politics = text_slice(politics)

tf_idf = TF_IDF_FUNCTION()
dtm_matrix = tf_idf.dtm(politics[54:56])
ti_matrix = tf_idf.tf_idf(dtm_matrix)
tf_idf.docu_sim(ti_matrix)

word_index = tf_idf.get_word_index()
print(word_index)


#print(politics[54] + '\n')
#print(politics[55] + '\n')
