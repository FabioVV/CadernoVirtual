from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, EmailField, ValidationError, FloatField, TextAreaField
from wtforms.validators import DataRequired, equal_to, length
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Log in')

class Postform(FlaskForm):
    pass 

class UsersForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    username = StringField("Usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about = TextAreaField("Sobre você...")
    profile_pic = FileField("Imagem de perfil")
    password_hash = PasswordField("Senha", validators=[DataRequired(), equal_to('password_hash2', message='As senhas precisam ser iguais!')])
    password_hash2 = PasswordField("Senha novamente", validators=[DataRequired()])
    submit = SubmitField('Create account')
