import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from db_controller import *
from konlpy.tag import Okt, Kkma, Mecab
from preprocess import *

mc = Mecab(dicpath='C:\mecab\mecab-ko-dic')

def write_out(titles:list):
	with open('data_list.txt', 'a', encoding='utf-8') as file:
		for idx, title in enumerate(titles):
			file.write(str(idx) + '\t' + title + '\n')

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


titles = select_title('all_0831_1546.db', 'politics')
titles = text_slice(titles)
write_out(titles)
titles = [tokenized_mecab(title) for title in titles]
titles = gensim_tagged(titles)

model = Doc2Vec(vector_size = 50, min_count=1, epochs=10)
model.build_vocab(titles)

model.train(titles, total_examples=model.corpus_count, epochs=model.epochs)

string = "이준석이 윤석열 홍준표 2강에게 '경고 한 장씩 준다'한 까닭은"
test_string = tokenized_mecab(string)
print(test_string)

predict_vector = model.infer_vector(test_string)
print(model.dv.most_similar([predict_vector], topn=15))