import os
# from dotenv import load_dotenv

# Seperate configurations from code
# allows different environments (dev vs production)

#load_dotenv() # Loads variables from .env into os.environ


class Config:
    #configure database using environment variable
    #SECRET_KEY = os.environ.get("SECRET_KEY", 'dev_secret_key')
    SECRET_KEY = 'dev_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    #SQALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", 'sqlite:///blog.db')

    # disables unnecessary tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False