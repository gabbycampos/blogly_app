"""Blogly application."""

from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'thebloglyVsecretapp'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_users():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template('home.html', posts=posts)

@app.route('/users')
def display_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user():
    """ Displays Form """ 
    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """ Adds a new user """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['photo']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_user_by_id(user_id):
    """ Shows User Details """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id==user_id)
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Deletes a user """
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:user_id>/edit")
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)
    
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """ Edit a user """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['photo']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()
    return redirect('/users')

""" Posts """

@app.route('/users/<int:user_id>/posts/new')
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('add_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    return redirect('/users')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    return render_template('post_details.html', post=post, user=user)

@app.route("/posts/<int:post_id>/edit")
def edit_form_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    title = request.form["title"]
    content = request.form["content"]
 
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
    
    db.session.commit()
    return redirect('/users')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')