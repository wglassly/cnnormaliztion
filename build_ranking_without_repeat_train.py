import os,sys
import string
from dictionary import dictionary
from terminology import read_term, normId, read_id2term


def expan_set(item_set,id2term):
	exp = []
	for y, item in enumerate(item_set):
		q , a, q_id, a_id, sieve, fname, index =  item.split('\t')
		terms = id2term[a_id] if a_id in id2term else [a]
		exp += [ "\t".join([q,a_new,q_id, a_id, sieve, fname,index]) for a_new in terms ]
	return exp		

def g_file(infile,save_file,terminology, dev_size=900):
	dataset = open(infile,'r').read().split("===========================\n")
	qa_set = []
	index_set = []
	no_postive=0
	Id_dict = read_term(terminology)
	id2term = read_id2term(terminology)
	no_query_repeat_train = []
	for x, data in enumerate(dataset):
		if data.strip() == '':
			continue
		item_set = data.strip().split('\n')
		
		if len(set(item_set)) == 1:
			continue
		query = ''
		pos_set, neg_set = [],[]
		repeat_list = []
		'''if dev_size > 0:
			a = len(item_set)
			item_set = expan_set(item_set,id2term)
			'''
		#print a, len(item_set)
		#print len(item_set)
		for y, item in enumerate(item_set):
			try:
				#label , query , question, ques_id, query_id =  item.split('\t')
				q , a, q_id, a_id, sieve, fname, index =  item.split('\t')
				if a in repeat_list:
					continue
				else:
					repeat_list.append(a)
				
				if dev_size > 0:
					if q in no_query_repeat_train:
						break
					else:
						no_query_repeat_train.append(q)
				
					
				q_id = normId( q_id, Id_dict)
				a_id  = normId( a_id  , Id_dict)
				if a_id in q_id:
					label = 1
				else:
					label = 0 
			except:
				print "Error parser:" + item
				continue
			qt = tokeniztion(q)  #"\t".join(word_tokenize(query))
			a = tokeniztion(a)
			if int(label) == 1:
				pos_set.append([a,item])
			else:
				neg_set.append([a,item])
		if pos_set == []:
			no_postive += 1
		if pos_set ==[] and neg_set == []:
			continue
			#print x, no_postive, a
		line = generate_qaset(uid=str(x), q=qt, pos_set=pos_set, neg_set=neg_set)
		index_line = generate_index(uid=str(x), q=qt, pos_set=pos_set, neg_set=neg_set)
		qa_set.append(line)
		index_set.append(index_line)
	print len(qa_set),len(index_set)
	open(save_file,'w').write('\n'.join(qa_set[dev_size:]))
	open(save_file.replace(".xml",".xml.index"),'w').write("\n".join(index_set[dev_size:]))
	if dev_size > 0:
		open(save_file.replace("train","dev"),'w').write('\n'.join(qa_set[:dev_size]))
	return 1




def g_file_svm(infile,save_file, terminology, dev_size=900):
	dataset = open(infile,'r').read().split("===========================\n")
	qa_set = []
	no_postive=0
	Id_dict = read_term(terminology)
	if dev_size>0:
		mode = 'train'
		mdict = dictionary()
		mdict.clean()
	else:
		mdict = dictionary()
		mode = 'test'
	for x, data in enumerate(dataset):
		if data.strip() == '':
			continue
		item_set = data.strip().split('\n')
		
		if len(set(item_set)) == 1:
			continue
		query = ''
		pos_set, neg_set = [],[]
		for y, item in enumerate(item_set):
			repeat_list = []
			if item in repeat_list:
				continue
			else:
				repeat_list.append(item)
			#print item
			try:
				#label , query, question, ques_id, query_id =  item.split('\t')
				q , a, q_id, a_id, sieve, fname, index =  item.split('\t')
				if a in repeat_list:
					continue
				else:
					repeat_list.append(a)
				q_id = normId( q_id, Id_dict)
				a_id  = normId( a_id  , Id_dict)
				if a_id in q_id:
					label = 1
				else:
					label = 0 
			except:
				print "Error parser:" + item
				continue
			qt = tokeniztion(q)  #"\t".join(word_tokenize(query))
			a = tokeniztion(a)
			if int(label) == 1:
				pos_set.append(a)
			else:
				neg_set.append(a)
		if pos_set == []:
			no_postive += 1
		line = generate_qaset_svm(uid=str(x), q=qt, pos_set=pos_set, neg_set=neg_set, mdict = mdict, mode = mode)
		qa_set.append(line)
	print len(qa_set)

	open(save_file,'w').write('\n'.join(qa_set[dev_size:]))
	if dev_size > 0:
		open(save_file.replace("train","dev"),'w').write('\n'.join(qa_set[:dev_size]))
	mdict.store_dict()
	return 1


