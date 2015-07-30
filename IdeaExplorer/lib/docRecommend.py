import os,sys
import docDetail,ideaParse
from flask import current_app, flash, Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
import sys
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer/DBUpdate')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer/lib')
import models
from models import *
from flask.ext.mongoengine.wtf import model_form
import forms
from User import Users
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from IdeaExplorer import login_manager,flask_bcrypt
import logging

class DocRecommend():
	def __init__(self,docList,k):
		self.__doclist=docList
		self.__idea=Ideas.objects.all()
		self.__searchlist=[]
		self.__ip=ideaParse.IdeaParse(self.__idea)
		idStr=self.__ip.fieldParse('id')
		for i in idStr:
			self.__searchlist.append(int(i))
		self.__k=k
		self.__recSet=set()

	def typeMatch(self,docid):
		type_of_innovation=self.__ip.fieldParse('type_of_innovation')
		similar_id=set()

		if type_of_innovation[docid]=="None":
			return self.__searchlist

		for si in self.__searchlist:
			if type_of_innovation[si]==type_of_innovation[docid]:
				similar_id.add(si)

		return similar_id

	def tagSearch(self,docSet,docid):
		docSet=set()
		dt=DocTag.objects.get_or_404(docid=docid)
		tagList=dt.tags
		for ele in tagList:
			td=TagDoc.objects.get_or_404(tag=ele)
			for docEle in td.docid:
				if docEle!=docid and docEle in docSet:
					docSet.add(docEle)

		return docSet

	def recommend(self,docSet,docid):
		simObj=DocSim.objects.get_or_404(docid=docid)
		simList=simObj.similarity
		simList_sorted=sorted(simList, key=lambda k: k['sim'])
		docList=[]
		if(len(simList_sorted)>=self.__k):
			for i in range(0,self.__k):
				self.__recSet.add(simList_sorted[i]['docid'])
		else:
			for ele in simList_sorted:
				self.__recSet.add(ele['docid'])



	def doRecommend(self):
		for doc in self.__doclist:
			search_id1=self.typeMatch(doc)
			search_id2=self.tagSearch(search_id1,doc)
			self.recommend(search_id2,doc)
		return self.__recSet