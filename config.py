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
    # email config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    # some of post in one page
    POSTS_PER_PAGE = 3
    # list language is suppported
    LANGUAGES = ['en', 'vi']
