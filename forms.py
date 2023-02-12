from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (EmailField, PasswordField, StringField, SubmitField,
                     TextAreaField, ValidationError)
from wtforms.validators import DataRequired, equal_to, length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Log in')


class Postform(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Finish")


class UsersForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    username = StringField("Usuário", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    about = TextAreaField("Sobre você...")
    profile_pic = FileField("Profile image")
    password_hash = PasswordField("Password", validators=[DataRequired(), equal_to(
        'password_hash2', message='The passwords need to match!')])
    password_hash2 = PasswordField(
        "Password again", validators=[DataRequired()])
    submit = SubmitField('Create account')


class SearchForm(FlaskForm):
    q = StringField("Search", validators=[DataRequired()])
    submit = SubmitField('Search')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password_hash = PasswordField("Password", validators=[DataRequired(), equal_to(
        'password_hash2', message='The passwords need to match!')])
    password_hash2 = PasswordField(
        "Password Again", validators=[DataRequired()])
    submit = SubmitField('Reset Password')
