import os,sys
from datetime import date
from dateutil.relativedelta import relativedelta
import mx.DateTime as dt

class Filter():
	def __init__(self,filt):
		self.__filt=filt

	def doFilter(self):
		if(self.__filt=="all"):
			pass

		elif(self.__filt=="1month"):
			= date.today()-relativedelta(months=-1)

		elif(self.__filt=="1year"):

