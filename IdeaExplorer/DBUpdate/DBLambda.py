import os,sys,numpy

class DBLambda():
	def __init__(self,lamFile):
		self.__lamFile=numpy.loadtxt(lamFile)

	def lam_tw(self):
		lamDict=dict()
		ind=0
		for row in self.__lamFile:
			lamDict[ind]=row.tolist()
			ind=ind+1
		return lamDict

	def lam_wt(self):
		lamDict=dict()

		for col in range(self.__lamFile.shape[1]):
			lamDict[col]=self.__lamFile[:,col].tolist()
		return lamDict




