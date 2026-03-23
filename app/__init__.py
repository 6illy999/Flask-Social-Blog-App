from flask import Flask
from app.extensions import db#, migrate
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates") # Create Flask app instance

    #print("CONFIG CLASS:", config_class)

    #load configuration
    app.config.from_object("config.DevelopmentConfig")

    '''
    db_url = app.config["SQLALCHEMY_DATABASE_URI"]

    # fix render postgres:// issue
    if db_url.startswith("postgre://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

'''

    
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("RAW VALUE: ", DevelopmentConfig.SQLALCHEMY_DATABASE_URI)

    # connect extensions to app
    db.init_app(app) # connect database to app
    #migrate.init_app(app, db) # connect migration system

    from app import models

    # register routes (blueprints)
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.posts import posts
    from app.routes.profile import profile

    app.register_blueprint(main)
    app.register_blueprint(auth)  # /auth/login or /auth/register
    app.register_blueprint(posts)
    app.register_blueprint(profile)

    print(db.metadata.tables.keys())

    return app