from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c240f2ec38f429adc14a1cd05beb0cdc'

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

if __name__ == '__main__':
    app.run(debug=True)
