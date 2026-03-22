from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from functools import wraps
from app.models.post import Post
from app.models.user import User
from app.extensions import db

posts = Blueprint("posts", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function



@posts.route("/add", methods=["GET", "POST"])
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

        return redirect(url_for("main.home"))
    
    return render_template("add_post.html", user=user)





#Dynamic route
@posts.route("/post/<int:post_id>")
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






@posts.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    '''
    if not session.get("user"):
        return redirect(url_for("login"))
'''
    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None
    

    post = Post.query.get_or_404(post_id)
    

    # Permission check
    if not (session.get("is_admin") or session.get("user_id") == post.user_id):
        return redirect(url_for("main.home"))

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        
        return redirect(url_for("posts.show_post", post_id=post.id))

    return render_template("edit_post.html", post=post, user=user)






@posts.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    '''
    if not session.get("user"):
        return redirect(url_for("login"))
'''
    post = Post.query.get_or_404(post_id)

     # Permission check
    if not (session.get("is_admin") or session.get("user") == post.author_obj.username):
        return redirect(url_for("main.home"))

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("main.home"))






@posts.route("/my_posts")
@login_required
def my_posts():
    '''
    if not session.get("user_id"):
        return redirect(url_for("login"))
'''
    user = User.query.get(session["user_id"])

    posts = user.posts
    return render_template("my_posts.html", user=user, posts=posts)