import os,sys
from build_ranking_without_repeat_train import g_file,g_file_svm
from benchmark import benchmark

def sys_run(command):
	os.system(command)

def recompline():
	sys_run("javac ./tool/sieves/*.java")
	sys_run("javac ./tool/util/*.java")
	sys_run("javac ./tool/Main.java")
	#sys_run("javac ./tool/MainTraining.java")

def run_rulebase(dataset,mode = 'test'):
	recompline()
	training_set = dataset + "/training"
	if mode == 'test':
		test_set  = dataset + "/test"
		#exe = "tool.Main"
		sieve_Level = "-1"
		sieve_Level = "10"
	elif mode == 'train':
		test_set = dataset + "/dev"
		#exe = "tool.MainTraining"'
		sieve_Level = "-1"
	else:
		print "only accepted train or test."
	terminology = dataset + "/TERMINOLOGY.txt"
	
	#data_label = dataset.split('/')[-1] if dataset.split('/')[-1] !=0 else dataset.split('/')[-2] 
	print "java " + " ".join(["tool.Main", training_set,test_set,terminology,sieve_Level])
	sys_run("java " + " ".join(["tool.Main", training_set,test_set,terminology,sieve_Level]) )
	sys_run("cp candidate.txt " + dataset + "/" + mode + "_candidate.txt" )

def generate_candidate_xml(dataset, mode='test'):
	infile = dataset + "/" + mode + "_candidate.txt"
	save_file = dataset + "/" + mode + "_candidate.xml"
	terminology = dataset + "/TERMINOLOGY.txt"
	if mode == 'test':
		dev_size = 0
	else:
		dev_size = 500
	g_file(infile, save_file, terminology, dev_size)
	benchmark(infile, terminology)

def generate_candidate_svm(dataset, mode='test'):

	print "warning... please train before test when you tried to generate svm format"
	infile = dataset + "/" + mode + "_candidate.txt"
	save_file = dataset + "/" + mode + "_candidate.svm"
	terminology = dataset + "/TERMINOLOGY.txt"
	if mode == 'test':
		dev_size = 0
	else:
		dev_size = 500
	g_file_svm(infile, save_file, terminology, dev_size)

def run(dataset, mode):
	run_rulebase(dataset,mode)
	generate_candidate_xml(dataset,mode)
	generate_candidate_svm(dataset,mode)

if __name__ == '__main__':

	run(sys.argv[1], sys.argv[2])
