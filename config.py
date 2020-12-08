import os

# all config to application goes here
class Config(object):
    # Flask-WTF need to set a secret key => create a security token  
    # protect form from CRSF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abc-def-123'


