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


class Register(MethodView):
    def __init__(self,name,badgeid,email,password):
        self.name=name
        self.badgeid=badgeid
        self.email=email
        self.password=password

    def doRegister(self):
        user=Users(badgeid=self.badgeid, email=self.email, password=self.password, keyword=[], doc=[], active=True,name=self.name)
        try:
            user.save()
            return "Register successfully!"
        except:
            return "Unable to register."

