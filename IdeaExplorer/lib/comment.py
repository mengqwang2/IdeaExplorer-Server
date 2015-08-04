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

class Comment():
	def __init__(self,postid):
		self.postid=postid

	def commentGet(self):
		comList=[]
		postAll=UserPost.objects.all()
		
		for p in postAll:
			if p.docid==self.postid:
				postObj=UserPost.objects.get_or_404(docid=self.postid)
				break
		else:
			return comList

		for c in postObj.comments:
			comDict={}
			comDict["user"]=c.user.email
			comDict["content"]=c.content
			comDict["date"]=c.created_at.strftime('%H:%M %Y-%m-%d')
			comList.append(comDict)

		return comList

	def commentPost(self,content,email):
		com=models.Comment()
		userObj=UserProfile.objects.get_or_404(email=email)
		com.user=userObj
		com.content=content
		upObj=UserPost.objects.all()
		for up in upObj:
			if(up.docid==self.postid):
				up.comments.append(com)
				up.save()
				return "Comment successfully!"

		try:
			up=UserPost()
			up.docid=self.postid
			up.avgrate=0
			up.slug=str(self.postid)
			up.comments.append(com)
			up.save()
			return "Comment successfully!"
		except:
			return "Failed to comment."


