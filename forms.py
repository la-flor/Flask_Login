from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25)])
    
class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25)])

