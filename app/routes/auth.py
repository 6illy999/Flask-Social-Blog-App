from app.extensions import db
from flask import Blueprint, request, render_template, redirect, url_for, session
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

auth = Blueprint("auth", __name__)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function



@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username") # request.form["username"]
        password = request.form.get("password") # request.form["password"]
        email = request.form.get("email") # request.form["email"]

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already taken!"
        
        # Add user (not admin by default)
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email, is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))
    
    return render_template("register.html")






    

@auth.route("/login", methods=["GET", "POST"])
def login():
    '''
    if "user_id" not in session:
        return redirect(url_for("login"))
    '''


    if request.method == "POST":
        username = request.form.get("username") # request.form["username"]
        password =request.form.get("password") # request.form["password"]

        '''if username == "admin" and password == "1234":
            session["user"] = username'''
        
        # Query user from database
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password): # if user and user.password == password
            session["user_id"] = user.id
            session["user"] = user.username
            session["is_admin"] = user.is_admin
            return redirect(url_for("main.home"))
        else:
            if user and not check_password_hash(user.password, password):
                return "wrong password"
            else:
                return "no such user"
        
    return render_template("login.html")




@auth.route("/logout")
def logout():

    if "user" in session:
        session.clear()
    '''
        session.pop("user", None)
        session.pop("is_admin", None)
        '''
    return redirect(url_for("main.home"))




@auth.route("/pass_change", methods=["GET", "POST"])
@login_required
def change_pass():
    min_pass_len = 4

    user = User.query.get(session["user_id"]) # User.query.filter_by(username=session["user"]).first() # User.query.filter_by(username=session["user"])


    if request.method == "POST":
        new_password = request.form.get("new_password") # request.form["new_password"]
        current_password = request.form.get("current_password") # request.form["current_pasword"]

          # Check password (only if fields filled)
        if current_password and new_password:
            if not check_password_hash(user.password, current_password):
                return "Current password is incorrect!"
                

            if len(new_password) < min_pass_len:
                return "Password must be at least 4 characters."

            if check_password_hash(user.password, new_password):
                return "You can't use your old password!"
            
            user.password = generate_password_hash(new_password)

            db.session.commit()

        return redirect(url_for("profile.user_profile", username=user.username))
        
    return render_template("change_pass.html", user=user)