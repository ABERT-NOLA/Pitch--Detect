from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
# Initializing Flask Extensions
bootstrap = Bootstrap(app)

from app.models import *
from app.views import *
