from flask import Blueprint # modular routing system, Helps split app into parts (auth, api, etc.)
from flask import render_template, redirect, url_for, session
from functools import wraps
from app.models.post import Post
from app.models.user import User
from app.extensions import db

main = Blueprint("main", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function




@main.route("/")
def home():
    posts = Post.query.all()
    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None


    return render_template("index.html", posts=posts, user=user)





@main.route("/about")
def about():

    if "user" in session:
        user = User.query.get(session.get("user_id"))
    else:
        user = None

    return render_template("about.html", user=user)





