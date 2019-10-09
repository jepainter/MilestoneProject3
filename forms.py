"""
Code adapted for use of WTForms in site from WTForms Documentation at 
https://wtforms.readthedocs.io/en/stable/index.html 

and with help from

Corey Shafer's tutorial found at
https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
"""

"""
Imports of packages for functioning of forms for the site
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
"""
Form classes for various forms used
"""

class RegistrationForm(FlaskForm):
    """
    Form to capture and validate registration of users
    """
    fname = StringField("First Name", 
                        validators=[DataRequired(), Length(min=1)])
    lname = StringField("Surname", 
                        validators=[DataRequired(), Length(min=1)])
    email = StringField("Email", 
                        validators=[DataRequired(), Email()])
    username = StringField("Username", 
                            validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField("Password", 
                            validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField("Confirm Password", 
                                        validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")
                            
class LogInForm(FlaskForm):
    """
    Form to capture and validate log in of users
    """
    email = StringField("Email", 
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password", 
                            validators=[DataRequired(), Length(min=8, max=16)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class AddBookForm(FlaskForm):
    """
    Form to capture and validate new book to add
    """
    title = StringField("Title:", 
                        validators=[DataRequired(), Length(min=1)])
    author_fname = StringField("Author First Name", 
                                validators=[DataRequired(), Length(min=1)])
    author_lname = StringField("Author Surname", 
                                validators=[DataRequired(), Length(min=1)])
    category_id = StringField("Category", 
                                validators=[DataRequired(), Length(min=1)]))
    user_id = StringField("UserId", 
                                validators=[DataRequired(), Length(min=1)]))
    up_votes = StringField("Up Votes", 
                                validators=[DataRequired(), Length(min=1)]))
    down_votes = StringField("Down Votes", 
                                validators=[DataRequired(), Length(min=1)]))
    cover_url = StringField("Cover Link", 
                                validators=[DataRequired(), Length(min=1)]))