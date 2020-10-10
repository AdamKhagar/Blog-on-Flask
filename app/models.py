from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    posts = db.relationship('Post', backref='author')

    def __repr__(self):
        '''return '<{}:{}>'.format(self.id, self.username)'''
        return '<{}:{}>'.format(self.id, self.username)

    def set_password(self, password):
        '''generate password hash and set'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''check password'''
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship('Post', backref='category')

    def __repr__(self):
        return (self.id, self.name)

    @staticmethod
    def get_list():
        return db.session.query(Category.id, Category.name).all()

post_tags = db.Table(
    'post_tags', 
    db.Column('post_id', db.Integer(), db.ForeignKey('posts.id')), 
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id')),
    extend_existing=True
)

class Tag(db.Model): 
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    @staticmethod
    def new_tags(tags: list):
        '''add tag into table tags if not exist'''
        old_tags_not_filter = db.session.query(Tag.name).all()
        old_tags = []

        for tags_tuple in old_tags_not_filter:
            old_tags.append(tags_tuple[0])

        for t in tags:
            if t not in old_tags:
                tag = Tag()
                tag.name = t
                db.session.add(tag)
        else: 
            db.session.commit()

    @staticmethod
    def get_tags(tags: list):
        tags_id_list = []
        for tag in tags:
            tags_id_list.append(db.session.query(Tag).filter(Tag.name == tag).first())

        return tags_id_list

class Post(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.DateTime(), default=datetime.utcnow())
    content = db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    # tags = db.relationship('Tag', secondary=post_tags, backref='posts')  

    def get(self):
        return {
            'id': self.id, 
            'title': self.title,
            'category_id': self.category_id,
            'pub_date': self.publication_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'content': self.content
        }
# db.metadata.clear()
db.create_all()