import datetime
from flask import url_for
from IdeaExplorer import db

#Embedded field for the innovator field in Table <Ideas>
class Innovator(db.EmbeddedDocument):
    badge_no=db.IntField(required=True)
    name=db.StringField(max_length=255, required=True)
    email=db.EmailField(max_length=255, required=True)

#Table Ideas
class Ideas(db.DynamicDocument):
    updated_date=db.DateTimeField(default=datetime.datetime.now, required=True)
    likes=db.BooleanField(default=False)
    innovation_doc=db.ListField(db.StringField(max_length=30))
    id=db.IntField(required=True)
    relevance_to_challenge=db.StringField(required=True)
    title=db.StringField(required=True)
    who_locked=db.ListField(db.StringField(max_length=30))
    innovators=db.ListField(db.EmbeddedDocumentField('Innovator'))
    status=db.StringField(required=True)
    description=db.StringField(required=True)
    tags=db.StringField(required=True)
    idea_history=db.StringField(required=True)
    status_date=db.DateTimeField(default=datetime.datetime.now, required=True)
    from_combined=db.BooleanField(default=False)
    contest_id=db.IntField(required=True)
    disposition=db.StringField(required=True)
    practical_problem_solved=db.StringField(required=True)
    likes_count=db.IntField(required=True)
    locked=db.StringField(required=True)
    sends_count=db.IntField(required=True)
    submit_date=db.DateTimeField(default=datetime.datetime.now, required=True)
    type_of_innovation=db.StringField(required=True)
    success_benefit=db.StringField(required=True)
    comments_count=db.IntField(required=True)
    submitter=db.EmailField(max_length=255, required=True)

#Table Users for login to the mobile platform
class UserProfile(db.DynamicDocument):
    email=db.EmailField(max_length=255, required=True)
    badgeid=db.StringField(max_length=255, required=True)
    password=db.StringField(max_length=255, required=True)
    name=db.StringField(max_length=255, required=True)
    keyword=db.ListField(db.StringField(max_length=30))
    doc=db.ListField(db.IntField())
    created_at=db.DateTimeField(default=datetime.datetime.now, required=True)
    active = db.BooleanField(default=True)

    meta={
        'indexes': [
            {'fields': ['email'], 'unique': True}
        ]
    }

#Embedded field for Table <UserPost> record
class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    content = db.StringField(required=True)
    user = db.ReferenceField('UserProfile',required=True)

#Embedded field for Table <UserPost> record
class Rate(db.EmbeddedDocument):
    create_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    rating = db.IntField(required=True)
    user = db.ReferenceField('UserProfile',required=True)

#Table for writting down user posts
class UserPost(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    docid = db.IntField(required=True)
    avgrate = db.IntField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    rate = db.ListField(db.EmbeddedDocumentField('Rate'))
    slug = db.StringField(max_length=255, required=True)
    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    @property
    def post_type(self):
        return self.__class__.__name__

    meta={
        'allow_inheritance': True,
        'indexes': [
            {'fields': ['docid'], 'unique': True}
        ],
        'ordering': ['docid']
    }

#Table for Document-Tags 
class DocTag(db.DynamicDocument):
    docid = db.IntField(required=True)
    tags = db.ListField(db.StringField(max_length=255))

#Table for Tag-Documents
class TagDoc(db.DynamicDocument):
    tag = db.StringField(max_length=255)
    docid = db.ListField(db.IntField(required=True))

#Table for LDA Gamma - Document-Gamma
class GammaDT(db.DynamicDocument):
    docid=db.IntField(required=True)
    gamma=db.ListField(db.FloatField(required=True))

#Embedded field for GammaTD below
class DocGamma(db.EmbeddedDocument):
    docid=db.IntField(required=True)
    gamma=db.FloatField(required=True)

#Table for LDA Gamma - Topic-Gamma 
class GammaTD(db.DynamicDocument):
    topicid=db.IntField(required=True)
    gam=db.ListField(db.EmbeddedDocumentField('DocGamma'))

#Embedded field for DocSim
class Similarity(db.DynamicDocument):
    docid=db.IntField(required=True)
    sim=db.FloatField(required=True)

#Table for Inter-document Similarity
class DocSim(db.DynamicDocument):
    docid=db.IntField(required=True)
    similarity=db.ListField(db.EmbeddedDocumentField('Similarity'))

#Table for LDA Lambda - Topic-Lambda
class LambdaTW(db.DynamicDocument):
    topicid=db.IntField(required=True)
    lam=db.ListField(db.FloatField(required=True))

#Table for LDA Lambda - Word-Lambda
class LambdaWT(db.DynamicDocument):
    wordid=db.IntField(required=True)
    lam=db.ListField(db.FloatField(required=True))

#Table for LDA dictionary
class Vocab(db.DynamicDocument):
    vid=db.IntField(required=True)
    word=db.StringField(max_length=255, required=True)

