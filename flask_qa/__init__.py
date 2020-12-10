from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c240f2ec38f429adc14a1cd05beb0cdc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sudhan_flask:abc@localhost:5432/sudhan_flask'
db = SQLAlchemy(app)

from flask_qa import routes