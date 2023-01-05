from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, EmailField, ValidationError, FloatField
from wtforms.validators import data_required, equal_to, length

class Userform(FlaskForm):
    pass

class Postform(FlaskForm):
    pass