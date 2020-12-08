from flask import Flask
from config import Config

app = Flask(__name__)

# get all configuration of the app from config module 
app.config.from_object(Config)


from server import routes