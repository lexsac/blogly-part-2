from models import db, User, Post
from app import app

#Create all tables
db.drop_all()
db.create_all()

u1 = User(id=1, first_name="lexsa", last_name="campbell", image_url="hi")
u2 = User(id=2, first_name="alex", last_name="s", image_url="yo")

p1 = Post(title="This is the title", content="This is the content", user_id=1)
p2 = Post(title="This is another title", content="This is more content", user_id=1)
p3 = Post(title="This is the title", content="This is the content", user_id=2)
p4 = Post(title="This is another title", content="This is more content", user_id=2)


db.session.add(u1)
db.session.add(u2)

db.session.commit()

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)

db.session.commit()