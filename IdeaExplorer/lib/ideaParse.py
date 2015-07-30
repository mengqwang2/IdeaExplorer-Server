import os, sys


class IdeaParse():
	def __init__(self,ideaObj):
		self.__ideaObj=ideaObj

	def fieldParse(self,fname):
		if (fname!='id'):
			fieldDict=dict()
			for io in self.__ideaObj:
				if(fname=="tags"):
					fieldDict[io.id]=io.tags
				elif(fname=="updated_date"):
					fieldDict[io.id]=io.updated_date
				elif(fname=="relevance_to_challenge"):
					fieldDict[io.id]=io.relevance_to_challenge
				elif(fname=="title"):
					fieldDict[io.id]=io.title
				elif(fname=="status"):
					fieldDict[io.id]=io.status
				elif(fname=="description"):
					fieldDict[io.id]=io.description
				elif(fname=="idea_history"):
					fieldDict[io.id]=io.idea_history
				elif(fname=="status_date"):
					fieldDict[io.id]=io.status_date
				elif(fname=="type_of_innovation"):
					fieldDict[io.id]=io.type_of_innovation
				
			return fieldDict

		else:
			fieldList=list()
			for io in self.__ideaObj:
				fieldList.append(int(io.id))
			return fieldList

