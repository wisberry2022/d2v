import re
import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from db_controller import *
from konlpy.tag import Okt, Kkma, Mecab
from preprocess import *

mc = Mecab(dicpath='C:\mecab\mecab-ko-dic')

def train_set(db_name:str, section:str):
	train_set = []
	titles = select_title(db_name, section)
	train_set += titles 
	return train_set

def data_to_dict(titles:list):
	dict = {}
	for idx, title in enumerate(titles):
		dict[idx] = title
	return dict

def write_out(titles:list):
	with open('data_list.txt', 'a', encoding='utf-8') as file:
		for idx, title in enumerate(titles):
			file.write(str(idx) + '\t' + title + '\n')

def text_slice_one(document):
	cn = Cleaning_Noise()
	clean_data = cn.cleaning(document.strip('\n'))
	return clean_data

def text_slice(documents:list): # db에서 꺼낸 기사 데이터 정제 -> [' 기사본문 ', ' 기사본문 ', ... ' 기사본문 ']의 형태
	cn = Cleaning_Noise()
	result = []
	for docu in documents:
		clean_data = cn.cleaning(docu[0].strip('\n'))
		result.append(clean_data)	
	return result

def tokenized_mecab(sentence, add_tags=False):
	new = []
	for word, tag in mc.pos(sentence):
		if (add_tags):
			if len(word) > 1:
				regex = re.compile('[가-힣]+').findall(word)
				if len(regex) >= 1:
					new.append('/'.join((regex[0], tag)))
		else:
			if len(word) > 1:
				regex = re.compile('[가-힣]+').findall(word)
				if len(regex) >= 1:
					new.append(regex[0])
	return new

def gensim_tagged(tokenized_docu:list):
	tagged = [TaggedDocument(words=data, tags=[idx]) for idx, data in enumerate(tokenized_docu)]
	return tagged

def train_model(data:list, vector_size, min_count, epochs, window, alpha, min_alpha):
	model = Doc2Vec(vector_size = vector_size, min_count = min_count, window=window, alpha = alpha, min_alpha = min_alpha, epochs = epochs)
	model.build_vocab(data)
	model.train(data, total_examples=model.corpus_count, epochs=model.epochs)
	return model

def new_data_input(titles, string_data:str, model, rank):
	with open('result.txt', 'a', encoding='utf-8') as file:
		new_data = text_slice_one(string_data[0])
		new_data = tokenized_mecab(new_data)
		predict_vector = model.infer_vector(new_data)
		result = model.dv.most_similar([predict_vector], topn=rank)
		index, value = result[0][0], result[0][1]
		file.write(string_data[0] + '\t' + titles[index] + '\t' + str(value) + '\n')

db_list = [file_name for file_name in os.listdir(os.getcwd()) if file_name.endswith(".db")]

section_list = ['politics', 'economy', 'society','life','world','it']

train_data = []
for db_name in db_list[1:]:
	for section in section_list:
		temp = train_set(db_name, section)
		train_data += temp

out_train_data = [article[0] for article in train_data]

train_titles = text_slice(train_data)
train_sets = [tokenized_mecab(title) for title in train_titles]
train_sets = gensim_tagged(train_sets)

model = train_model(train_sets, 30, 2, 40, 2, 0.015, 0.01)

test_data = []
for section in section_list:
	temp = train_set(db_list[0], section)
	test_data += temp

for input in test_data:
	new_data_input(out_train_data, input, model, 3)

name = 'test_model_16th'
model.save(name)

# 학습률을 크게 잡으니 유사도 결과값이 낮아지는 현상 발견 
# alpha와 min_alpha의 차가 0.02를 넘으면 유사도 결과값이 눈에 띄게 낮아짐