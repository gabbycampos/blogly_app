"""Blogly application."""

from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    """ Shows list of users """
    return render_template('home.html')

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
    return render_template('user_details.html', user=user)

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