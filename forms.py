from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, EmailField, ValidationError, FloatField
from wtforms.validators import DataRequired, equal_to, length
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField("Nome", validators=[DataRequired()])
    password = StringField("Senha", validators=[DataRequired()])
    submit = SubmitField('Logar')

class Postform(FlaskForm):
    pass 

class UsersForm(FlaskForm):
    pass