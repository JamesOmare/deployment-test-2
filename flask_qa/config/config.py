import os
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'q&a.db')
    DEBUG = config('DEBUG', cast = bool)
  
