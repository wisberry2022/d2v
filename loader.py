from konlpy.tag import Okt

class Load(object):
	def __init__(self):
		self.stopwords_set = {}
		self.voca_set = {}
		self.word_list = []
		self.integer_list = []
		self.comment_list = []

	def document_load(self, file_name):
		with open(f'{file_name}.txt', 'r', encoding='utf-8') as file:
			while True:
				data = file.readline()
				self.comment_list.append(data.rstrip('\n'))
				if not data: return self.comment_list

	def stopwords_loader(self, file_name): # 불용어 사전 로더
		with open(f'{file_name}', 'r', encoding='utf-8') as file:
			data = file.readlines()
			for num in range(0,len(data)):
				corpus = data[num].rstrip('\n').split('\t')
				self.stopwords_set[corpus[0]] = corpus[1]
			return self.stopwords_set

	def voca_loader(self, file_name):
		with open(f'{file_name}', 'r', encoding='utf-8') as file:
			data = file.readlines()
			for x in data:
				y = x.rstrip('\n').split('\t')
				self.voca_set[y[0]] = y[2]
			return self.voca_set

	def word_list_loader(self, file_name):
		okt = Okt()
		with open(f'{file_name}', 'r', encoding='utf-8') as file:
			while True:
				data = file.readline()
				if not data:
					return 
				data2 = data.rstrip('\n')
				sent = okt.morphs(data2)
				self.word_list.append(' '.join(sent))

	def integer_list_loader(self, file_name):
		with open(f'{file_name}', 'r', encoding='utf-8') as file:
			data = file.readlines()
			for x in data:
				int_sent = x.split(' ')
				result = list(map(int, int_sent))
				self.integer_list.append(result)
			return self.integer_list