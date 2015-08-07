from IdeaExplorer import app
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import json
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask.ext.httpauth import HTTPBasicAuth
import logging
from flask import request, jsonify
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import register,login,docList,docDetail,rate,comment,docRecommend,category,sorter,searchFilter,interestManage
from models import *
from IdeaExplorer import cache
from flask import current_app, flash, Blueprint, request, redirect, render_template, url_for
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
import flask
import urllib
from operator import itemgetter
from collections import deque


api = Api(app)
auth = HTTPBasicAuth()

def cache_key():
    args=flask.request.args
    key1=flask.request.path
    keyList=key1.split("&")
    return keyList[0]

def cache_key_index():
    args=flask.request.args
    key1=flask.request.path
    keyList=key1.split("&")
    return keyList[0]+keyList[1]

def cache_key_query():
    args=flask.request.args
    key1=flask.request.path
    keyList=key1.split("&")
    return keyList[0]+keyList[1]+keyList[2]

class Utility:
    @staticmethod
    def generate_auth_token(user, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': user['Email']})
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            logging.warning('decoding')
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        id = data['id']
        return id


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    if (not ('authorization' in request.headers)):
        logging.warning("nothing in token")
        return False
    username_or_token = request.headers['authorization']
    logging.warning("verifying: " + username_or_token)
    
    user = Utility.verify_auth_token(username_or_token)
    #if not user:
        # try to authenticate with username/password
    if not user:
        logging.warning('verification failed')
        return False
    logging.warning('verification succeeded')
    return True


class IdeaAPI(Resource):
    decorators = [auth.login_required]

    @cache.cached(timeout=500,key_prefix=cache_key_index)
    def retrieveIdeaList(self,email):
        userObj=UserProfile.objects.get_or_404(email=email)
        dl=docList.DocList(userObj=userObj)
        dlist=dl.doRetrieveDoc()
        data=list()
        ideasDict={}
        for d in dlist:
            rateObj=rate.Rate(d,'0')
            rt=rateObj.rateGet()
            d_detail=dict()
            d_detail["id"]=d
            dd=docDetail.DocDetail(d)
            d_detail["title"]=dd.getTitle()
            d_detail["description"]=dd.getDescription()
            d_detail["tags"]=dd.getTags()
            d_detail["rating"]=rt
            d_detail["innovators"]=dd.getInnovator()
            data.append(d_detail)
        return data

    def get(self, email, ca, sind, capacity):
        print "IdeaAPI"
        self.email=email
        data=self.retrieveIdeaList(email)
        ideasDict={}

        size=len(data)
        if (sind>=size):
            ideasDict["Ideas"]=[]
            ideasDict["eind"]=size-1
            ideasDict['size']=len(data)
            return ideasDict
        
        if (sind+capacity>size):
            data1=data[sind:size]
            ideasDict["eind"]=size-1
        else:
            data1=data[sind:sind+capacity]
            ideasDict["eind"]=sind+capacity-1
        
        ideasDict["Ideas"]=data1
        ideasDict['size']=len(data)
        return ideasDict


class DetailAPI(Resource):
    decorators = [auth.login_required]
    def get(self, postid, email):
        print "DetailAPI"
        #Return document detail
        dd=docDetail.DocDetail(postid)
        rateObj=rate.Rate(postid,'0')
        rt=rateObj.rateGet()
        data=dict()
        data["title"]=dd.getTitle()
        data["description"]=dd.getDescription()
        data["innovators"]=dd.getInnovator()
        data["submit_date"]=dd.getUpdatedDate()
        data["rtc"]=dd.getRelevance()
        data["pps"]=dd.getProbSolved()
        data["success_benefit"]=dd.getSuccessBenefit()
        data["rating"]=rt
        data["tags"]=dd.getTags()
        data["innovators"]=dd.getInnovator()
        data["id"]=postid
        #Write user preference
        uo=UserProfile.objects.get_or_404(email=email)
        docList=deque(uo.doc)
        if postid not in docList:
            docList.append(postid)
            if(len(docList)>5):
                docList.popleft()
            docList=list(docList)
            uo.doc=docList
            uo.save()

        return data

class SimilarAPI(Resource):
    decorators = [auth.login_required]

    @cache.cached(timeout=250,key_prefix=cache_key)
    def getSimilarPosts(self,postid):
        d=list()
        d.append(postid)
        dl=docList.DocList(docList=d)
        dlist=dl.doRetrieveDoc()
        data=list()

        for d in dlist:
            rateObj=rate.Rate(d,'0')
            rt=rateObj.rateGet()
            d_detail=dict()
            d_detail["id"]=d
            dd=docDetail.DocDetail(d)
            d_detail["title"]=dd.getTitle()
            d_detail["description"]=dd.getDescription()
            d_detail["tags"]=dd.getTags()
            d_detail["rating"]=rt
            d_detail["innovators"]=dd.getInnovator()
            data.append(d_detail)
        return data
        
        
    def get(self, postid):
        data=self.getSimilarPosts(postid)
        ideaDict=dict()
        ideaDict["Ideas"]=data
        return ideaDict
        

class QueryAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        super(QueryAPI, self).__init__()

    @cache.cached(timeout=350,key_prefix=cache_key_query)
    def retrieveIdeaList(self,kwList,criteria,filt):
        dl=docList.DocList(kwList=kwList)
        dlist=dl.doRetrieveDoc()
        #print dlist
        #filter
        sf=searchFilter.Filter(filt,dlist)
        dlist=sf.doFilter()

        #sort
        sortObj=sorter.Sorter(criteria,dlist)
        sortObj.doSort()
        dlist=sortObj.getList()

        data=list()
        
        for d in dlist:
            rateObj=rate.Rate(d,'0')
            rt=rateObj.rateGet()
            d_detail=dict()
            d_detail["id"]=d
            dd=docDetail.DocDetail(d)
            d_detail["title"]=dd.getTitle()
            d_detail["description"]=dd.getDescription()
            d_detail["tags"]=dd.getTags()
            d_detail["rating"]=rt
            d_detail["innovators"]=dd.getInnovator()
            data.append(d_detail)
        return data

    def get(self,queries,sorter,filt,sind,capacity,email):
        print "QueryAPI"
        kwList=queries.split("%")
        print kwList

        #record keyword interest
        up=UserProfile.objects.get_or_404(email=email)
        oldlist=up.keyword

        for ele in kwList:
            if ele not in oldlist:
                oldlist.append(ele)

        up.keyword=oldlist
        up.save()
        
        data=self.retrieveIdeaList(kwList,sorter,filt)
        #print data

        ideasDict={}

        size=len(data)
        if (sind>=size):
            ideasDict["Ideas"]=[]
            ideasDict["eind"]=size-1
            ideasDict['size']=len(data)
            return ideasDict
        
        if (sind+capacity>size):
            data1=data[sind:size]
            ideasDict["eind"]=size-1
        else:
            data1=data[sind:sind+capacity]
            ideasDict["eind"]=sind+capacity-1
        
        ideasDict["Ideas"]=data1
        ideasDict['size']=len(data)
        return ideasDict

class CategoryAPI(Resource):
    decorators = [auth.login_required]

    @cache.cached(timeout=100000,key_prefix=cache_key)
    def getCategory(self):
        cat=category.Category(5)
        catList=cat.getCatList()
        return catList

    def get(self):
        return self.getCategory()


class RatingPostAPI(Resource):
    decorators = [auth.login_required]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Email', type=str, required=True,
                                   help='Email required',
                                   location='json')
        self.reqparse.add_argument('Rating', type=int, required=True,
                                   help='Rating required',
                                   location='json')
        self.reqparse.add_argument('PostID', type=int, required=True,
                                   help='PostID required',
                                   location='json')

        super(RatingPostAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        email=args["Email"]
        rating=args["Rating"]
        docid=args["PostID"]
        rateObj=rate.Rate(docid,email)
        msg=rateObj.ratePost(rating)
        print msg
        if(msg=="Rate successfully!"):
            return 201
        return 450

#average and individual rating
class RatingGetAPI(Resource):
    decorators = [auth.login_required]
    def get(self, postid, email): #0 email means getting average rating
        rateObj=rate.Rate(postid,email)
        rt=rateObj.rateGet()
        return {'rating': rt};

class CommentGetAPI(Resource):
    decorators = [auth.login_required]
    def get(self,postid):
        comObj=comment.Comment(postid)
        comList=comObj.commentGet()
        return {'Comment': comList}


class CommentPostAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Email', type=str, required=True,
                                   help='Email required',
                                   location='json')
        self.reqparse.add_argument('PostID', type=int, required=True,
                                   help='PostID required',
                                   location='json')
        self.reqparse.add_argument('Content', type=str, required=True,
                                   help='Password required',
                                   location='json')

        super(CommentPostAPI, self).__init__()


    def post(self):
        print "Comment API"
        args = self.reqparse.parse_args()
        email=args["Email"]
        content=args["Content"]
        docid=args["PostID"]

        try:
            comObj=comment.Comment(docid)
            msg=comObj.commentPost(content,email)
            if (msg=="Comment successfully!"):
                comList=comObj.commentGet()
                return {'Comment': comList},201
            return 450
        except:
            raise sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
            return 450

class UserRegAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('UserID', type=str, required=True,
                                   help='UserID required',
                                   location='json')
        self.reqparse.add_argument('Username', type=str, required=True,
                                   help='Username required',
                                   location='json')
        self.reqparse.add_argument('Password', type=str, required=True,
                                   help='Password required',
                                   location='json')
        self.reqparse.add_argument('Email', type=str, required=True,
                       help='Email required',
                       location='json')
        super(UserRegAPI, self).__init__()

    def post(self):
        print "UserRegAPI"
        args = self.reqparse.parse_args()
        logging.warning(args)
        reg=register.Register(args['Username'],args['UserID'],args['Email'],args['Password'])
        msg=reg.doRegister()
        if (msg=="Register successfully!"):
            return {"state": msg},201
        return {"state":msg},450
        

class UserAuthAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Email', type=str, required=True,
                                   help='Email required',
                                   location='json')
        self.reqparse.add_argument('Password', type=str, required=True,
                                   help='Password required',
                                   location='json')
        super(UserAuthAPI, self).__init__()

    def post(self):
        print "UserAuthAPI"
        args = self.reqparse.parse_args()
        l=login.Login(args['Email'],args['Password'])
        msg=l.doLogin()
        if (msg=="Login successfully"):
            name=l.getName()
            logging.warning("Login successfully")
            currentID = Utility.generate_auth_token(args)
            currentID = currentID.decode('ascii')
            return {'Token':currentID, "state":msg, "name":name}, 201
        else:
            logging.warning("Login failed")
            return {"state":msg},450

