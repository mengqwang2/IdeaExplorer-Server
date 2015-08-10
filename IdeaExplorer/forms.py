import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from flask.ext.mongoengine.wtf.orm import validators

user_form = model_form(models.UserProfile, exclude=['password'])

# Signup Form created from user_form
class SignupForm(user_form):
    password = PasswordField('Password', validators=[validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

# Login form will provide a Password field (WTForm form field)
class LoginForm(user_form):
    password = PasswordField('Password',validators=[validators.Required()])
