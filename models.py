import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# Models go below! 

class User(db.Model):
    """User."""

    @classmethod
    def get_by_species(cls, last_name):
        return cls.query.filter_by(last_name=last_name).all()
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=True) 

    def __repr__(self):

        p = self
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>" 


class Post(db.Model):
    """Post."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts')

    def __repr__(self):

        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} date={p.created_at} user={p.user_id}>" 


def get_posts_list():
    all_posts = Post.query.all()
    
    for post in all_posts:
        print(post.title, post.content, post.user.first_name, post.user.last_name)