import DTM as dtm
import loader as ld
import pickle
from dos import *
from preprocess import Cleaning_Noise

# 필요한 데이터 불러오기
loader = ld.Load()
train = loader.document_load('test_data_cleaning_mask')
stopwords_set = list(dict.keys(loader.stopwords_loader('stopwords_dic.txt')))

with open('politics_data.pickle', 'rb') as file:
	politics = pickle.load(file)

with open('society_data.pickle', 'rb') as file:
	society = pickle.load(file)

with open('world_data.pickle', 'rb') as file:
	world = pickle.load(file)


# 결측값 제거
movie = [comment for comment in train if comment != '']
politics = [comment for comment in politics if comment != '']
society = [comment for comment in society if comment != '']
world = [comment for comment in world if comment != '']

''' 
cn = Cleaning_Noise()
movie = cn.clean_noise_data(movie)
politics = cn.clean_noise_data(politics)
society = cn.clean_noise_data(society)
world = cn.clean_noise_data(world)

base_docu = politics[:5000]
p_train = politics[5000:10000]
p_train1 = politics[5000:15000]
s_train = society[:5000]
w_train = world[:2000]
m_train = movie[:5000]

base_dtm, word_index = dtm.make_base_dtm(base_docu, stopwords_set, 10)
p_dtm = dtm.calc_dtm(p_train, stopwords_set, base_dtm)
p_dtm2 = dtm.calc_dtm(p_train1, stopwords_set, base_dtm)
s_dtm = dtm.calc_dtm(s_train, stopwords_set, base_dtm)
w_dtm = dtm.calc_dtm(w_train, stopwords_set, base_dtm)
m_dtm = dtm.calc_dtm(m_train, stopwords_set, base_dtm)

matrix = dtm.dtm_matrix(p_dtm, p_dtm2, s_dtm, w_dtm, m_dtm)
tf_matrix_w = dtm.tf_idf(matrix, word_index)
tf_matrix2 = dtm.tf_idf(matrix)
print(tf_matrix_w)
print(tf_matrix2)

print(cos_sim(tf_matrix2[0], tf_matrix2[1]))
print(cos_sim(tf_matrix2[1], tf_matrix2[2]))
print(cos_sim(tf_matrix2[2], tf_matrix2[3]))

print(cos_sim(tf_matrix2[0], tf_matrix2[4]))
print(cos_sim(tf_matrix2[2], tf_matrix2[4]))
print(cos_sim(tf_matrix2[3], tf_matrix2[4]))
'''