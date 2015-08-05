import os,sys
import sys
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer/DBUpdate')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer/lib')
import models
from models import *

class InterestManage():
	def __init__(self,email="",kw=""):
		self.__email=email
		self.__kw=kw
		self.__up=UserProfile.objects.get_or_404(email=self.__email)
		self.__kwList=self.__up.keyword

	def interestGet(self):
		return self.__kwList

	def interestDelete(self):
		if(self.__kw==""):
			return "No deletion executed"

		l=[ele for ele in self.__kwList if ele==self.__kw]
		self.__up.keyword=l
		try:
			self.__up.save()
			return "Delete successfully"
		except:
			return "Fail to delete"

