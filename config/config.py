# config/config.py
import os

curr_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(curr_dir, '../Database')
    # Change 'housing.db' to your desired DB filename, e.g., 'gaitguard.db'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, 'user.db')
    DEBUG = True
    SECRET_KEY = "group4_gaitguard_unique_secret_key"
    # Optional security configurations:
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'gaitguard_unique_salt'
