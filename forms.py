from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, EmailField, ValidationError, FloatField, TextAreaField
from wtforms.validators import DataRequired, equal_to, length
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = StringField("Senha", validators=[DataRequired()])
    submit = SubmitField('Logar')

class Postform(FlaskForm):
    pass 

class UsersForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    username = StringField("Usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about = TextAreaField("Sobre você...")
    profile_pic = FileField("Imagem de perfil")
    password_hash = StringField("Senha", validators=[DataRequired(), equal_to('password_hash2', message='As senhas precisam ser iguais!')])
    password_hash2 = StringField("Senha", validators=[DataRequired()])
    submit = SubmitField('Criar conta')
