import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = "secret"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
