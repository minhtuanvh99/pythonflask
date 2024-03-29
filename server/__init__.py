from flask import Flask
from config import Config
# use database with local uri
from flask_sqlalchemy import SQLAlchemy
# tranverse from local database to another database
from flask_migrate import Migrate
# provide user session management, handle common tasks of login, logout, remember user session
from flask_login import LoginManager
#
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
#
from flask_mail import Mail
#
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
# 
from flask import request

app = Flask(__name__)

# get all configuration of the app from config module 
app.config.from_object(Config)

# set database config
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# set instance to flask login 
login = LoginManager(app)
# set a default page, if user request to a page which need to authentication
# redirect to this page
login.login_view = 'login'
#
mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
babel = Babel(app)

#
@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'vi'

# 
if not app.debug:
    # config mail
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Myblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    # write a log file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/myblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
 
    app.logger.setLevel(logging.INFO)
    app.logger.info('Myblog startup')


from server import routes, models, errors