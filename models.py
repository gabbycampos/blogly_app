"""Models for Blogly."""
# First, create a User model for SQLAlchemy. Put this in a models.py file.

# It should have the following columns:

# id, an autoincrementing integer number that is the primary key
# first_name and last_name
# image_url for profile images

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE = "/static/images/default.jpg"

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS
class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __repr__(self):
        return f'{self.full_name} {self.image_url} has been created successfully! Date: {self.date_created}'

class Post(db.Model):
    __tablename__ = "posts" 

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #relationships
    users = db.relationship("User", backref=db.backref("posts", cascade="all,delete"))

    def __repr__(self):
        return f'<Post: {self.title}, {self.content}, {self.created_at}>'
        
class Tag(db.Model):
    __tablename__ = "tags" 

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(25), unique = True)

    # relationships
    posts = db.relationship("Post", secondary="posts_tags", backref=db.backref("tags"))

class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True, nullable=False)