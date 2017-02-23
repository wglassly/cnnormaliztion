import os,sys
import json
class dictionary:
	def __init__(self,store_file = 'dictionary.dic'):
		self.store_file = store_file
		if os.path.exists(store_file):
			self.load(store_file)
		else:
			#pen(store_file,'w').write('')
			self.dict = {}
	
	def load(self, store_file):
		jstr = open(store_file,'r').read()
		#{word:[index, frequence]}
		self.dict =  json.loads(jstr)	

	def add_word(self, word):
		if word in self.dict:
			self.dict[word][1] += 1
		else:
			index = len(self.dict)
			self.dict[word] = [index,1]

	def  get_index(self,word):
		if word not in self.dict:
			return -1
		return self.dict[word][0]

	def get_frequence(self,word):
		if word not in self.dict:
			return 0
		return self.dict[word][1]

	def add_words(self,words):
		for word in words:
			self.add_word(word)

	def clean(self):
		self.dict = {}

	def store_dict(self, store_path=''):
		if not store_path:
			store_path = self.store_file
		jstr = json.dumps(self.dict)
		open(store_path,'w').write(jstr)

if __name__ == '__main__':
	mdict = dictionary()
	mdict.add_word("word")
	print mdict.get_index("word")