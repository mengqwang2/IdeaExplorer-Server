from flask import current_app, flash, Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
import sys
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/tumblelog/flask-tumblelog/tumblelog/DBUpdate')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/tumblelog/flask-tumblelog/tumblelog/lib')
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/tumblelog/flask-tumblelog/tumblelog')
import models
from models import *
from flask.ext.mongoengine.wtf import model_form
from User import Users
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from tumblelog import login_manager,flask_bcrypt
import forms, keywordSearch
from hashlib import md5
sys.path.append('/Users/mengqwang/Documents/IdeaExplorer/tumblelog/flask-tumblelog/tumblelog/DBUpdate')
import DBSim,DBGamma,DBLambda,DBVocab
import category, docRecommend

posts = Blueprint('posts', __name__, template_folder='templates')

class ListView(MethodView):
    @login_required
    def get(self):
        ideas = Ideas.objects.all()
        posts = UserPost.objects.all()
        user = UserProfile.objects.get_or_404(email=current_user.email)

        kwList=user.keyword
        docList=user.doc
        displayList=set()

        if len(kwList)>0:
            ks=keywordSearch.KeywordSearch(kwList,2)
            displayList=displayList.union(ks.doSearch())
        if len(docList)>0:
            ds=docRecommend.DocRecommend(docList,5)
            displayList=displayList.union(ds.doRecommend())
        else:
            displayList=["phone"]


        return render_template('posts/list.html', ideas=ideas, docList=displayList)

class DetailView(MethodView):
    def get_context(self, docid):
        ideas = Ideas.objects.get_or_404(id=docid)
        post = UserPost.objects.all()
        fd=0
        for ele in post:
            if int(ele.docid)==int(docid):
                fd=1

        if fd==0:
            post=UserPost(docid=docid,avgrate=0,comment=[],rate=[],slug=int(docid))
        else:
            post=UserPost.objects.get_or_404(docid=docid)

        context = {
                "post": post,
                "idea": ideas
        }

        return context


    @login_required
    def get(self,slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)


class CommentView(MethodView):
    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, docid):
        ideas = Ideas.objects.get_or_404(id=docid)
        post = UserPost.objects.all()
        fd=0
        for ele in post:
            if int(ele.docid)==int(docid):
                fd=1

        if fd==0:
            post=UserPost(docid=docid,avgrate=0,comment=[],rate=[],slug=int(docid))
        else:
            post=UserPost.objects.get_or_404(docid=docid)

        form = self.form(request.form)
        form.user.label_attr='email'

        context = {
            "post": post,
            "form": form
        }

        return context

    @login_required
    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/comment.html', **context)

    @login_required
    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)
            post = context.get('post')
            post.comments.append(comment)
            post.slug=str(post.slug)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)

class RateView(MethodView):
    form = model_form(Rate, exclude=['create_at'])

    def get_context(self, docid):
        ideas = Ideas.objects.get_or_404(id=docid)
        post = UserPost.objects.all()
        fd=0
        for ele in post:
            if int(ele.docid)==int(docid):
                fd=1

        if fd==0:
            post=UserPost(docid=docid,avgrate=0,comment=[],rate=[],slug=int(docid))
        else:
            post=UserPost.objects.get_or_404(docid=docid)

        form=self.form(request.form)
        form.user.label_attr='email'

        context = {
            "post": post,
            "form": form
        }

        return context

    @login_required
    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/rate.html', **context)

    @login_required
    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            rt = Rate()
            form.populate_obj(rt)
            post = context.get('post')
            post.rate.append(rt)

            allRate=[r.rating for r in post.rate]
            avgRate=reduce(lambda x, y: x + y, allRate) / len(allRate)
            post.avgrate=avgRate
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)

