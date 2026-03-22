from flask import Blueprint
from app.models.post import Post
from app.models.user import User
from functools import wraps
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from flask import request, render_template, redirect, url_for, session


profile = Blueprint("profile", __name__)




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function




@profile.route("/user/<username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(user_id=user.id).all()  #posts = user.posts
    return render_template("profile.html", user=user, posts=posts)




@profile.route("/profile")
@login_required
def my_profile():
    '''    
    if not session.get("user"):
        return redirect(url_for("login"))
    '''
    user = User.query.get(session["user_id"]); # db.session.get(User, session["user_id")
    username = user.username
    return redirect(url_for("profile.user_profile", username=username)) # username=session.get("user")






@profile.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    '''
    if not session.get("user_id"):
        return redirect(url_for("login"))
    '''
    user = User.query.get(session["user_id"]) # User.query.filter_by(username=session["user"]).first() # User.query.filter_by(username=session["user"])

    if request.method == "POST":
        new_username = request.form.get("username") # request.form["username"].strip()
        new_email = request.form.get("email") # request.form["email"].strip()
        new_bio = request.form.get("new_bio") # request.form["bio"].strip()
        pic = request.files.get("profile_pic") # request.files["profile_pic"]
        
        

        # Check if username already exists
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user.id:
            return "Username already in use!"
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=new_email).first()
        if existing_email and existing_email.id != user.id:
            return "Email already in use!"
        
        # Update username, email, bio
        user.username = new_username
        user.email = new_email
        user.bio = new_bio
            
                

        # Handle profile picture
        if pic and pic.filename != "":
            filename = secure_filename(pic.filename)
            pic.save(os.path.join("static/profile_pics", filename))
            user.profile_pic = filename

        db.session.commit()
            # Update session username if changed
        session["user"] = user.username

        return redirect(url_for("profile.user_profile", username=user.username))
        
    return render_template("edit_profile.html", user=user)




'''
        if new_username:
            user.username = new_username
            session["user"] = new_username

'''