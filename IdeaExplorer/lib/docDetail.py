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


class DocDetail(MethodView):
	def __init__(self,docid):
		self.docid=docid
		self.ideaObj=Ideas.objects.get_or_404(id=self.docid)

	def wordTrim(self,word):
		punc = ["(", ")", ":", ";", ",", "-", "!", ".", "?", "/", "\"", "*","#","_"]
		word = word.lower()
		for p in punc:
			word = word.replace(p, " ")
		return word

	def getTags(self):
		raw_tag=self.ideaObj.tags
		if raw_tag=="":
			raw_tag="na"
		word=unicode(raw_tag).encode("utf-8")
		word=self.wordTrim(word)
		wordList=word.split()
		wordList=list(set(wordList))
		return wordList

	def getUpdatedDate(self):
		return self.ideaObj.updated_date

	def getRelevance(self):
		return self.ideaObj.relevance_to_challenge

	def getTitle(self):
		return self.ideaObj.title

	def getInnovator(self):
		innoList=list()
		for i in self.ideaObj.innovators:
			innoDict=dict()
			innoDict["badge_no"]=i.badge_no
			innoDict["name"]=i.name
			innoDict["email"]=i.email

			innoList.append(innoDict)

		return innoList

	def getStatus(self):
		return self.ideaObj.status

	def getDescription(self):
		return self.ideaObj.description

	def getIdeaHistory(self):
		return self.ideaObj.idea_history

	def getStatusDate(self):
		return self.ideaObj.status_date

	def getProbSolved(self):
		return self.ideaObj.practical_problem_solved

	def getSubmitter(self):
		return self.ideaObj.submitter

	def getSuccessBenefit(self):
		return self.ideaObj.success_benefit

