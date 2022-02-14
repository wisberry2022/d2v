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

def write_out(file_name, titles:list):
	with open(f'{file_name}', 'a', encoding='utf-8') as file:
		for title in titles:
			file.write(title + '\n')

def text_slice_one(document):
	cn = Cleaning_Noise()
	clean_data = cn.cleaning(document.strip('\n'))
	return clean_data

def read_data(file_name):
	with open(f'{file_name}', 'r', encoding='utf-8') as file:
		data_set = []
		while True:
			data = file.readline()
			data_set.append(data.strip('\n'))
			if not data:
				return data_set

def compare_same(data_set, data_set2):
	if (len(data_set) != len(data_set2)):
		print("both datas has not same length!")
	else:
		if data_set == data_set2:
			print("same")
		else:
			print("not same")

db_list = [file_name for file_name in os.listdir(os.getcwd()) if file_name.endswith(".db")]

print(db_list)

section_list = ['politics', 'economy', 'society','life','world','it']

input_data = read_data('input_article.txt')
output_data = read_data('output_article.txt')

input_set = []
for section in section_list:
	temp = select_title_section(db_list[0], section)
	input_set += temp

input_sections = [data[0] for data in input_set]
input_set = [data[1] for data in input_set]

#write_out("input_articles_section.txt", input_sections)

output_set = []
for db_name in db_list[1:]:
	for section in section_list:
		temp = select_title_section(db_name, section)
		output_set += temp

print(output_set)

output_set2 = []
for idx in range(0, len(output_data)):
	for section, contents in output_set:
		if output_data[idx] == contents:
			print(idx, contents)
			output_set2.append(contents)
			print(len(output_set2))

#compare_same(output_data, output_set2)