class LoginView(MethodView):
    def get(self):
        """
        gammaObj=DBGamma.DBGamma("data/LDAResult/gamma.dat")
        d1=gammaObj.gammaDT()
        d2=gammaObj.gammaTD()

        for k,v in d1.iteritems():
            go=GammaDT()
            go.docid=k
            go.gamma=v
            go.save()

        for k,v in d2.iteritems():
            go=GammaTD()
            go.topicid=k
            for k1,v1 in v.iteritems():
                dg=DocGamma()
                dg.docid=k1
                dg.gamma=v1
                go.gam.append(dg)
            go.save()
        

        
        lamObj=DBLambda.DBLambda("data/LDAResult/lambda.dat")
        d1=lamObj.lam_tw()
        d2=lamObj.lam_wt()
        for k,v in d2.iteritems():
            ld=LambdaWT()
            ld.wordid=k
            ld.lam=v
            ld.save()
        
        
        for k,v in d1.iteritems():
            ld=LambdaTW()
            ld.topicid=k
            ld.lam=v
            ld.save()

        

        
        gammaObj=Gamma.objects.all()
        #print gammaObj
        
        gammaDict=dict()
        for g in gammaObj:
            gammaDict[g.docid]=g.gamma

        #print gammaDict
        
        sim=DBSim.DBSim(gammaDict)
        simResult=sim.similarity()
        #print simResult
        
        for k,v in simResult.iteritems():
            docsimObj=DocSim()
            docsimObj.docid=int(k)
            for k1,v1 in v.iteritems():
                simObj=Similarity()
                simObj.docid=int(k1)
                simObj.sim=float(v1)
                docsimObj.similarity.append(simObj)
            docsimObj.save()
        
        
        gammaObj=DBGamma.DBGamma("data/LDAResult/gamma.dat")
        gammaDict=gammaObj.gamma()

        for k,v in gammaDict.iteritems():
            go=Gamma()
            go.docid=int(k)
            go.gamma=v
            go.save()
        
        dv=DBVocab.DBVocab("data/vocabulary.txt")
        vocList=dv.vocabBuilder()
        ind=0
        for ele in vocList:
            vocObj=Vocab()
            vocObj.vid=ind
            vocObj.word=ele
            vocObj.save()
            ind=ind+1
        """
        return render_template("posts/login.html")

    def post(self):
        email = request.form["email"]
        userObj = Users()
        user = userObj.get_by_email_w_password(email)
        if user and md5(request.form["password"]).hexdigest()==user.password and user.is_active():
            remember = request.form.get("remember", "no") == "yes"

            if login_user(user, remember=remember):
                return redirect('/list')
        return render_template("posts/login.html")

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/')

    @login_manager.user_loader
    def load_user(id):
        if id is None:
            redirect('/login')
        user = Users()
        user.get_by_id(id)
        if user.is_active():
            return user
        else:
            return None

class LogoutView(MethodView):
    @login_required
    def get(self):
        logout_user()
        return redirect('/')


class RegisterView(MethodView):
    def get(self):
        registerForm = forms.SignupForm()
        templateData = {
            'form' : registerForm
        }
        return render_template("posts/register.html", **templateData)

    def post(self):
        registerForm = forms.SignupForm(request.form)
        templateData = {
            'form' : registerForm
        }
        current_app.logger.info(request.form)

        if registerForm.validate() == False:
            current_app.logger.info(registerForm.errors)
            return "uhoh registration error"

        else:
            email = request.form['email']
            name = request.form['name']
            badgeid = request.form['badgeid']
            pwd = request.form['password']

            pwd=md5(pwd).hexdigest()

        # prepare User
        user=Users(badgeid=badgeid, email=email, password=pwd, keyword=[], doc=[], active=True, name=name)
        user.save()

        #try:
        if login_user(user, remember="no"):
            flash("Logged in!")
            return redirect('/list')
        else:
            flash("unable to log you in")
        #except:
        #    flash("unable to register with that email address")
        #    current_app.logger.error("Error on registration - possible duplicate emails")

        return render_template("posts/register.html", **templateData)

class InterestView(MethodView):
    def get_context(self, userid):
        up = UserProfile.objects.get_or_404(email=userid)
        context = {
            "up": up
        }

        return context

    @login_required
    def get(self):
        context = self.get_context(current_user.email)
        return render_template('posts/interest.html', **context)

    def post(self):
        userId=current_user.email
        userObj=UserProfile.objects.all()
        kwItem=request.form["keyword"]
        docItem=request.form["doc"]

        kwItem=kwItem.split(" ")
        docItem=docItem.split(" ")

        for uo in userObj:
            if(uo.email==userId):
                for k in kwItem:
                    if k not in uo.keyword:
                        uo.keyword.append(k)

                for d in docItem:
                    if d not in uo.doc:
                        uo.doc.append(d)
                try:
                    uo.save()
                    return redirect('/list')
                except:
                    flash("Unable to log1")
                    return render_template("/posts/interest.html")

        flash("Unable to log3")
        return render_template("/posts/interest.html")

class SearchView(MethodView):
    def get(self):
        return render_template("posts/search.html")

    def post(self):
        userId=current_user.email
        searchItem=request.form["kw"]

        kwList=searchItem.split()

        userObj=UserProfile.objects.all()
        ideaObj=Ideas.objects.all()

        ks=keywordSearch.KeywordSearch(kwList)
        
        docList=ks.doSearch()

        for uo in userObj:
            if(uo.email==userId):
                for k in kwList:
                    if k not in uo.keyword:
                        uo.keyword.append(k)

                try:
                    uo.save()
                    return render_template("posts/searchresult.html", docList=docList, ideas=ideaObj)
                except:
                    flash("Unable to log interest")
                    return render_template("/posts/search.html")



# Register the urls
posts.add_url_rule('/',view_func=LoginView.as_view('login'))
posts.add_url_rule('/logout',view_func=LogoutView.as_view('logout'))
posts.add_url_rule('/register',view_func=RegisterView.as_view('register'))
posts.add_url_rule('/list', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/<slug>/comment',view_func=CommentView.as_view('comment'))
posts.add_url_rule('/<slug>/rate',view_func=RateView.as_view('rate'))
posts.add_url_rule('/interest', view_func=InterestView.as_view('interest'))
posts.add_url_rule('/search', view_func=SearchView.as_view('search'))