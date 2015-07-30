import os,sys,numpy

class DBVocab():
	def __init__(self,vocabFile):
		self.__vocab=vocabFile

	def vocabBuilder(self):
		vocab=list()
		with open(self.__vocab) as f:
			for line in f:
				v=line.split()
				for ele in v:
					vocab.append(ele)
		return vocab

	