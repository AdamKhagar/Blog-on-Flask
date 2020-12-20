from . import db
from .models import User, Category, Post, Adminlist

# create users
def create_user(username, name, email, description, lastname='none', password='12345678', is_admin=False):
    user = User()
    user.username = username
    user.name = name
    if lastname != 'none':
        user.lastname = lastname
    user.set_password(password)
    user.email = email
    user.set_description(description)
    db.session.add(user)
    db.session.commit()

    if is_admin:
        admin = Adminlist()
        admin.user_id = user.id
        db.session.add(admin)
        db.session.commit()

def add_category(category_name):
    category = Category()
    category.name = category_name
    db.session.add(category)
    db.session.commit()

def add_post(tille, author, prev_text, text, tags, category):
    post = Post()
    post.title = title
    post.prev_text = prev_text
    post.content = text
    try: 
        category_id = db.session.query(Category.id) = 


