from flask import current_app, flash, Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
import sys
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer/DBUpdate')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/Idea-Server/IdeaExplorer/lib')
from models import *
from flask.ext.mongoengine.wtf import model_form
import forms
from User import Users
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from IdeaExplorer import login_manager,flask_bcrypt
import logging

class interest(MethodView):
	def __init__(self,keyword,doc,userId):
		self.keyword=keyword
		self.doc=doc
		self.userId=userId

	def doLogInterest(self):
		userObj=UserProfile.objects.all()
		 for uo in userObj:
            if(uo.email==userId):
                for kw in self.keyword:
                	if kw not in uo.keyword:
                    	uo.keyword.append(kw)

                for doc in self.doc:
                	if doc not in uo.doc:
                		uo.doc.append(doc)
                try:
                    uo.save()
                    return "Interest logged"
                except:
                    return "Failed to log interest"

            return "User not found"

    	return "Error!"