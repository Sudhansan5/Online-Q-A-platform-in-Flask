from flask import render_template, url_for, flash, redirect, request, abort
from flask_qa import app, db, bcrypt
from flask_qa.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
    QuestionForm, AnswerForm
from flask_qa.models import Users, Question, Answer
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    ques = Question.query.order_by(Question.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('home.html', ques=ques)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
            .decode('utf-8')
        user = Users(username=form.username.data,
                     email=form.email.data,
                     password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can log in now', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password again',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
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
    form = QuestionForm()
    if form.validate_on_submit():
        ques = Question(title=form.title.data,
                        content=form.content.data,
                        asker=current_user)
        db.session.add(ques)
        db.session.commit()
        flash('Your question has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_ques.html', title='New Question',
                           form=form, legend='New Question')


@app.route("/question/<int:question_id>")
def question(question_id):
    question = Question.query.get_or_404(question_id)
    answer = Answer.query.filter_by(ques_id=question_id).all()
    return render_template('question.html',
                           title=question.title,
                           question=question,
                           answer=answer)


@app.route("/question/<int:question_id>/update", methods=['GET', 'POST'])
@login_required
def update_question(question_id):
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
    question = Question.query.get_or_404(question_id)
    if question.asker != current_user:
        abort(403)
    Answer.query.filter_by(ques_id=question_id).delete()
    db.session.delete(question)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/question/<int:question_id>/answer", methods=['GET', 'POST'])
@login_required
def new_answer(question_id):
    form = AnswerForm()
    if form.validate_on_submit():
        ans = Answer(content=form.content.data,
                     ques_id=question_id,
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
    answer = Answer.query.get_or_404(answer_id)
    if answer.answerer != current_user:
        abort(403)
    db.session.delete(answer)
    db.session.commit()
    flash('Your answer has been deleted!', 'success')
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def permission_denied(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500
