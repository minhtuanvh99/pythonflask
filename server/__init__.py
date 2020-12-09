from flask import Flask
from config import Config
# use database with local uri
from flask_sqlalchemy import SQLAlchemy
# tranverse from local database to another database
from flask_migrate import Migrate

app = Flask(__name__)

# set database config
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# get all configuration of the app from config module 
app.config.from_object(Config)


from server import routes, models