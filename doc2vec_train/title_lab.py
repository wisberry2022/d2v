from model_train import *

def text_slice(documents:list): # db에서 꺼낸 기사 데이터 정제 -> [' 기사본문 ', ' 기사본문 ', ... ' 기사본문 ']의 형태
	cn = Cleaning_Noise()
	result = []
	for docu in documents:
		clean_data = cn.cleaning(docu[0].strip('\n'))
		result.append(clean_data)	
	return result

def train_set(db_names:list, section:str):
	train_set = []
	titles = select_title(db_names, section)
	train_set += titles 
	return train_set

def new_data_input(titles, string_data:str, model, rank):
	new_data = tokenized_mecab(string_data)
	predict_vector = model.infer_vector(new_data)
	result = model.dv.most_similar([predict_vector], topn=rank)
	index, value = result[0][0], result[0][1]
	print(index, value, '기존:',titles[index], '입력:',string_data)

section_list = ['politics','economy','society','life','world','it']

db_list = [file_name for file_name in os.listdir(os.getcwd()) if file_name.endswith(".db")]

lab_data = []
for section in section_list:
	temp = train_set(db_list[0], section)
	lab_data += temp

titles = text_slice(lab_data)
print(len(titles))
input_data = []
for section in section_list:
	temp = train_set(db_list[1], section)
	input_data += temp

input_title = text_slice(input_data)
print(len(input_title))

for input in input_title:
	new_data_input(titles, input, model, 3)