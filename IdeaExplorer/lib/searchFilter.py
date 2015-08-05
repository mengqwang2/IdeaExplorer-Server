import os,sys
from models import *
from datetime import date
from dateutil.relativedelta import relativedelta

class Filter():
	def __init__(self,filt,dlist):
		self.__filt=filt
		self.__dlist=dlist

	def doFilter(self):
		if(self.__filt=="1month"):
			targetDate = date.today()+relativedelta(months=-1)

		elif(self.__filt=="6months"):
			targetDate = date.today()+relativedelta(months=-6)

		elif(self.__filt=="1year"):
			targetDate = date.today()+relativedelta(years=-1)

		elif(self.__filt=="5years"):
			targetDate = date.today()+relativedelta(years=-5)

		elif(self.__filt=="10years"):
			targetDate = date.today()+relativedelta(years=-10)

		else:
			targetDate = date.today()+relativedelta(years=-50)

		dateStr=targetDate.strftime('%Y%m%d')
		dateStr=int(dateStr)
		#print dateStr

		filterList=[]
		for ele in self.__dlist:
			idea=Ideas.objects.get_or_404(id=ele)
			dat=str(idea.submit_date)[0:10]
			cur=dat[0:4]+dat[5:7]+dat[8:10]
			if(int(cur)>dateStr):
				filterList.append(ele)

		return filterList

