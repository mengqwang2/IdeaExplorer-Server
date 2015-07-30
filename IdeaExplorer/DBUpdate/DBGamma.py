import os,sys,numpy

class DBGamma():
	def __init__(self,gammaFile):
		self.__gammaFile=gammaFile

	def gammaDT(self):
		gammaDict=dict()
		with open(self.__gammaFile) as f:
			for line in f:
				g=line.split()
				for ele in g[1:]:
					g[0]=int(g[0])
					if(g[0] not in gammaDict):
						gammaDict[g[0]]=list()
					gammaDict[g[0]].append(float(ele))

		#print gammaDict
		return gammaDict

	def gammaTD(self):
		gammaDict=dict()
		gammaArr=numpy.loadtxt(self.__gammaFile)
		indexList=list()

		for line in gammaArr:
			indexList.append(int(line[0]))
		gammaArr=gammaArr[:,1:]


		for col in range(gammaArr.shape[1]):
			gammaList=gammaArr[:,col].tolist()
			ind=0
			gammaDict[col]=dict()
			for ele in gammaList:
				gammaDict[col][indexList[ind]]=ele
				ind=ind+1

		#print gammaDict
		return gammaDict



