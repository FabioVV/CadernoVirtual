from flask import Flask, url_for, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_manager, login_user, logout_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = 'secreto'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0',port=5002,debug=True)