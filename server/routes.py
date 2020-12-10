from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from server import app, db
from server.forms import LoginForm, RegistrationForm, EditProfileForm
# working with flask-login
from flask_login import current_user, login_user, logout_user, login_required
from server.models import User
from datetime import datetime


# .before_request: have to run this after call display function
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# home page route
@app.route('/')
@app.route('/index')
@login_required # user cannot access this route if user has not login
def index():
    posts = [
        {
            'author': {'username': 'Nguyen'},
            'body': 'Flask de hoc qua phai khong?'
        },
        {
            'author': {'username': 'Long'},
            'body': 'Lap trinh Web that thu vi!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


# profile page
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Bài viết #1'},
        {'author': user, 'body': 'Bài viết #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('index'))
    # get all components was defined in module forms.py 
    form = LoginForm()
    # handling form data if success go to homepage(index)
    if form.validate_on_submit():
        # get matched user from database
        user = User.query.filter_by(username=form.username.data).first()
        # handling error if user is not exist
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # if user exist create a session and remember user has logged in to flask-form, go homepage 
        login_user(user, remember=form.remember_me.data)
        # next param is showed in the uri: /login?next=/index, its been when user is logged in, go to homepage    
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    # render login page, and pass form to view
    return render_template('login.html', title='Sign In', form=form)


# logout 
@app.route('/logout')
def logout():
    # destroy session of user in server
    logout_user()
    return redirect(url_for('index'))


# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# edit profile route
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
