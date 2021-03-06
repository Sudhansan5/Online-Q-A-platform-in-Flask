from datetime import datetime
from flask_qa import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    '''
    This function login the user
    '''
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    '''
        Table Schema for Users table
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    asked_question = db.relationship('Question', backref='asker', lazy=True)
    given_answer = db.relationship('Answer', backref='answerer', lazy=True)

    def __repr__(self):
        return f"Users('{self.username}', '{self.email}')"


class Question(db.Model):
    '''
        Table Schema for Question table
    '''
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self):
        return f"Question('{self.title}', '{self.date_posted}')"


class Answer(db.Model):
    '''
        Table Schema for Answer table
    '''
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer,
                            db.ForeignKey('question.id'),
                            )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Answer('{self.content}', '{self.date_posted}')"
