from flask import *
# from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session,sessionmaker,relationship,backref)
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


# db_uri = 'sqlite:///site.db'
# DATABASE_URL = 'sqlite:///site.db'
# SECRET_KEY = 'ashish'
# if environ:
DATABASE_URL = environ.get('DATABASE_URL')
SECRET_KEY = environ.get('SECRET_KEY')

engine = create_engine(DATABASE_URL,convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# db = SQLAlchemy(app)

from practice import routes