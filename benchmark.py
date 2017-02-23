import os,sys
from terminology import read_term, normId

def benchmark(infile, terminology):
	dataset = open(infile,'r').read().split("===========================\n")
	qa_set = []
	no_postive=0
	summ = 0
	right = 0

	Id_dict = read_term(terminology)

	for x, data in enumerate(dataset):
		if data.strip() == '':
			continue
		item_set = data.strip().split('\n')

		query = ''
		pos_set, neg_set = [],[]
		repeat_list = []

		for y, item in enumerate(item_set):
			if item in repeat_list:
				continue
			else:
				repeat_list.append(item)
			try:
				query , question, query_id, ques_id, sieve, fname, index =  item.split('\t')
				query_id = normId( query_id, Id_dict)
				ques_id  = normId( ques_id  , Id_dict)
				if query_id == ques_id:
					label = 1
					break
				elif query_id in ques_id:
					label = 2
					break
				else:
					label = 0 

			except:
				print "Error Parser :" + item
				continue	
		if label == 1:
			summ  +=1
			right += 1
		elif label == 2:
			summ += 1
			right += 0.5
		else :
			no_postive += 1
			summ += 1
	print summ, right,no_postive
	print float(right)/summ

if __name__ == '__main__':
	benchmark(sys.argv[1], sys.argv[2])
