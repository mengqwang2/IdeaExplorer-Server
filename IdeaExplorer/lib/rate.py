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

class Rate():
	def __init__(self,postid,email):
		self.postid=int(postid)
		self.email=email

	def rateGet(self):
		postAll=UserPost.objects.all()
		fd=0
		for p in postAll:
			if p.docid==self.postid:
				postObj=UserPost.objects.get_or_404(docid=self.postid)
				fd=1
		if fd==0:
			return 0

		if self.email=='0':
			return postObj.avgrate

		for r in postObj.rate:
			if r.user.email==self.email:
				return r.rating

	def ratePost(self,rating):
		rt=models.Rate()
		userObj=UserProfile.objects.get_or_404(email=self.email)
		rt.user=userObj
		rt.rating=rating
		upObj=UserPost.objects.all()
		for up in upObj:
			if(up.docid==self.postid):
				for rateObj in up.rate:
					print rateObj.user.email
					if (rateObj.user.email==self.email):
						rateObj.rating=rating
				allRate=[r.rating for r in up.rate]
				avgRate=reduce(lambda x, y: x + y, allRate) / len(allRate)
				up.avgrate=avgRate
				up.save()
				return "Rate successfully!"

				up.rate.append(rt)
				allRate=[r.rating for r in up.rate]
				avgRate=reduce(lambda x, y: x + y, allRate) / len(allRate)
				up.avgrate=avgRate
				up.save()
				return "Rate successfully!"

		try:
			up=models.UserPost()
			up.docid=self.postid
			up.rate.append(rt)
			up.slug=str(self.postid)
			up.avgrate=rating
			up.save()
			return "Rate successfully!"
		except:
			return "Fail to rate"









