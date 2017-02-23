import os,sys

def read_term(infile):
	'''
	terminology format (line): ID<1>|ID<2>|...||term<1>|term<2>|...|term<n>
	js format {ID<1>:{additionList:[ID<2>,...], termList:[term<1>,term<2>,...,<term<n>>]}}
	'''
	termList = open(infile,'r').read().strip().split('\n')
	out_js = {}
	for line in termList:
		IDs, terms = line.split("||")
		IDset = IDs.split('|')
		#termset = [ term.lower() for term in terms.split('|')]
		for Id in IDset:
			out_js[Id] = IDset[0]
	return out_js

def normId(Id,Id_dict):
	return Id_dict[Id] if Id in Id_dict else Id
	
	
def read_id2term(infile):
	'''
	terminology format (line): ID<1>|ID<2>|...||term<1>|term<2>|...|term<n>
	js format {ID1:[t1,t2,t3...]}
	'''
	termList = open(infile,'r').read().strip().split('\n')
	out_js = {}
	for line in termList:
		IDs, terms = line.split("||")
		IDset = IDs.split('|')
		termset = [ term.lower() for term in terms.split('|')]
		for Id in IDset:
			out_js[IDset[0]] = termset
	return out_js
