# from logging import DEBUG

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from . import app, db, login_manager
from .forms import BookmarkForm, LoginForm, SignupForm
from .models import User, Bookmark

# app.logger.setLevel(DEBUG)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored: '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome {}!, Please login'.format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # app.logger.debug('You hit the page')
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user:
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('Incorrect username or password.')
        # else:
        # app.logger.debug('User issue')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html'), 404  # returns tuple that includes status code for the page failing to do so will prevent flask \
    # from setting the correct status code one the return


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500  # debug needs to be turned off to hit 500
