# -*- coding: utf-8 -*-
import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
from models import *


class Users(UserMixin):
    def __init__(self, badgeid=None, email=None, password=None, keyword=None, doc=None, id=None, active=True,name=None):
        self.badgeid = badgeid
        self.password = password
        self.name=name
        self.keyword = keyword
        self.doc = doc
        self.email = email
        self.id = None
        self.active = active


    def save(self): 
        newUser = models.UserProfile(email=self.email, password=self.password, name=self.name, doc=self.doc, keyword=self.keyword, badgeid=self.badgeid,active=self.active)
        newUser.save()
        print "new user id = %s " % newUser.id
        self.id = newUser.id
        return self.id

    def get_by_email(self, email):
    	dbUser = models.UserProfile.objects.get(email=email)
    	if dbUser:
            self.email = dbUser.email
            self.id = dbUser.id
            self.active = dbUser.active
            return self
        else:
            return None
    
    def get_by_email_w_password(self, email):
        try:
            dbUser = models.UserProfile.objects.get(email=email)
            
            if dbUser:
                self.email = dbUser.email
                self.password = dbUser.password
                self.active = dbUser.active
                self.id = dbUser.id
                return self
            else:
                return None
        except:
            print "there was an error"
            return None

    def get_mongo_doc(self):
        if self.id:
            return models.UserProfile.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, id):
    	dbUser = models.UserProfile.objects.with_id(id)
    	if dbUser:
    		self.email = dbUser.email
    		self.active = dbUser.active
    		self.id = dbUser.id

    		return self
    	else:
    		return None

class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
