print("App starting")

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


app = Flask(__name__, static_folder="static")

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'dev_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_obj = db.relationship('User', backref='posts')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    posts = Post.query.all()
    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None

    return render_template("index.html", posts=posts, user=user)

@app.route("/about")
def about():

    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None

    return render_template("about.html", user=user)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_post():

    
    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None
    '''if "user" not in session:
        return redirect(url_for("login"))'''
    
    '''if session.get("user") != "admin": # if not session.get("is_admin")
        return redirect(url_for("home"))'''
        
    '''  
        if not session.get("user"): # User_id?
            return redirect(url_for("login"))
    '''
    if request.method == "POST":
        title = request.form.get("title") # request.form["title"]
        content = request.form.get("content") # request.form["content"]
       

        new_post = Post(title=title, content=content, user_id=session["user_id"])
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("home"))
    
    return render_template("add_post.html", user=user)

#Dynamic route
@app.route("/post/<int:post_id>")
@login_required
def show_post(post_id):

    
    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None

    ''' 
    if not session.get("user"): # User_id?
        return redirect(url_for("login"))
    '''
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post, user=user)


@app.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("home"))
        else:
            return "Invalid credentials"
        
    return render_template("login.html")
    

@app.route("/logout")
def logout():

    if "user" in session:
        session.clear()
    '''
        session.pop("user", None)
        session.pop("is_admin", None)
        '''
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():

    
    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None
    
    return render_template("dashboard.html", user=user)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    bio = db.Column(db.Text, default="Hello! I'm new here.")
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    #posts = db.relationship("Post", backref='author_obj', lazy=True)
    profile_pic = db.Column(db.String(200), default="default.svg")



@app.route("/register", methods=["GET", "POST"])
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

        return redirect(url_for("login"))
    
    return render_template("register.html")



@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    '''
    if not session.get("user"):
        return redirect(url_for("login"))
'''
    post = Post.query.get_or_404(post_id)

    # Permission check
    if not (session.get("is_admin") or session.get("user_id") == post.user_id):
        return redirect(url_for("home"))

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("edit_post.html", post=post)


@app.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    '''
    if not session.get("user"):
        return redirect(url_for("login"))
'''
    post = Post.query.get_or_404(post_id)

     # Permission check
    if not (session.get("is_admin") or session.get("user") == post.author_obj.username):
        return redirect(url_for("home"))

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))



@app.route("/user/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(user_id=user.id).all()  #posts = user.posts
    return render_template("profile.html", user=user, posts=posts)


@app.route("/profile")
@login_required
def my_profile():
    '''    
    if not session.get("user"):
        return redirect(url_for("login"))
    '''
    user = User.query.get(session["user_id"]); # db.session.get(User, session["user_id")
    username = user.username
    return redirect(url_for("profile", username=username)) # username=session.get("user")


@app.route("/my_posts")
@login_required
def my_posts():
    '''
    if not session.get("user_id"):
        return redirect(url_for("login"))
'''
    user = User.query.get(session["user_id"])

    posts = user.posts
    return render_template("my_posts.html", user=user, posts=posts)



@app.route("/edit-profile", methods=["GET", "POST"])
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

        return redirect(url_for("profile", username=user.username))
        
    return render_template("edit_profile.html", user=user)

@app.route("/pass_change", methods=["GET", "POST"])
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

        return redirect(url_for("profile", username=user.username))
        
    return render_template("change_pass.html", user=user)


'''
        if new_username:
            user.username = new_username
            session["user"] = new_username

'''
            
        
        


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