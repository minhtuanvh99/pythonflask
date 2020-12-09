from server import app, db
from server.models import User, Post


# working with flash shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


