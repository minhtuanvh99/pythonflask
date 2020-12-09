from flask import Flask
from config import Config
# use database with local uri
from flask_sqlalchemy import SQLAlchemy
# tranverse from local database to another database
from flask_migrate import Migrate
# provide user session management, handle common tasks of login, logout, remember user session
from flask_login import LoginManager

app = Flask(__name__)

# set database config
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# set instance to flask login 
login = LoginManager(app)
# set a default page, if user request to a page which need to authentication
# redirect to this page
login.login_view = 'login'

# get all configuration of the app from config module 
app.config.from_object(Config)


from server import routes, models