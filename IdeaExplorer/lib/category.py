import os,sys,operator
import dataParse
from flask import current_app, flash, Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
from models import *
from flask.ext.mongoengine.wtf import model_form
import forms
from User import Users
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from IdeaExplorer import login_manager,flask_bcrypt
import logging

class Category():
	def __init__(self,k):
		self.__td=TagDoc.objects.all()
		self.__K=k
		self.__catList=set()
		self.__topicList=set()

	def getPopTags(self):
		tag_doc=dict()
		for tdObj in self.__td:
			tag_doc[tdObj.tag]=len(tdObj.docid)

		td_sorted=sorted(tag_doc.items(),key=operator.itemgetter(1),reverse=True)
		for i in range(0,self.__K):
			self.__catList.add(td_sorted[i][0])

	def getPopTopics(self):
		gammaObj=GammaTD.objects.all()
		tdGamma=dict()
		for go in gammaObj:
			tdGamma[go.topicid]=len(go.gam)

		tdGamma_sorted=sorted(tdGamma.items(),key=operator.itemgetter(1),reverse=True)
		for i in range(0,self.__K):
			self.__topicList.add(tdGamma_sorted[i][0])

	def getPopKW(self):
		for tid in self.__topicList:
			lo=LambdaTW.objects.get_or_404(topicid=tid)
			lamList=lo.lam
			lamValue=zip(lamList, range(0,len(lamList)))
			rank=sorted(lamValue, key = lambda x: x[0],reverse=True)
			for i in range(0,self.__K):
				wordid=rank[i][1]
				vo=Vocab.objects().get_or_404(vid=wordid)
				self.__catList.add(vo.word)

	def getCatList(self):
		return self.__catList

	def getCatList(self):
		self.getPopTags()
		self.getPopTopics()
		self.getPopKW()
		#print self.__catList
		return list(self.__catList)

