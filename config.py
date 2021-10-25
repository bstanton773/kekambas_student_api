import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess...'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # sqlite:///c:\Documents\codingtemple-feb-2021\week5\feb_intro_to_flask\app.db
    SQLALCHEMY_TRACK_MODIFICATIONS = False