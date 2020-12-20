from flask import render_template, url_for, flash, redirect, request, abort
from flask_qa import app, db, bcrypt
from flask_qa.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
    QuestionForm, AnswerForm
from flask_qa.models import Users, Question, Answer
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    '''
    View for home
    '''
    page = request.args.get('page', 1, type=int)
    question = Question.query.order_by(Question.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('home.html', question=question)


@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
        View for register
    '''
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
            .decode('utf-8')
        user = Users(username=form.username.data,
                     email=form.email.data,
                     password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
        View for login
    '''
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password again',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    '''
        View for logout
    '''
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    '''
        View for account
    '''
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/question/new", methods=['GET', 'POST'])
@login_required
def new_question():
    '''
        View for new question
    '''
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data,
                            content=form.content.data,
                            asker=current_user)
        db.session.add(question)
        db.session.commit()
        flash('Your question has been created!', 'success')
        return redirect(url_for('question', question_id=question.id))
    return render_template('create_ques.html', title='New Question',
                           form=form, legend='New Question')


@app.route("/question/<int:question_id>")
def question(question_id):
    '''
        View for question
    '''
    question = Question.query.get_or_404(question_id)
    answer = Answer.query.filter_by(question_id=question_id).all()
    return render_template('question.html',
                           title=question.title,
                           question=question,
                           answer=answer)


@app.route("/question/<int:question_id>/update", methods=['GET', 'POST'])
@login_required
def update_question(question_id):
    '''
        View for updating question
    '''
    question = Question.query.get_or_404(question_id)
    if question.asker != current_user:
        abort(403)
    form = QuestionForm()
    if form.validate_on_submit():
        question.title = form.title.data
        question.content = form.content.data
        db.session.commit()
        flash('Your question has been updated!', 'success')
        return redirect(url_for('question', question_id=question.id))
    elif request.method == 'GET':
        form.title.data = question.title
        form.content.data = question.content
    return render_template('create_ques.html', title='Update Question',
                           form=form, legend='Update Question')


@app.route("/question/<int:question_id>/delete", methods=['POST'])
@login_required
def delete_question(question_id):
    '''
        View for deleting question
    '''
    question = Question.query.get_or_404(question_id)
    if question.asker != current_user:
        abort(403)
    Answer.query.filter_by(question_id=question_id).delete()
    db.session.delete(question)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/question/<int:question_id>/answer", methods=['GET', 'POST'])
@login_required
def new_answer(question_id):
    '''
        View for new answer
    '''
    form = AnswerForm()
    if form.validate_on_submit():
        ans = Answer(content=form.content.data,
                     question_id=question_id,
                     user_id=current_user.id)
        db.session.add(ans)
        db.session.commit()
        flash('Your answer has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_ans.html', title='New Answer',
                           form=form, legend='New Answer')


@app.route("/question/<int:question_id>/answer/<int:answer_id>/update",
           methods=['GET', 'POST'])
@login_required
def update_answer(question_id, answer_id):
    '''
        View for updating answer
    '''
    answer = Answer.query.get_or_404(answer_id)
    if answer.answerer != current_user:
        abort(403)
    form = AnswerForm()
    if form.validate_on_submit():
        answer.content = form.content.data
        db.session.commit()
        flash('Your answer has been updated!', 'success')
        return redirect(url_for('question', question_id=question_id))
    elif request.method == 'GET':
        form.content.data = answer.content
    return render_template('create_ans.html', title='Update answer',
                           form=form, legend='Update answer')


@app.route("/question/<int:question_id>/answer/<int:answer_id>/delete",
           methods=['GET', 'POST'])
@login_required
def delete_answer(question_id, answer_id):
    '''
        View for deleting answer
    '''
    answer = Answer.query.get_or_404(answer_id)
    if answer.answerer != current_user:
        abort(403)
    db.session.delete(answer)
    db.session.commit()
    flash('Your answer has been deleted!', 'success')
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    '''
    This function handles 404 error
    '''
    return render_template('404.html'), 404


@app.errorhandler(403)
def permission_denied(e):
    '''
    This function handles 403 error
    '''
    return render_template('403.html'), 403


@app.errorhandler(500)
def error_500(e):
    '''
    This function handles 500 error
    '''
    return render_template('500.html'), 500
