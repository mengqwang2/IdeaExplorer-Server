from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.cache import Cache
from flask.ext.bcrypt import Bcrypt
from flask.ext.cors import CORS
from flask.ext.mail import Mail, Message
from celery import Celery


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {"DB": "tumblelog"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config["CACHE_TYPE"]="simple"
CORS(app, resources={r'/api/*':{"origins": "*"}} ,allow_headers=['Authorization', 'Content-Type','Access-Control-Allow-Origin'])


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
	MAIL_USERNAME = 'emcmailassistant@gmail.com',
	MAIL_PASSWORD = 'emcmail123'
	)

flask_mail=Mail(app)

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)

flask_bcrypt = Bcrypt(app)


def register_blueprints(app):
    # Prevents circular imports
    from IdeaExplorer.views import posts
    app.register_blueprint(posts)

register_blueprints(app)
cache = Cache(app)

from IdeaExplorer import restserver

if __name__ == '__main__':
    app.run()
