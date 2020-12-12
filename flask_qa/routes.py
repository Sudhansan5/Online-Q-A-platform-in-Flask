from flask import render_template, url_for, flash, redirect, request
from flask_qa import app, db, bcrypt
from flask_qa.forms import RegistrationForm, LoginForm
from flask_qa.models import Users, Question, Answer
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
