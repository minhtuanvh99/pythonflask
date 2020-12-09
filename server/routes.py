from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from server import app, db
from server.forms import LoginForm, RegistrationForm
# working with flask-login
from flask_login import current_user, login_user, logout_user, login_required
from server.models import User


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


