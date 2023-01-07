from functools import wraps
from flask import Flask, url_for, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user, LoginManager, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_ckeditor import CKEditor
from forms import LoginForm, UsersForm
import os


app = Flask(__name__)
app.secret_key = 'secreto'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:guerra998@localhost/caderno'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
UPLOAD_FOLDER = 'static'
ckeditor = CKEditor(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
lg = LoginManager(app)
lg.init_app(app)
lg.login_view = 'login'
@lg.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


@app.route('/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = Users.query.filter_by(username = form.username.data).first()
            if username and check_password_hash(username.password_hash, form.password.data):
                login_user(username)
                flash('Logado com sucesso!')
                return redirect(url_for('index'))
    return render_template('login.html', form = form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('Deslogado com sucesso')
    return redirect('/')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = UsersForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = Users.query.filter_by(username = form.username.data).first()
            if not username:
                hsps = generate_password_hash(form.password_hash.data, 'sha256')
                user = Users(name = form.name.data, username = form.username.data, email = form.email.data, password_hash = hsps)
                db.session.add(user)
                db.session.commit()
            flash('Conta criada com sucesso!')
            redirect(url_for('index'))

    return render_template('register.html', form = form)

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def index():
    return render_template('home.html')


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(28), nullable= False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    date_updated = db.Column(db.DateTime, default = datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable= False, unique = True)
    username = db.Column(db.String(28), nullable= False, unique = True)
    email = db.Column(db.String(70), nullable= False, unique = True)
    about = db.Column(db.Text(260), nullable= True)
    password_hash = db.Column(db.String(150), nullable= False, unique = False)
    profile_pic = db.Column(db.String(380), nullable= True, unique = False)
    date_added = db.Column(db.DateTime ,default = datetime.utcnow, nullable= False, unique = False)
    post_count = db.relationship('Posts', backref = 'poster') 

if __name__ == '__main__':
    app.run('0.0.0.0',port=5002,debug=True)