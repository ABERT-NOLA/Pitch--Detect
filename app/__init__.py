from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
# Initializing Flask Extensions
bootstrap = Bootstrap(app)
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

from app.models import *
from app.views import *