class UserHabitAPI(Resource):
    def get(self,email,kw):
        im=interestManage.InterestManage(email=email)
        return im.interestGet()

    def delete(self,email,kw):
        im=interestManage.InterestManage(email=email,kw=kw)
        msg=im.interestDelete()
        if(msg=="Delete successfully" or msg=="No deletion executed"):
            return 201
        else:
            return 450



api.add_resource(IdeaAPI, '/api/ideas/id=<string:email>&ca=<int:ca>&start=<int:sind>&cap=<int:capacity>')
api.add_resource(SimilarAPI, '/api/ideas/relevant/<int:postid>')
api.add_resource(CategoryAPI, '/api/category')
api.add_resource(UserAuthAPI, '/api/login')
api.add_resource(QueryAPI, '/api/ideas/query=<string:queries>&sort=<string:sorter>&filt=<string:filt>&start=<int:sind>&cap=<int:capacity>&email=<string:email>')
api.add_resource(UserRegAPI, '/api/reg')
api.add_resource(CommentGetAPI, '/api/ideas/comment/<int:postid>')
api.add_resource(CommentPostAPI, '/api/ideas/comment')
api.add_resource(RatingPostAPI, '/api/ideas/rating')
api.add_resource(RatingGetAPI, '/api/ideas/rating/<int:postid>/<string:email>')
api.add_resource(UserHabitAPI, '/api/user/interest/email=<string:email>&interest=<string:kw>')
api.add_resource(DetailAPI, '/api/ideas/details/<int:postid>&<string:email>')