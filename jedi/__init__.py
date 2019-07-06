from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '9c4c971e249b5f90558bf749515acc8c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt()

login_manger = LoginManager(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'danger'

from jedi import routes
