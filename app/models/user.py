from app.extensions import db
from datetime import datetime

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