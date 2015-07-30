import os,sys,numpy
import dataParse
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
		document_id = set()
		for topic_id in topic_set:
			gammaObj=GammaTD.objects.get_or_404(topicid=topic_id)
			gamObj=gammaObj.gam
			gamObj_sorted=sorted(gamObj, key=lambda k: k['gamma'],reverse=True)
			
			for i in range(0,self.__K):
				document_id.add(gamObj_sorted[i].docid)
		return document_id


	def doSearch(self):
		topic_id=self.topicSearch()
		document_id=self.documentSearch(topic_id)
		d=self.tagSearch()
		docset=d.union(document_id)
		return docset
