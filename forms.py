from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional

class RegisterForm(FlaskForm):
    """User registration form."""
    
    username = StringField("Username", validators=[InputRequired(),Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=8, max=50)])
    email = StringField("Email", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(),Length(min=1, max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(),Length(min=1, max=30)])
    
    
class LoginForm(FlaskForm):
    """User login form."""
    
    username = StringField("Username", validators=[InputRequired(),Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=8, max=50)])


class DeleteForm(FlaskForm):
    """for route '/users/<username>'"""
    
class FeedbackForm(FlaskForm):
    """Add feedback form."""
    
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
    
