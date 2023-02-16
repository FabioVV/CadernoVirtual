import os
import uuid as uuid
from datetime import datetime

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from itsdangerous import URLSafeSerializer
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from forms import (LoginForm, Postform, RequestResetForm, ResetPasswordForm,
                   SearchForm, UsersForm)

# Imports/dependencies up here


# Download pdf with content
# Todo list
# Finance helper

##


# Flask app start, secret key for sessions and storage location of cookies
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'


# SQLALCHEMY configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:guerra998@localhost/caderno'
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Mail configs
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'noreplydemor@gmail.com'
app.config["MAIL_PASSWORD"] = 'atqlzqllxmnowayq'


# Image uploading directory
UPLOAD_FOLDER = 'static/post-images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# App resources
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)


# Flask ADMIN config


class MyHomeView(AdminIndexView):

    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin == True:
            return True

    def inaccessible_callback(self, name, **kwargs):
        flash('You need to be an admin for that!')
        return redirect(url_for('login'))

    @expose('/')
    def index(self):
        return self.render('admin.html')


class adminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin == True:
            return True

    def inaccessible_callback(self, name, **kwargs):
        flash('You need to be an admin for that!')
        return redirect(url_for('login'))


admin = Admin(app, index_view=MyHomeView(), template_mode='bootstrap3')


# Login
lg = LoginManager(app)
lg.init_app(app)
lg.login_view = 'login'


@lg.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


# FUNCTIONS

# Reset email
def send_email(user):
    token = user.get_token()
    msg = Message('Password reset request',
                  sender='noreply@thismail.com', recipients=[user.email])
    msg.body = f""" To reset your password, visit the following link:
{url_for('reset_password', token = token, _external = True)}

If you did not make this request, please ignore this email and no changes will be made.
    """
    mail.send(msg)

##


@ app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if form.validate_on_submit():
            username = Users.query.filter_by(
                username=form.username.data).first()
            if username and check_password_hash(username.password_hash, form.password.data):
                login_user(username)
                flash('Logged in!')
                return redirect(url_for('index'))
            elif username and not check_password_hash(username.password_hash, form.password.data):
                form.password.data = ''
                flash('Wrong Password!')
                return redirect(url_for('login'))
            else:
                form.username.data = ''
                flash('Wrong Username!')
                return redirect(url_for('login'))

    return render_template('login.html', form=form)


@ app.route('/logout', methods=['GET', 'POST'])
@ login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect('/')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = UsersForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = Users.query.filter_by(
                username=form.username.data).first()
            if not username:
                hsps = generate_password_hash(
                    form.password_hash.data, 'sha256')

                if request.files['profile_pic']:

                    pic = request.files['profile_pic']
                    picfilename = secure_filename(pic.filename)
                    picname = str(uuid.uuid1()) + "_" + picfilename
                    saver = request.files['profile_pic']

                    user = Users(name=form.name.data, username=form.username.data,
                                 email=form.email.data, password_hash=hsps, profile_pic=picname)
                    db.session.add(user)
                    db.session.commit()

                    saver.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], picname))

                    flash('Account created!')
                    return redirect(url_for('login'))
                else:
                    user = Users(name=form.name.data, username=form.username.data,
                                 email=form.email.data, password_hash=hsps)
                    db.session.add(user)
                    db.session.commit()

                    flash('Account created!')
                    return redirect(url_for('login'))

    form.name.data = ''
    form.username.data = ''
    form.email.data = ''
    form.password_hash.data = ''
    form.password_hash2.data = ''
    return render_template('register.html', form=form)


@ app.route('/home', methods=['GET', 'POST'])
@ login_required
def index():
    pos = Posts.query.filter_by(poster_id=current_user.id)
    return render_template('home.html', post=pos)


@ app.route('/new-post', methods=['GET', 'POST'])
@login_required
def newpost():
    form = Postform()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            post = Posts(title=title, content=content,
                         poster_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('New entry added to your journal')
            return redirect(url_for('index'))

    return render_template('new-post.html', form=form)


@ app.route('/delete-post', methods=['POST'])
@login_required
def delete_post():

    id = request.form.get('id')
    post = Posts.query.filter_by(id=id).first()
    if post and post.poster.id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash('Entry deleted.')
        return redirect(url_for('index'))
    else:
        flash('No entry found!')
        return redirect(url_for('index'))


@ app.route('/edit-post', methods=['GET', 'POST'])
def edit_post():
    form = Postform()
    id = request.form.get('id')
    post = Posts.query.get_or_404(id)

    if post and post.poster.id == current_user.id:
        if form.validate_on_submit():

            post.title = form.title.data
            post.content = form.content.data
            post.date_updated = datetime.utcnow()
            db.session.add(post)
            db.session.commit()

            flash('Entry edited.')
            return redirect(url_for('index'))

        form.title.data = post.title
        form.content.data = post.content

    return render_template('edit-post.html', form=form, id=post.id)


@ app.route('/post', methods=['POST'])
@ login_required
def post():
    id = request.form.get("id")
    post = Posts.query.filter_by(id=id).first()
    if id and post.poster.id == current_user.id:
        return render_template('post.html', post=post)


@ app.route('/profile')
@ login_required
def profile():
    return render_template('profile.html')


@ app.route('/search')
def search():
    searched = request.args.get('q')

    posts = Posts.query.filter(Posts.title.like(
        '%' + searched + '%')).filter_by(poster_id=current_user.id).order_by(Posts.title).all()

    output = jsonify(
        [{"id": posts.id, "title": posts.title, "date_posted": posts.date_posted, "date_updated": posts.date_updated} for posts in posts])

    return output


# JINJA2 Configuration (For search)
@ app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Models for SQL
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_pic = db.Column(db.String(380), nullable=True, unique=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    username = db.Column(db.String(28), nullable=False, unique=True)
    email = db.Column(db.String(70), nullable=False, unique=True)
    about = db.Column(db.Text(260), nullable=True)
    password_hash = db.Column(db.String(150), nullable=False, unique=False)
    profile_pic = db.Column(db.String(380), nullable=True, unique=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    date_added = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, unique=False)
    post_count = db.relationship('Posts', backref='poster')

    # Token for password reseting
    def get_token(self, expires=1800):
        s = URLSafeSerializer(app.config['SECRET_KEY'], "auth")
        return s.dumps({'user_id': self.id})

    # Method to verify the token
    @ staticmethod
    def verify_token(token):
        s = URLSafeSerializer(app.config['SECRET_KEY'], "auth")
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        u = Users.query.get(user_id)
        return u


# PASSWORD RESET ROUTES
@ app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('An email has been sent!')
        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form)


@ app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = Users.verify_token(token)
    if not user:
        flash('That is an invalid token! Expired or invalid token.')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if user:
        if form.validate_on_submit():
            hsp = generate_password_hash(form.password_hash.data, 'sha256')
            user.password_hash = hsp
            db.session.add(user)
            db.session.commit()
            flash('Your password has been changed!')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('register'))
    return render_template('reset_password.html', form=form)
###


# ADMIN ROUTES
admin.add_view(adminModelView(Users, db.session))
admin.add_view(adminModelView(Posts, db.session))
###

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
