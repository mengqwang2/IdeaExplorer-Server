import os,sys,numpy
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

class KeywordSearch():
	def __init__(self,kw,k):
		self.__vocab=Vocab.objects.all()
		self.__keyword=kw
		self.__K=k

	def tagSearch(self):
		docSet=set()
		for word in self.__keyword:
			allTD=TagDoc.objects.all()
			fd=0
			for obj in allTD:
				if (obj.tag==word):
					fd=1
			if fd==1:
				TDObj=TagDoc.objects.get_or_404(tag=word)
				for ele in TDObj.docid:
					docSet.add(ele)
		return docSet

	def topicSearch(self):
		word_set=[]
	
		for wordObj in self.__vocab:
			word=wordObj.word
			wordid=wordObj.vid
			for kw in self.__keyword:
				if kw==word:
					word_set.append(wordid)

		topicSet=set()

		for word_id in word_set:
			temp = LambdaWT.objects.get_or_404(wordid=word_id)
			lamValue=temp.lam
			lamValue = zip(lamValue, range(0,len(lamValue)))
			rank = sorted(lamValue, key = lambda x: x[0],reverse=True)
			
			for i in range(0,self.__K):
				topicSet.add(rank[i][1])
		
		return topicSet

	def documentSearch(self,topic_set):
		document_id = list()
		for topic_id in topic_set:
			gammaObj=GammaTD.objects.get_or_404(topicid=topic_id)
			gamObj=gammaObj.gam
			gamObj_sorted=sorted(gamObj, key=lambda k: k['gamma'],reverse=True)
			
			for i in range(0,self.__K):
				document_id.append(gamObj_sorted[i].docid)
		return document_id


	def doSearch(self):
		docList=list()
		if len(self.__keyword)==0:
			return docList

		kw_updated=[]

		d=self.tagSearch()
		for ele in d:
			docList.append(ele)

		for ele in self.__vocab:
			if(ele.word in self.__keyword):
				if(ele.word not in kw_updated):
					kw_updated.append(ele.word)

		self.__keyword=kw_updated


		topic_id=self.topicSearch()
		document_id=self.documentSearch(topic_id)
		
		for ele in document_id:
			if ele not in docList:
				docList.append(ele)
		return docList
