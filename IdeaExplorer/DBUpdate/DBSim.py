import os,sys,numpy

class DBSim():
	def __init__(self,gamma):
		self.__gamma=gamma

	def distance(self,document1,document2):
		d1=numpy.asarray(document1)
		d2=numpy.asarray(document2)
		sim = sum(pow(d1-d2,2))
		return sim

	def similarity(self):
		similarity_matrix=dict()
		for k,v in self.__gamma.iteritems():
			cnt=0
			for k1,v1 in self.__gamma.iteritems():
				if k1!=k:
					if k not in similarity_matrix:
						similarity_matrix[k]=dict()
					if k1 not in similarity_matrix:
						similarity_matrix[k1]=dict()

					if k1 not in similarity_matrix[k]:
						result=self.distance(v,v1)
						similarity_matrix[k][k1]=result
						similarity_matrix[k1][k]=result
						cnt=cnt+1
			print cnt


		return similarity_matrix
