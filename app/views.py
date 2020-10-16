from flask import (
    render_template, request,
    redirect, url_for,
    flash, jsonify
)
from flask_login import (
    LoginManager, login_required,
    login_user, current_user,
    logout_user
)
from sqlalchemy.exc import IntegrityError
from app import app, db
from .models import User, Post, Category, Tag
from .forms import LoginForm, RegisterForm, PostForm


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/')
@app.route('/main/')
def main():
    return render_template('main.html', options=Category.get_list())


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = db.session.query(User).filter(
                User.username == form.username.data
                ).first()
                
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main'))
        
        flash('Invalid username/password', 'error')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

1234567890123456789012345678901234567890123456789012345678901234567890123456789
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = User()
        user.name = form.name.data
        if len(form.lastname.data) > 0:
            user.lastname = form.lastname.data
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        
        try: 
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash("The system already has an account with the same name and/or mail.")
            return redirect(url_for('register'))

        login_user(user, remember=form.remember.data)
        return redirect(url_for('main'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route('/licence')
def licence():
    return '<h2>Теперь мы будем продавать твои данные</h2>'


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit() and request.method == 'POST':
        post = Post()
        post.title = form.title.data
        post.category_id = form.category.data
        post.content = form.text.data
        post.author_id = current_user.get_id()

        tags = form.tags.data.split()

        Tag.new_tags(tags)
        post.tags.extend(Tag.get_tags(tags))
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('main'))
    return render_template('post.html', form=form)


@app.route('/get_posts/<category_id>', methods=['POST', 'GET'])
def get_posts(category_id): 
    if category_id.isdigit(): 
        category_id = int(category_id)
        posts = db.session.query(Post).filter(Post.category_id == category_id).all();      
    else:
        posts = db.session.query(Post).all()
    
    return {'posts': [post.get() for post in posts]}


@app.login_manager.unauthorized_handler
def unauth_handler():
    flash("Authorize please to access this page")
    return redirect(url_for("login"))

@app.route('/current_user_info')
@login_required
def get_current_user_info():
    user = db.session.query(User).filter(
        User.id == current_user.get_id()).first()
    return jsonify(user.get())

@app.route('/my_page')
@login_required
def get_my_page():
    pass

@app.route('/my_posts')
@login_required
def get_my_posts():
    pass