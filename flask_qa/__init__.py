from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c240f2ec38f429adc14a1cd05beb0cdc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sudhan_flask:abc@localhost:5432/sudhan_flask'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_qa import routes