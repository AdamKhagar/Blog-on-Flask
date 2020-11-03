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
    is_admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<{}:{}>'.format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_user_by_username(username: str):
        return db.session.query(User).filter(User.username == username).first()

    def get(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "username": self.username, 
            "email": self.email
        }

    def get_posts(self):
        posts = db.session.query(Tag).filter(Tag.author_id == self.id).all()
        return [post.get() for post in posts]


class Blacklist(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'blacklist'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True,  nullable=False)
    user = db.relationship('User', backref=db.backref("in_blacklist", uselist=False))
    blacklist_date = db.Column(db.DateTime(), default=datetime.utcnow())
    blacklist_period = db.Column(db.Integer(), nullable=False)


class Category(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship('Post', backref='category', cascade='all,delete-orphan')


    @staticmethod
    def get_list():
        return db.session.query(Category.id, Category.name).all()
        
    @staticmethod
    def get_dict_list():
        db_responce = db.session.query(Category.id, Category.name).all()
        return [{'key': key, 'value': value} for key, value in db_responce]


post_tags = db.Table('post_tags', 
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
            tags_id_list.append(
                    db.session.query(Tag).filter(Tag.name == tag).first())

        return tags_id_list


class Post(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    images = db.relationship('Image', backref='posts')
    publication_date = db.Column(db.DateTime(), default=datetime.utcnow())
    prev_text = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    views = db.Column(db.Integer(), default=0)
    likes = db.Column(db.Integer(), default=0)
    dislikes = db.Column(db.Integer(), default=0)

    def get(self): 
        res = {
            'id': self.id, 
            'title': self.title,
            'category_id': self.category_id,
            'pub_date': self.publication_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'author': db.session.query(User.username).filter(
                User.id == self.author_id).first()[0],
            'views': self.views,
            'likes': self.likes, 
            'dislikes': self.dislikes,
            'prev_content': self.prev_text,
            'content': self.content
        }
        return res

    @staticmethod
    def get_by_id(post_id):
        return db.session.query(Post).filter(Post.id == post_id).first().get()


class Image(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'images'
    id = db.Column(db.Integer(), primary_key=True)
    sequence_num = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    post = db.Column(db.Integer(), db.ForeignKey('posts.id'))

# db.metadata.clear()
db.create_all()