import re
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, get_posts_list


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_of_users():
    """Shows list of users in db"""
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """Shows list of users in db"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_by_id(user_id):
    """Shows details about each user by user_id"""
    found_user = User.query.get_or_404(user_id)
    
    return render_template("user_detail.html", found_user=found_user)

@app.route('/users/new', methods=["GET"])
def new_users_form():
    """"""
    return render_template('users_form.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():
    """Retrieves form data, adds to database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user_by_id(user_id):
    """"""
    found_user = User.query.get_or_404(user_id)
    return render_template('user_detail_edit.html', found_user=found_user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def commit_edit_user_by_id(user_id):
    """"""
    found_user = User.query.get_or_404(user_id)

    found_user.first_name = request.form["first_name"]
    found_user.last_name = request.form["last_name"]
    found_user.image_url = request.form["image_url"]

    db.session.add(found_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user_by_id(user_id):
    """"""
    found_user = User.query.get_or_404(user_id)
    
    db.session.delete(found_user)
    db.session.commit()
    
    return redirect('/users')

#################
# Posts route

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    found_user = User.query.get_or_404(user_id)
    return render_template('post_form.html', found_user=found_user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post_detail_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
