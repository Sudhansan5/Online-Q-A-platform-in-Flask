from flask import render_template, url_for, flash, redirect
from flask_qa import app
from flask_qa.forms import RegistrationForm, LoginForm
from flask_qa.models import Users, Question, Answer


ques = [
    {
        'asker': 'Sudhanshu',
        'title': 'Question 1',
        'question': 'First question',
        'date_posted': 'December 8, 2020'
    },
    {
        'asker': 'Anish',
        'title': 'Question 2',
        'question': 'Second question',
        'date_posted': 'April 1, 2019'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', ques=ques)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'sudhansan5@gmail.com' and form.password.data == 'abc':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password and try again!', 'danger')
    return render_template('login.html', title='Login', form=form)
