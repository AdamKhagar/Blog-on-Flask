from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, func, text, delete, insert


class Model(db.Model):
    __abstract__ = True 
    
    def _get_dict(self, _dict=None, rels=False):
        if _dict is None or not isinstance(_dict, dict):
            _dict = {}
        
        columns = self.__table__.columns.keys()
        for key in columns:
            if not key.startswith('_'):
                _dict[key] = getattr(self, key)

        return _dict

    def get_dict(self):
        return self._get_dict()


class SavePost(Model):
    __tablename__ = 'save_post'
     
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)


class PostView(Model):
    __tablename__ = 'post_views'

    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)


class PostLike(Model):
    __tablename__ = 'post_likes'
     
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)


class PostDislike(Model):
    __tablename__ = 'post_dislikes'

    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)


subscriptions = db.Table('subscriptions',
    db.Column("author_id", db.Integer(), db.ForeignKey('users.id'), primary_key=True),
    db.Column("user_id", db.Integer(), db.ForeignKey('users.id'), primary_key=True)
)

class User(Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    _password_hash = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    _description = db.Column(db.String())

    _watched = db.relationship('Post', secondary="post_views", backref='watcher')
    _liked = db.relationship('Post', secondary="post_likes", backref='liker')
    _disliked = db.relationship('Post', secondary="post_dislikes", backref='disliker')
    _saved = db.relationship('Post', secondary="save_post", backref='saver')
    posts = db.relationship('Post', backref='author', cascade='all,delete-orphan')
    comments = db.relationship('Comment', backref='author', cascade='all,delete-orphan')
    subscriptions = db.relationship('User', 
        secondary=subscriptions,
        primaryjoin="User.id == subscriptions.c.user_id", 
        secondaryjoin="User.id == subscriptions.c.author_id")

    def __repr__(self):
        return '< @{} >'.format(self.username)

    def set_password(self, password:str):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password:str):
        return check_password_hash(self._password_hash, password)
    
    def watched_posts(self):
        print(self._watched.post_id)

    def get_post_score(self, post_id):
        post = Post.query.get(post_id)
        is_watched = False
        is_liked = False
        is_disliked = False
        if post in self._watched:
            is_watched = False
        if post in self._liked:
            is_liked = True
        elif post in self._disliked:
            is_disliked = True

        return {
            "is_watched": is_watched,
            "is_liked": is_liked,
            "is_disliked": is_disliked
        }

    def add_post_to_history(self, post):
        if db.session.query(PostView).filter(PostView.post_id == post.id).\
                filter(PostView.user_id == self.id).count() == 0:
            view = PostView()
            view.post_id = post.id 
            view.user_id = self.id

            db.session.add(view)
            db.session.commit()

    def like_post(self, post_id):
        post = Post.get(post_id)
        if post not in self._liked:
            self._liked.append(post)
            db.session.add(self)
            db.session.commit()

            if post in self._disliked:
                self.dislike_post(post_id)

            return True
        else:
            post_like = db.session.query(PostLike).\
                    filter(PostLike.post_id == post_id).\
                    filter(PostLike.user_id == self.id).first()
            db.session.delete(post_like)
            db.session.commit()
            return False

    def dislike_post(self, post_id):
        post = Post.get(post_id)
        if post not in self._disliked:
            self._disliked.append(post)
            db.session.add(self)
            db.session.commit()

            if post in self._liked:
                self.like_post(post_id)

            return True
        else:
            post_dislike = db.session.query(PostDislike).\
                    filter(PostDislike.post_id == post_id).\
                    filter(PostDislike.user_id == self.id).first()

            db.session.delete(post_dislike)
            db.session.commit()
            return False

    def like_comment(self, comment_id):
        comment = Comment.get(comment_id)  
        if comment not in self.liked_comment:
            self.liked_comment.append(comment)
            db.session.add(self)
            db.session.commit()
        else:
            like = db.session.query(comment_like).\
                    filter(comment_like.c.comment_id == comment_id).\
                    filter(comment_like.c.user_id == self.id).first()
            
            db.session.delete(like)
            db.session.commit()
        
        return db.session.query(comment_like).\
                filter(comment_like.c.comment_id).count()

    def get_posts(self):
        posts = db.session.query(Tag).filter(Tag.author_id == self.id).all()
        return [post.get_dict() for post in posts]
        
    def get_dict(self):
        return super()._get_dict({
            'is_admin': self.is_admin
        })
    
    def add_subscribe(self, subscribe_id):
        self.subscriptions.append(User.query.get(subscribe_id))
        db.session.commit()

        return len(self.subscriptions)

    def del_subscribe(self, subscribe_id):
        stmt = (
            delete(subscriptions).\
            where(subscriptions.c.user_id == self.id).
            where(subscriptions.c.author_id == subscribe_id)
        )
        db.engine.execute(stmt)
        db.session.commit()
        return True

    def get_subscribers(self):
        return [x.get_dict() for x in db.session.query(subscriptions).\
                filter(subscriptions.c.author_id == self.id).all()]

    def get_subscribes(self):
        return [x.get_dict for x in self.subscriptions]

    def get_user_posts(self):
        posts = db.session.query(Post, func.count(PostLike.user_id).label("total")).\
                outerjoin(PostLike).group_by(Post.id).filter(Post.author_id == self.id).\
                order_by(text("total DESC")).all()

        return [post.get_dict()for post, _ in posts]

    def set_description(self, description):
        self._description = description
        db.session.add(self)
        db.session.commit()
        
    def get_description(self):
        return self._description

    @property
    def is_admin(self):
        return db.session.query(Adminlist).filter(self.id == Adminlist.user_id).count() == 1

    @staticmethod
    def get_user_by_username(username: str):
        return db.session.query(User).filter(User.username == username).first()


