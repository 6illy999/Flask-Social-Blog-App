from app import create_app
from config import DevelopmentConfig

app = create_app()# app = create_app(DevelopmentConfig)

# Print all registered routes
for rule in app.url_map.iter_rules():
    print(rule)

if __name__  == "__main__":
    app.run()


#Run Migrations
'''
$env:FLASK_APP="run.py" or for Mac/Linux export FLASK_APP=run.py
flask db init - creates migration folder
flask db migrate -m "initial" - detects models - creates migration script
flask db upgrade - applies changes - creates tables in SQLite
'''

# updating
'''
flask db migrate -m "user model"
flask db upgrade
'''


# create database
'''
psql -U postgres
CREATE DATABASE trstdb - you can create both development and testing db

# Verify
#\l

flask db upgrade
'''