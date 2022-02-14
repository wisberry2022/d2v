from konlpy.tag import Okt, Kkma
import numpy as np
import copy
import re

class Cleaning_Noise(object):
	def __init__(self):
		pass

	def cleaning(self, corpus):
		result = re.sub('["0-9a-zA-Zㄱ-ㅎㅏ-ㅣ~!@#$%~&-_=\\n\.\'\$\(\)\*\+\?\[\\\^\{\`♥␞]', '', corpus)
		return result

	def clean_noise_file(self, read_file, write_file):
		with open(f'{read_file}','r',encoding='utf-8') as file, open(f'{write_file}', 'a', encoding='utf-8') as file2:
			while True:
				raw = file.readline()
				if (not raw):
					break
				result = self.cleaning(raw)
				file2.write(result)

	def clean_noise_data(self, tokenized_data):
		result = []
		for sentence in tokenized_data:
			result.append(self.cleaning(sentence))
		return result
		

class Stopwords(object):
	def __init__(self):
		self.stopwords_set={}

	def loader(self, file_name): # 불용어 사전 로더
		with open(f'{file_name}', 'r', encoding='utf-8') as file:
			data = file.readlines()
			for num in range(0,len(data)):
				corpus = data[num].rstrip('\n').split('\t')
				self.stopwords_set[corpus[0]] = corpus[1]
			return self.stopwords_set

class VocaSet(object):
	def __init__(self):
		self.voca_set = {}
		self.okt = Okt()

	def get_voca(self):
		return self.voca_set

	def make(self, file_name, stopwords_set): # 단어 집합 생성
		with open(f'{file_name}','r',encoding='utf-8') as file:
			while True:
				data = file.readline()
				if not data:
					break
				corpus = data.rstrip('\n')
				sent = self.okt.morphs( str(corpus) )
				for i in range(0, len(sent)):
					if ( len(sent[i]) > 1 ):
						if sent[i] not in stopwords_set.keys():
							if sent[i] not in self.voca_set:   # 단어 집합의 키 : 단어, 값 : 등장횟수
								self.voca_set[sent[i]] = 1
							self.voca_set[sent[i]] += 1

	def sorting(self): # 단어 집합 빈도수 기준 정렬
		sorted_vocab = sorted(self.voca_set.items(), key=lambda x:x[1], reverse=True)
		self.voca_set.clear()
		for (word, freq) in sorted_vocab:
			self.voca_set[word] = freq

	def indexing(self): # 높은 빈도수를 가진 어휘부터 차례대로 넘버링 진행
		i=1
		voca_set = copy.deepcopy(self.voca_set)
		self.voca_set.clear()
		for word in voca_set.keys():
			self.voca_set[word] = i
			i += 1

	def select_ranked(self, vocab_size): # 단어 집합 Size 축소
		new_sort = [w for w,c in self.voca_set.items() if c > vocab_size]
		for words in new_sort:
			del self.voca_set[words]

	def save_to_text(self, file_name): # 단어집합의 단어와 품사, 빈도 수를 텍스트 파일로 출력
		with open(f'{file_name}', 'a', encoding='utf-8') as file:
			for word,freq in self.voca_set.items():
				text = word + '\t' +  self.okt.pos(word)[0][1] + '\t' + str(freq) + '\n'
				file.write(text)
			print('save success!')

class Encoding(object):
	def __init__(self, voca_set):
		self.int_list = []
		self.voca_set = voca_set
		self.okt = Okt()

	def get_integer_list(self):
		return self.int_list

	def integer_encoding(self, file_name, stopwords_set):
		with open(f'{file_name}', 'r', encoding='utf-8') as file:
			while True:
				sent = file.readline()
				if not sent:
					break
				data = sent.rstrip('\n')
				analysis = self.okt.morphs(data)
				mid_list=[]
				for i in range(0, len(analysis)):
					if analysis[i] not in stopwords_set.keys():
						if analysis[i] not in mid_list:
							if analysis[i] in self.voca_set.keys():
								mid_list.append( self.voca_set[analysis[i]] )
							elif analysis[i] not in self.voca_set.keys():
								mid_list.append( -1 )
							else:
								pass
				self.int_list.append(mid_list)

	def integer_encoding_removed_OOV(self, file_name, stopwords_set):
		with open(f'{file_name}', 'r', encoding='utf-8') as file:
			while True:
				sent = file.readline()
				if not sent:
					break
				data = sent.rstrip('\n')
				analysis = self.okt.morphs(data)
				mid_list=[]
				for i in range(0, len(analysis)):
					if analysis[i] not in stopwords_set.keys():
						if analysis[i] not in mid_list:
							if analysis[i] in self.voca_set.keys():
								mid_list.append( self.voca_set[analysis[i]] )
							else:
								pass
				self.int_list.append(mid_list)

	def save_to_text(self, file_name):  # 사용자가 원하는 리스트를 텍스트 파일로 반환 
		with open(f'{file_name}', 'a', encoding='utf-8') as file:
			for i in range(0, len(self.int_list)):
				for j in range(0, len(self.int_list[i])):
					if(j == len(self.int_list[i])-1):
						file.write(str(self.int_list[i][j]) + '\n')
					else:
						file.write(str(self.int_list[i][j]) + ' ')					