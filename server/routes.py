from flask import render_template, flash, redirect, url_for
from server import app
from server.forms import LoginForm


# home page route
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Tuan'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # get all components was defined in module forms.py 
    form = LoginForm()
    # handling form data if success go to homepage(index)
    if form.validate_on_submit():
        flash('Yeu cau dang nhap tu user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    # render login page, and pass form to view
    return render_template('login.html', title='Sign In', form=form)


