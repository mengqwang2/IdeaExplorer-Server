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
import logging,keywordSearch,docRecommend
import category


class DocList(MethodView):
	def __init__(self,userObj=None,kwList=[],docList=[]):
		self.uo=userObj
		self.kwList=kwList
		self.docList=docList

	def getKeywords(self):
		return self.uo.keyword

	def getDocHistory(self):
		return self.uo.doc

	def doRetrieveDoc(self):
		d1=set()
		d2=set()
		kwList=list()
		docList=list()

		if self.uo!=None:
			kwList=self.uo.keyword
			docList=self.uo.doc
			if len(kwList)==0 and len(docList)==0:
				cat=category.Category(3)
				cat.getPopTopics()
				kwList=cat.getCatList()
				docList=[]

		if len(self.kwList)>0:
			kwList=self.kwList
			
		if len(self.docList)>0:
			docList=self.docList
			
		ks=keywordSearch.KeywordSearch(kwList,2)
		d1=ks.doSearch()
		dr=docRecommend.DocRecommend(docList,5)
		d2=dr.doRecommend()

		recSet=d1.union(d2)
		return recSet
