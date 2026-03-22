print("App starting")

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy




app = SQLAlchemy()


            
        
        


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


'''
from app import app, User, db
with app.app_context():
    # Create Initial admin admin user from python terminal once
    admin = User(username="admin", password="1234", email="admin@gmail.com", is_admin=True)
    db.session.add(admin)

    # Create a regular user if no registration route
    user1 = User(username="John", password="1234", is_admin=False)
    db.session.add(user1)

    db.session.commit()
'''


'''
# Updating existing admin user with hased password
from app import app, db, User
from werkzeug.security import generate_password_hash
with app.app_context():
    admin = User.query.filter_by(usernamr="admin").first()
    admin.password = generate_password_hash("1234")
    db.session.commit()
    db.create_all()
exit()
'''


'''
from app import app, db, User
from werkzeug.security import generate_password_hash
with app.app_context():
    hashed_pw = generate_password_hash("1234")
    admin = User(username="admin", password=hashed_pw, email="admin@gmail.com", is_admin=True)
    db.session.add(admin)
    db.session.commit()
'''