def tokeniztion(word):
	c_word = ''
	for item in word:
		if item in string.punctuation:
			c_word += ' ' + item + ' '
		else:
			c_word += item
	c_word = c_word.replace('  ', ' ').replace(' ', '\t')
	return c_word

def generate_qaset(uid,q, pos_set, neg_set):
	head = "<QApairs id='" +uid + "'>\n<question>\n"
	ques_line = q + '\n</question>\n'
	pos_lines = ''.join(["<positive>\n"+item[0]+"\n</positive>\n" for item in pos_set])
	neg_lines = ''.join(["<negative>\n"+item[0]+"\n</negative>\n" for item in neg_set])
	end = "</QApairs>"
	return head + ques_line + pos_lines + neg_lines +end

def generate_index(uid,q, pos_set, neg_set):
	return "\n".join([uid + "\t" + str(x) + "\t" +  item[1] for x, item  in enumerate( pos_set + neg_set ) ])



def feature_generate(q,a, mdict,mode):
	feature = []
	#qset,aset = q.split('\t'),a.split('\t')
	#print "q:", q, "a:", a
	qset, aset = ngram_split(q), ngram_split(a)
	#print qset, aset
	for i in xrange(0,len(qset) if len(qset) < 5 else 5):
		if qset[i] in aset:
			feature.append(str(i + 1) + ":1")
	start = 6
	all_match = 1 if qset == aset else 0
	feature.append(str(start) + ":" + str(all_match) )
	start += 1
	partial_match =  (len(feature) -1)/ float(len(qset))
	feature.append(str(start) + ":" + str(partial_match) )
	start += 1
	bow_sorted = bag_of_word(qset, aset, mdict, start,mode)
	for item in bow_sorted:
		feature.append(str(item[0])+':'+str(item[1]))
	return feature

def ngram_split(phrase,  flag="\t"):
	unigram = phrase.split(flag)
	bigram = [ unigram[i-1] + '_' + unigram[i] for i in xrange(1,len(unigram) )] if len(unigram) > 1 else []
	trigram = [unigram[i-2] + '_' + unigram[i-1] + '_' + unigram[i] for i in xrange(2,len(unigram) )] if len(unigram) > 2 else []
	return unigram + bigram + trigram

def bag_of_word(q,a,mdict,start,mode):
	bow = {}
	if mode == 'train':
		mdict.add_words(q)
		mdict.add_words(a)

	for word in q:
		if mdict.get_index(word) != -1:
			index = mdict.get_index(word)
			if index+ start in bow:
				bow[index+start] += 1
			else:
				bow[index+start] = 1
	for word in a:
		if mdict.get_index(word) != -1:
			index = mdict.get_index(word)
			if index+ start in bow:
				bow[index+start] += 1
			else:
				bow[index+start] = 1
	bow_sorted = sorted(bow.iteritems(), key= lambda x:x[0])
	return bow_sorted

def generate_qaset_svm(uid, q, pos_set, neg_set, mdict, mode='train'):
	outlist = []
	
	#feature: 5 same, all same word
	for enum,item in enumerate(pos_set):
		feas = feature_generate(q=q, a=item, mdict=mdict,mode=mode)
		line = "1" + ' ' + 'qid:' + str(uid) + ' ' + ' '.join(feas) + " #"+ str(uid) + '1_'+ str(enum) 
		outlist.append(line)
	for enum,item in enumerate(neg_set):
		feas = feature_generate(q=q, a=item, mdict=mdict,mode=mode)
		line = "0" + ' ' + 'qid:' + str(uid) + ' ' + ' '.join(feas) + " #"+ str(uid) + '0_' + str(enum) 
		outlist.append(line)
	return '\n'.join(outlist)



if __name__ == '__main__':
	'''
	if len(sys.argv) < 2:
		traindir = "./data/cui_train"
		testdir = "./data/cui_test"
	else:
		traindir, testdir = sys.argv[1:3]
	if sys.argv[3] == 'xml':
		g_file(traindir, "train.xml",dev_size= 900)
		g_file(testdir , "test.xml",dev_size= 0)
	else:
		g_file_svm(traindir, "train.svm",dev_size= 900)
		g_file_svm(testdir , "test.svm",dev_size= 0)
	'''
	g_file(sys.argv[1],sys.argv[2], sys.argv[3], int(sys.argv[4]))
