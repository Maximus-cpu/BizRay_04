import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False