class Adminlist(Model):
    __tablename__ = 'adminlist'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref("in_adminlist", uselist=False))


class Blacklist(Model):     
    __tablename__ = 'blacklist'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    blacklist_date = db.Column(db.DateTime(), default=datetime.utcnow())
    blacklist_period = db.Column(db.Integer(), nullable=False)

    user = db.relationship('User', backref=db.backref("in_blacklist", uselist=False))


class Category(db.Model):
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
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id'))
)


class Tag(db.Model):    
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


class PosteNotFoundError(Exception):pass

class Post(Model):
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
        return len(self.liker)

    @property 
    def dislike_count(self): 
        return len(self.disliker)

    @property
    def view_count(self):
        return len(self.watcher)

    @property
    def comment_count(self): 
        return len(self._comments)

    def get_dict(self):
        return super()._get_dict(_dict={
            'author': self.author.username,
            # 'comments': [Comment.get_post_comments(self.id)],
            'views': self.view_count,
            'likes': self.like_count,
            'dislikes': self.dislike_count,
            'comment_count': len(self._comments),
            'tags': [tag.name for tag in self.tags]
        })

    def add_tags(self, tags):
        Tag.new_tags(tags)
        self.tags.extend(Tag.get_tags(tags))
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id:int):
        post = db.session.query(Post).filter(Post.id == id).first()
        return post
 

class NotReplyedCommentError(Exception): pass


comment_like = db.Table('comment_like', 
    db.Column('comment_id', db.Integer(), db.ForeignKey('comments.id'), primary_key=True),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), primary_key=True)
)


reply_comment = db.Table('reply_comment', 
    db.Column('comment_id', db.Integer(), db.ForeignKey('comments.id'), primary_key=True),
    db.Column('reply_id', db.Integer(), db.ForeignKey('comments.id'), primary_key=True)
)


class Comment(Model): 
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    text = db.Column(db.String(), nullable=False)
    is_first = db.Column(db.Boolean(), default=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    likers_user = db.relationship('User',
        secondary=comment_like, backref='liked_comment'
    )
    replyes = db.relationship('Comment',
        secondary=reply_comment,
        primaryjoin='Comment.id == reply_comment.c.comment_id',
        secondaryjoin='Comment.id == reply_comment.c.reply_id'
    )   

    def get_dict(self):
        d = {'author': self.author.username}
        if not self.is_first:
            comment_id = db.session.query(reply_comment.c.comment_id).\
                filter(reply_comment.c.reply_id == self.id).first()[0]
            comment = db.session.query(Comment).get(comment_id)
            d["replyed_c_author"] = comment.author.username
            d["replyed_c_id"] = comment_id

        return super()._get_dict(_dict=d)
    
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
        comment = db.session.query(Comment).get(comment_id)

        reply = cls()
        reply.text = text
        reply.post_id = post_id
        reply.author_id = author_id

        db.session.add(reply)
        db.session.commit()

        comment.replyes.append(reply)

        db.session.add(comment)
        db.session.commit()

        return reply.get_dict()
    

    @staticmethod
    def get_post_comments(post_id: int):
        comments = db.session.query(Comment, func.count(comment_like.c.user_id).label('total')).\
            outerjoin(comment_like).group_by(Comment).filter(Comment.post_id == post_id).\
            filter(Comment.is_first == True).order_by(text('total DESC')).all()

        comments_list = []

        def get_all_replyes(comment):
            replyes_id_list = db.session.query(reply_comment.c.reply_id).\
                    filter(reply_comment.c.comment_id == comment.id).all()

            replyes_list = []
            for reply_id in replyes_id_list:
                reply = db.session.query(Comment).get(reply_id)
                replyes_list.append(reply.get_dict())
                replyes_list += get_all_replyes(reply)
                
            return replyes_list

        for comment, _ in comments:
            comment_d = comment.get_dict()
            replyes = get_all_replyes(comment)
            
            comment_d['replyes'] = replyes

            comments_list.append(comment_d)

        return comments_list



db.create_all()