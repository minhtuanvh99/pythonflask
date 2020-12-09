import os
basedir = os.path.abspath(os.path.dirname(__file__))

# all config to application goes here
class Config(object):
    # Flask-WTF need to set a secret key => create a security token  
    # protect form from CRSF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abc-def-123'
    # database config (sqlite)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    


