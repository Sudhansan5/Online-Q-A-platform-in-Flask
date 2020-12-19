from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
from flask_qa.models import Users


class RegistrationForm(FlaskForm):
    '''
        Form for registration
    '''
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=16)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        '''
            This function checks if username is already present or not
        '''
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        '''
            This function checks if email is already present or not
        '''
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken.')


class LoginForm(FlaskForm):
    '''
        Form for login
    '''
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    '''
        Form for updating account information
    '''
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already taken.')


class QuestionForm(FlaskForm):
    '''
        Form to create a new question
    '''
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AnswerForm(FlaskForm):
    '''
        Form to create a new answer
    '''
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
