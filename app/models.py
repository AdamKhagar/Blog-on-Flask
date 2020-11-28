from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

class Model(db.Model):
    __abstract__ = True 
    
    def _get_dict(self, _dict=None, rels=False):
        # возвращает объект в dict
        if _dict is None or not isinstance(_dict, dict):
            _dict = {}
        
        columns = self.__table__.columns.keys()
        for key in columns:
            if not key.startswith('_'):
                _dict[key] = getattr(self, key)

        if rels:
            relationships = self.__table__.relationships.keys()
            for rel in relationships:
                if not rel.startswith('_'):
                    _dict[rel] = getattr(self.rel)

        return _dict

    def get_dict(self):
        # возвращает _get_dict()
        return self._get_dict()


class User(Model, UserMixin):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    _password_hash = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    _watched = db.relationship('PostView', backref='user', cascade='all,delete-orphan')
    _liked = db.relationship('PostLike', backref='user', cascade='all,delete-orphan')
    _disliked = db.relationship('PostDislike', backref='user', cascade='all,delete-orphan')
    _saved = db.relationship('SavePost', backref='user', cascade='all,delete-orphan')

    posts = db.relationship('Post', backref='author', cascade='all,delete-orphan')
    comments = db.relationship('Comment', backref='author', cascade='all,delete-orphan')

    def set_password(self, password:str):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password:str):
        return check_password_hash(self._password_hash, password)
    
    def watched_posts(self):
        print(self._watched.post_id)

    def add_post_to_history(self, post_id:int):
        if not post_id in db.session.query(PostView.post_id).filter(
                PostView.user_id == self.id):
            view = PostView()
            view.user_id = self.id
            view.post_id = post_id

            db.session.add(view)
            db.session.commit() 

    def get_posts(self):
        posts = db.session.query(Tag).filter(Tag.author_id == self.id).all()
        return [post.get() for post in posts]
        
    def get_dict(self):
        return super()._get_dict({'is_admin': self.is_admin})

    

    @property
    def is_admin(self):
        return db.session.query(Adminlist).filter(self.id == Adminlist.user_id).count() == 1

    @staticmethod
    def get_user_by_username(username: str):
        return db.session.query(User).filter(User.username == username).first()


class Subscription(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer(), primary_key=True)
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    subscriber_id = db.Column(db.Integer(), nullable=False)


class Adminlist(Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'adminlist'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    user = db.relationship('User', backref=db.backref("in_adminlist", uselist=False),\
            cascade='all,delete-orphan')

    @staticmethod
    def new_admin(new_admin: User, admin:User):
        if admin.is_admin:
            new_a = Adminlist
            new_a.user_id = new_admin.id
            db.session.add(new_a)
            db.session.commit()
            print("!new_admin:200")
        else:
            print("!new_admin:404")

class Blacklist(Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    blacklist_date = db.Column(db.DateTime(), default=datetime.utcnow())
    blacklist_period = db.Column(db.Integer(), nullable=False)

    user = db.relationship('User', backref=db.backref("in_blacklist", uselist=False), \
            cascade='all,delete-orphan')


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
        return db.session.query(Tag).filter(Tag.name in tags).all()


class PosteNotFoundError(Exception):
    pass

class SavePost(Model):
    __tablename__ = 'save_post'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


class PostView(Model):
    __tablename__ = 'post_views'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


class PostLike(Model):
    __tablename__ = 'post_likes'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


class PostDislike(Model):
    __tablename__ = 'post_dislikes'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


class Post(Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.DateTime(), default=datetime.utcnow())
    prev_text = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)

    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    _comments = db.relationship('Comment', backref="posts")
    
    @property
    def like_count(self):
        return db.session.query(PostLike).filter(PostLike.post_id == self.id).count()

    @property 
    def dislike_count(self): 
        return db.session.query(PostLike).filter(PostDislike.post_id == self.id).count()

    @property
    def view_count(self):
        return db.session.query(PostView).filter(PostView.post_id == self.id).count()

    @property
    def comment_count(self):
        return db.session.query(Comment).filter(Comment.post_id == self.id).count()

    @property
    def comments(self):
        return Comment.get_post_comments(self.id)

    def get_dict(self):
        return super()._get_dict(_dict={
            'author': self.author.username,
            'comments': self.comments,
            'views': self.view_count,
            'likes': self.like_count,
            'dislikes': self.dislike_count,
            'comment_count': self.comment_count,
            })
  
    @staticmethod
    def get(id:int):
        post = db.session.query(Post).filter(Post.id == id).first()
        if not isinstance(post, Post):
            raise PosteNotFoundError
        return post
 


class NotReplyedCommentError(Exception): pass


class Comment(Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    text = db.Column(db.String(), nullable=False)
    is_first = db.Column(db.Boolean(), default=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    def get_dict(self):
        d = {'author': self.author.username}
        if not self.is_first:
            d += self.reply_to

        return super()._get_dict(_dict=d)


    @property
    def reply_to(self):
        if self.is_first:
            raise NotReplyedCommentError
        replyed_comment = db.session.query(CommentToComment).filter(
                CommentToComment.comment_reply_id == self.id).first()
        
        return {'replyed_comment_author': replyed_comment.author.username, 
                'replyed_comment_id': replyed_comment.id}

    @classmethod
    def comment_post(cls, post_id: int, author_id:int, text: str):
        comment = cls()
        comment.post_id = post_id
        comment.author_id = author_id
        comment.text = text
        comment.is_first = True

        db.session.add(comment)
        db.session.commit()

        return comment.get_dict()

    @classmethod 
    def reply_comment(cls, post_id:int, author_id:int, text:str, comment_id:int):
        comment = cls()
        comment.post_id = post_id
        comment.author_id = author_id
        comment.text = text

        db.session.add(comment)
        db.session.commit()

        reply = CommentToComment()
        reply.comment_id = comment_id
        reply.comment_reply_id = comment.id

        db.session.add(reply)
        db.session.commit()

        return comment.get_dict()

    @staticmethod
    def get_post_comments(post_id: int):
        comments = db.session.query(Comment).filter(Comment.is_first).filter(Comment.post_id == post_id).all()
        comment_list = []
        for comment in comments:
            replyes_id = db.session.query(CommentToComment).filter(
                CommentToComment.comment_id == comment.id).all()
            replyes = [reply.get_dict() for reply in [db.session.query(Comment).filter(
                    Comment.id == id).all() for id in replyes_id]]
            comment_dict = comment.get_dict()
            comment_dict['childs'] = replyes 
            comment_list.append(comment_dict)

        return comment_list 
        

class CommentToComment(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'comment_to_comment'
    id = db.Column(db.Integer(), primary_key=True)
    comment_id = db.Column(db.Integer(), nullable=False)
    comment_reply_id = db.Column(db.Integer(), nullable=False)


db.create_all()